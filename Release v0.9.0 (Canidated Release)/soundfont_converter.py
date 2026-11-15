import json
import os
import struct
import wave
from array import array

ZERO_MOD = struct.pack("<HHHhH", 0, 0, 0, 0, 0)


def _riff_chunk(tag, payload):
    if len(tag) != 4:
        raise ValueError("RIFF chunk tags must be four bytes")
    pad = b"\x00" if len(payload) & 1 else b""
    return tag + struct.pack("<I", len(payload)) + payload + pad


def _list_chunk(list_type, chunks):
    return _riff_chunk(b"LIST", list_type + b"".join(chunks))


def _name20(value):
    raw = value.encode("ascii", errors="replace")[:20]
    return raw.ljust(20, b"\x00")


def _read_wav(path):
    with wave.open(path, "rb") as wav:
        channels = wav.getnchannels()
        width = wav.getsampwidth()
        rate = wav.getframerate()
        frames = wav.readframes(wav.getnframes())
    if width not in (1, 2):
        raise ValueError("only 8-bit or 16-bit PCM WAV files are supported")
    if channels < 1 or channels > 2:
        raise ValueError("only mono or stereo WAV files are supported")
    if width == 1:
        vals = array("B", frames)
        # WAV 8-bit PCM is unsigned; SF2 samples are signed 16-bit.
        signed = [((v - 128) << 8) for v in vals]
    else:
        vals = array("h")
        vals.frombytes(frames)
        if struct.pack("=H", 1) != struct.pack("<H", 1):
            vals.byteswap()
        signed = list(vals)
    if channels == 2:
        signed = [(signed[i] + signed[i + 1]) // 2
                  for i in range(0, len(signed), 2)]
    if not signed:
        raise ValueError("WAV contains no sample frames")
    if rate < 400 or rate > 192000:
        raise ValueError(f"implausible sample rate: {rate}")
    return signed, rate


def _generator(operator, amount):
    return struct.pack("<HH", operator, amount & 0xFFFF)


def _key_range(low, high):
    return bytes((low, high))


def _load_samples(sample_dir, manifest_path):
    manifest = {"samples": {}}
    if os.path.isfile(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    metadata = manifest.get("samples", {})
    items = []
    for filename in sorted(os.listdir(sample_dir)):
        if not filename.lower().endswith(".wav"):
            continue
        path = os.path.join(sample_dir, filename)
        try:
            pcm, rate = _read_wav(path)
        except (OSError, wave.Error, ValueError) as exc:
            print(f"[Warning] Skipping {filename}: {exc}")
            continue
        stem = os.path.splitext(filename)[0]
        meta = metadata.get(filename, metadata.get(stem, {}))
        root = int(meta.get("root_key", 60))
        key_range = meta.get("key_range", [0, 127])
        low, high = int(key_range[0]), int(key_range[1])
        if not (0 <= low <= high <= 127 and 0 <= root <= 127):
            print(f"[Warning] Skipping {filename}: invalid MIDI key metadata")
            continue
        loop = bool(meta.get("loop", False))
        items.append({
            "name": stem[:20], "pcm": pcm, "rate": rate,
            "root": root, "low": low, "high": high, "loop": loop
        })
    return items


def build_soundfont(sample_dir, output_path, manifest_path=None, preset_name="ROM Samples"):
    """Create a minimal SF2 file from WAV samples. Returns output path or None."""
    if not os.path.isdir(sample_dir):
        print(f"[Warning] Sample folder not found: {sample_dir}")
        return None
    if manifest_path is None:
        manifest_path = os.path.join(sample_dir, "sample_manifest.json")
    samples = _load_samples(sample_dir, manifest_path)
    if not samples:
        print("[Warning] No compatible WAV samples found; SoundFont not created.")
        return None

    smpl_data = bytearray()
    shdr_records = []
    igen_records = []
    ibag_records = []
    inst_records = []
    pgen_records = []
    pbag_records = []

    for idx, sample in enumerate(samples):
        start = len(smpl_data) // 2
        pcm = sample["pcm"]
        smpl_data.extend(struct.pack("<" + "h" * len(pcm), *pcm))
        end = len(smpl_data) // 2
        # SF2 recommends at least 46 zero-valued guard samples after each sample.
        smpl_data.extend(b"\x00" * (46 * 2))
        loop_start = start
        loop_end = end
        shdr_records.append(struct.pack(
            "<20sIIIIIBbHH",
            _name20(sample["name"]), start, end, loop_start, loop_end,
            sample["rate"], sample["root"], 0, 0, 1
        ))

        # One instrument and one sample zone per WAV.
        inst_records.append(struct.pack("<20sH", _name20(sample["name"]), idx))
        bag_start = len(igen_records)
        igen_records.append(_generator(43, (sample["low"] | (sample["high"] << 8))))
        igen_records.append(_generator(58, sample["root"]))
        if sample["loop"]:
            igen_records.append(_generator(54, 1))  # continuous loop
        igen_records.append(_generator(53, idx))  # sampleID
        ibag_records.append(struct.pack("<HH", bag_start, 0))

    # Terminal records required by SF2.
    inst_records.append(struct.pack("<20sH", _name20("EOI"), len(ibag_records)))
    ibag_records.append(struct.pack("<HH", len(igen_records), 0))
    igen_records.append(_generator(0, 0))

    # Single preset zone points to each instrument, allowing all samples in
    # one preset; each instrument contains its own key-range/sample zone.
    pgen_start = 0
    for idx in range(len(samples)):
        pgen_records.append(_generator(41, idx))  # instrument
        pbag_records.append(struct.pack("<HH", pgen_start, 0))
        pgen_start += 1
    pbag_records.append(struct.pack("<HH", len(pgen_records), 0))
    pgen_records.append(_generator(0, 0))

    phdr = struct.pack("<20sHHHIII", _name20(preset_name), 0, 0, 0, 0, 0, 0)
    phdr += struct.pack("<20sHHHIII", _name20("EOP"), 0, 0, len(pbag_records)-1, 0, 0, 0)

    pdta_chunks = [
        _riff_chunk(b"phdr", phdr),
        _riff_chunk(b"pbag", b"".join(pbag_records)),
        _riff_chunk(b"pmod", ZERO_MOD + ZERO_MOD),
        _riff_chunk(b"pgen", b"".join(pgen_records)),
        _riff_chunk(b"inst", b"".join(inst_records)),
        _riff_chunk(b"ibag", b"".join(ibag_records)),
        _riff_chunk(b"imod", ZERO_MOD + ZERO_MOD),
        _riff_chunk(b"igen", b"".join(igen_records)),
        _riff_chunk(b"shdr", b"".join(shdr_records) +
                    struct.pack("<20sIIIIIBbHH", _name20("EOS"),
                                len(smpl_data)//2, len(smpl_data)//2,
                                len(smpl_data)//2, len(smpl_data)//2,
                                44100, 0, 0, 0, 1))
    ]
    info_chunks = [
        _riff_chunk(b"ifil", struct.pack("<HH", 2, 1)),
        _riff_chunk(b"isng", b"EMU8000\x00"),
        _riff_chunk(b"INAM", preset_name.encode("ascii", errors="replace") + b"\x00")
    ]
    sdta_chunks = [_riff_chunk(b"smpl", bytes(smpl_data))]
    body = b"sfbk" + _list_chunk(b"INFO", info_chunks) + \
           _list_chunk(b"sdta", sdta_chunks) + _list_chunk(b"pdta", pdta_chunks)
    with open(output_path, "wb") as f:
        f.write(b"RIFF" + struct.pack("<I", len(body)) + body)
    print(f"[Success] SoundFont created: {output_path}")
    print(f"[Info] Included {len(samples)} WAV sample(s).")
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build a SoundFont 2 from WAV samples")
    parser.add_argument("sample_folder", help="Folder containing extracted WAV samples")
    parser.add_argument("-o", "--output", default="rom_samples.sf2")
    parser.add_argument("--manifest", default=None)
    args = parser.parse_args()
    build_soundfont(args.sample_folder, args.output, args.manifest)
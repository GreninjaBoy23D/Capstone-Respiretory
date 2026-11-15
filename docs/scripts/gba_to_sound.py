import json
import os
import struct
import wave

AUDIO_SIGNATURES = (
    (b"RIFF", b"WAVE", ".wav"),
    (b"FORM", None, ".aiff"),
    (b"OggS", None, ".ogg"),
)


def _safe_name(value):
    cleaned = "".join(c if c.isalnum() or c in "-_." else "_" for c in value)
    return cleaned.strip("._") or "audio_sample"


def _find_embedded_audio(rom_data):
    """Yield (offset, end, extension) for recognizable self-contained files."""
    found = []
    pos = 0
    while True:
        pos = rom_data.find(b"RIFF", pos)
        if pos < 0:
            break
        if pos + 12 <= len(rom_data) and rom_data[pos + 8:pos + 12] == b"WAVE":
            size = struct.unpack_from("<I", rom_data, pos + 4)[0] + 8
            end = pos + size
            if 12 <= size and end <= len(rom_data):
                found.append((pos, end, ".wav"))
        pos += 4

    # AIFF/AIFC files have a big-endian FORM length.
    pos = 0
    while True:
        pos = rom_data.find(b"FORM", pos)
        if pos < 0:
            break
        if pos + 12 <= len(rom_data) and rom_data[pos + 8:pos + 12] in (b"AIFF", b"AIFC"):
            size = struct.unpack_from(">I", rom_data, pos + 4)[0] + 8
            end = pos + size
            if 12 <= size and end <= len(rom_data):
                found.append((pos, end, ".aiff"))
        pos += 4

    # Ogg pages are not individually self-sizing as a whole stream. Extract
    # each contiguous Ogg run up to the next non-Ogg data boundary.
    pos = 0
    while True:
        pos = rom_data.find(b"OggS", pos)
        if pos < 0:
            break
        end = pos
        while end + 27 <= len(rom_data) and rom_data[end:end + 4] == b"OggS":
            segment_count = rom_data[end + 26]
            header_end = end + 27 + segment_count
            if header_end > len(rom_data):
                break
            body_size = sum(rom_data[end + 27:header_end])
            page_end = header_end + body_size
            if page_end > len(rom_data):
                break
            end = page_end
        if end > pos:
            found.append((pos, end, ".ogg"))
        pos += 4

    # Remove overlaps/duplicates and return in ROM order.
    unique = sorted(set(found))
    result = []
    last_end = -1
    for item in unique:
        if item[0] >= last_end:
            result.append(item)
            last_end = item[1]
    return result


def _convert_pcm(raw, bits, signed):
    if bits == 8:
        if signed:
            return bytes((v + 128) & 0xFF for v in struct.unpack(f"<{len(raw)}b", raw))
        return raw
    if bits == 16:
        if len(raw) % 2:
            raise ValueError("16-bit PCM region has an odd byte count")
        if signed:
            return raw
        values = struct.unpack(f"<{len(raw)//2}H", raw)
        return struct.pack(f"<{len(values)}h", *(v - 32768 for v in values))
    raise ValueError("PCM bit depth must be 8 or 16")


def _extract_pcm_regions(rom_data, regions, output_dir):
    count = 0
    for index, region in enumerate(regions, 1):
        name = _safe_name(region.get("name", f"pcm_sample_{index}"))
        offset = int(region["offset"])
        length = int(region["length"])
        rate = int(region.get("sample_rate", 22050))
        bits = int(region.get("bits", 8))
        channels = int(region.get("channels", 1))
        signed = bool(region.get("signed", False))
        if offset < 0 or length <= 0 or offset + length > len(rom_data):
            raise ValueError(f"{name}: region is outside ROM boundaries")
        if rate <= 0 or channels not in (1, 2) or bits not in (8, 16):
            raise ValueError(f"{name}: invalid rate, channels, or bit depth")
        frame_size = channels * (bits // 8)
        raw = rom_data[offset:offset + length]
        if len(raw) % frame_size:
            raise ValueError(f"{name}: data length is not frame-aligned")
        pcm = _convert_pcm(raw, bits, signed)
        out = os.path.join(output_dir, name + ".wav")
        with wave.open(out, "wb") as wav:
            wav.setnchannels(channels)
            wav.setsampwidth(bits // 8)
            wav.setframerate(rate)
            wav.writeframes(pcm)
        print(f"[Success] PCM sample exported: {out}")
        count += 1
    return count


def extract_audio(rom_path):
    """Extract embedded audio files and configured PCM regions from a ROM."""
    if not os.path.isfile(rom_path):
        print(f"[Error] ROM file does not exist: {rom_path}")
        return False

    output_dir = os.path.join(os.path.dirname(os.path.abspath(rom_path)), "extracted_audio")
    os.makedirs(output_dir, exist_ok=True)

    with open(rom_path, "rb") as f:
        rom_data = f.read()

    extracted = 0
    for index, (start, end, extension) in enumerate(_find_embedded_audio(rom_data), 1):
        filename = f"embedded_{index:03d}_0x{start:X}{extension}"
        path = os.path.join(output_dir, filename)
        with open(path, "wb") as f:
            f.write(rom_data[start:end])
        print(f"[Success] Embedded audio exported: {path}")
        extracted += 1

    # Optional per-ROM metadata file. Offsets must be verified for the game.
    config_path = os.path.join(os.path.dirname(os.path.abspath(rom_path)), "audio_regions.json")
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            regions = config.get("regions", [])
            extracted += _extract_pcm_regions(rom_data, regions, output_dir)
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            print(f"[Warning] PCM region configuration was not processed: {exc}")
    else:
        print("[Info] No audio_regions.json found; configured raw PCM extraction skipped.")

    print(f"\nAudio extraction finished: {extracted} file(s).")
    print(f"Output folder: {output_dir}")
    if not extracted:
        print("[Info] No standalone audio files were identified.")
        print("[Info] GBA M4A/Sappy samples generally need game-specific sample/ADPCM decoding.")
    return extracted > 0


if __name__ == "__main__":
    path = input("Enter imported ROM path: ").strip().strip('"')
    extract_audio(path)
    input("Press Enter to exit...")

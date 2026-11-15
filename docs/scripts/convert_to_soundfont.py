
import os
import wave
import struct

SAMPLE_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "extracted_samples"
)

OUTPUT_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "soundfonts"
)


def chunk(name, data):
    """Create a RIFF chunk."""
    result = name.encode("ascii")
    result += struct.pack("<I", len(data))
    result += data

    if len(data) % 2:
        result += b"\x00"

    return result


def list_chunk(name, data):
    """Create a RIFF LIST chunk."""
    return chunk("LIST", name.encode("ascii") + data)


def fixed_name(name, length=20):
    """Create a fixed-length SoundFont name."""
    return name.encode("ascii", errors="replace")[:length].ljust(
        length, b"\x00"
    )


def read_wav(filepath):
    """Read a mono 8-bit or 16-bit PCM WAV file."""

    with wave.open(filepath, "rb") as wav:

        channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        frame_count = wav.getnframes()

        if channels != 1:
            raise ValueError(
                f"{filepath} must be mono audio."
            )

        if sample_width not in (1, 2):
            raise ValueError(
                f"{filepath} must use 8-bit or 16-bit PCM."
            )

        if wav.getcomptype() != "NONE":
            raise ValueError("Compressed WAV files are not supported.")

        raw = wav.readframes(frame_count)

    if sample_width == 1:
        # WAV 8-bit PCM is unsigned.
        samples = [
            (value - 128) << 8
            for value in raw
        ]

    else:
        count = len(raw) // 2
        samples = list(
            struct.unpack("<" + "h" * count, raw)
        )

    return samples, sample_rate


def make_soundfont(sample_files, output_path):

    if not sample_files:
        raise ValueError("No WAV samples were supplied.")

    if len(sample_files) > 128:
        raise ValueError(
            "This version supports a maximum of 128 samples."
        )

    all_samples = []
    sample_headers = []
    instrument_bags = []
    instrument_generators = []

    current_position = 0

    for index, filepath in enumerate(sample_files):

        samples, sample_rate = read_wav(filepath)

        if not samples:
            print(f"[Warning] Skipping empty sample: {filepath}")
            continue

        sample_name = os.path.splitext(
            os.path.basename(filepath)
        )[0]

        start = current_position
        end = start + len(samples)

        # No looping by default.
        loop_start = start
        loop_end = end

        # Add sample data.
        all_samples.extend(samples)

        # SoundFont requires 46 extra sample points.
        all_samples.extend([0] * 46)

        current_position += len(samples) + 46

        # Assign each sample to a separate MIDI note.
        midi_note = index

        # Add instrument bag.
        instrument_bags.append(
            (len(instrument_generators), 0)
        )

        # Generator 43: Key range.
        instrument_generators.append(
            (43, (midi_note << 8) | midi_note)
        )

        # Generator 58: Overriding root key.
        instrument_generators.append(
            (58, midi_note)
        )

        # Generator 53: Sample ID.
        instrument_generators.append(
            (53, index)
        )

        # Create sample header.
        sample_headers.append({
            "name": sample_name,
            "start": start,
            "end": end,
            "loop_start": loop_start,
            "loop_end": loop_end,
            "rate": sample_rate,
            "pitch": midi_note
        })

        print(
            f"[Info] Added {sample_name} "
            f"(MIDI note {midi_note})"
        )

    if not sample_headers:
        raise ValueError("No valid WAV samples were found.")

    # Build sample data.
    smpl_data = struct.pack(
        "<" + "h" * len(all_samples),
        *all_samples
    )

    # Build preset header.
    preset_header = (
        fixed_name("ROM Samples")
        + struct.pack("<HHHIII", 0, 0, 0, 0, 0, 0)
    )

    preset_terminal = (
        fixed_name("EOP")
        + struct.pack("<HHHIII", 0, 0, 1, 0, 0, 0)
    )

    phdr = preset_header + preset_terminal

    # Preset bag and generator.
    pbag = (
        struct.pack("<HH", 0, 0)
        + struct.pack("<HH", 1, 0)
    )

    pgen = (
        struct.pack("<HH", 41, 0)
    )

    # Preset modulator terminal.
    pmod = b"\x00" * 10

    # Instrument headers.
    inst = (
        fixed_name("ROM Instrument")
        + struct.pack("<H", 0)
        + fixed_name("EOI")
        + struct.pack("<H", len(instrument_bags))
    )

    # Instrument bags.
    ibag = b""

    for gen_index, mod_index in instrument_bags:
        ibag += struct.pack("<HH", gen_index, mod_index)

    ibag += struct.pack(
        "<HH",
        len(instrument_generators),
        0
    )

    # Instrument generators.
    igen = b""

    for operator, amount in instrument_generators:
        igen += struct.pack(
            "<HH",
            operator,
            amount & 0xFFFF
        )

    # Instrument modulator terminal.
    imod = b"\x00" * 10

    # Sample headers.
    shdr = b""

    for sample in sample_headers:

        shdr += (
            fixed_name(sample["name"])
            + struct.pack(
                "<IIIIIBbHH",
                sample["start"],
                sample["end"],
                sample["loop_start"],
                sample["loop_end"],
                sample["rate"],
                sample["pitch"],
                0,
                0,
                1
            )
        )

    # Required terminal sample header.
    shdr += (
        fixed_name("EOS")
        + struct.pack(
            "<IIIIIBbHH",
            current_position,
            current_position,
            current_position,
            current_position,
            44100,
            0,
            0,
            0,
            1
        )
    )

    # SoundFont INFO section.
    info = (
        chunk("ifil", struct.pack("<HH", 2, 1))
        + chunk("isng", b"EMU8000\x00")
        + chunk("INAM", b"ROM Generated SoundFont\x00")
        + chunk("ISFT", b"Python ROM Converter\x00")
    )

    # SoundFont sample data section.
    sdta = chunk("smpl", smpl_data)

    # SoundFont preset/instrument data section.
    pdta = (
        chunk("phdr", phdr)
        + chunk("pbag", pbag)
        + chunk("pmod", pmod)
        + chunk("pgen", pgen)
        + chunk("inst", inst)
        + chunk("ibag", ibag)
        + chunk("imod", imod)
        + chunk("igen", igen)
        + chunk("shdr", shdr)
    )

    # Combine SoundFont sections.
    sf2_data = (
        list_chunk("INFO", info)
        + list_chunk("sdta", sdta)
        + list_chunk("pdta", pdta)
    )

    # Create final RIFF file.
    riff_data = (
        b"sfbk"
        + sf2_data
    )

    with open(output_path, "wb") as file:
        file.write(b"RIFF")
        file.write(struct.pack("<I", len(riff_data)))
        file.write(riff_data)

    print("\n[Success] SoundFont created!")
    print(f"[Info] Output: {output_path}")


def convert_samples():

    print("\n=== ROM to SoundFont Converter ===")

    if not os.path.exists(SAMPLE_FOLDER):
        print("[Error] Extracted samples folder not found.")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    sample_files = [
        os.path.join(SAMPLE_FOLDER, file)
        for file in os.listdir(SAMPLE_FOLDER)
        if file.lower().endswith(".wav")
    ]

    sample_files.sort()

    if not sample_files:
        print("[Warning] No WAV samples found.")
        return

    print(f"[Info] Found {len(sample_files)} samples.")

    filename = input(
        "\nEnter SoundFont filename: "
    ).strip()

    if not filename:
        filename = "ROM_SoundFont"

    if not filename.lower().endswith(".sf2"):
        filename += ".sf2"

    # Prevent invalid Windows filename characters.
    invalid_chars = '<>:"/\\|?*'

    if any(char in invalid_chars for char in filename):
        print("[Error] Invalid SoundFont filename.")
        return

    output_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    try:
        make_soundfont(sample_files, output_path)

    except (OSError, ValueError, wave.Error, struct.error) as error:
        print(f"[Error] SoundFont conversion failed: {error}")


if __name__ == "__main__":
    convert_samples()

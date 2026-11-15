
import os
import wave
import struct


# ==========================================
# GBA ROM AUDIO EXTRACTOR
# ==========================================

GBA_HEADER_OFFSET = 0xA0
GBA_HEADER_SIZE = 0x20

# Add verified sample locations for a particular game.
GBA_SAMPLE_REGIONS = []


def validate_gba_rom(rom_data):
    """Validate the basic GBA ROM header."""

    if len(rom_data) < 0xC0:
        raise ValueError("ROM is too small to contain a GBA header.")

    title = rom_data[0xA0:0xAC].decode(
        "ascii", errors="replace"
    ).strip("\x00 ")

    game_code = rom_data[0xAC:0xB0].decode(
        "ascii", errors="replace"
    )

    maker_code = rom_data[0xB0:0xB2].decode(
        "ascii", errors="replace"
    )

    fixed_byte = rom_data[0xB2]
    stored_checksum = rom_data[0xBD]

    calculated_checksum = (
        -(sum(rom_data[0xA0:0xBD]) + 0x19)
    ) & 0xFF

    valid_checksum = calculated_checksum == stored_checksum

    return {
        "title": title,
        "game_code": game_code,
        "maker_code": maker_code,
        "valid_header": fixed_byte == 0x96,
        "valid_checksum": valid_checksum
    }


def find_audio_markers(rom_data):
    """Search for recognizable M4A/Sappy markers."""

    markers = []
    signatures = [b"M4A "]

    for signature in signatures:
        start = 0

        while True:
            offset = rom_data.find(signature, start)

            if offset == -1:
                break

            markers.append(offset)
            start = offset + 1

    return markers


def convert_sample(raw_data, bits, signed):
    """Convert sample data into WAV-compatible PCM."""

    if bits == 8:
        if signed:
            return bytes(
                (value + 128) % 256
                for value in struct.unpack(
                    f"<{len(raw_data)}b", raw_data
                )
            )
        return raw_data

    if bits == 16:
        if len(raw_data) % 2:
            raise ValueError("Invalid 16-bit PCM sample length.")

        if signed:
            return raw_data

        samples = struct.unpack(
            f"<{len(raw_data) // 2}H", raw_data
        )

        return struct.pack(
            f"<{len(samples)}h",
            *(value - 32768 for value in samples)
        )

    raise ValueError("Only 8-bit and 16-bit PCM are supported.")


def extract_gba_sample(rom_data, region, output_dir):
    """Extract one configured PCM sample."""

    name = region["name"]
    offset = region["offset"]
    length = region["length"]

    sample_rate = region.get("sample_rate", 22050)
    bits = region.get("bits", 8)
    channels = region.get("channels", 1)
    signed = region.get("signed", False)

    if offset < 0 or length <= 0:
        raise ValueError("Invalid sample offset or length.")

    if offset + length > len(rom_data):
        raise ValueError("Sample exceeds ROM boundaries.")

    if sample_rate <= 0 or channels not in (1, 2):
        raise ValueError("Invalid sample rate or channel count.")

    if bits not in (8, 16):
        raise ValueError("Unsupported PCM bit depth.")

    raw_data = rom_data[offset:offset + length]

    if len(raw_data) % (channels * (bits // 8)) != 0:
        raise ValueError("Sample data is not frame-aligned.")

    pcm_data = convert_sample(raw_data, bits, signed)

    output_path = os.path.join(output_dir, name + ".wav")

    with wave.open(output_path, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(bits // 8)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)

    print(f"[Success] Extracted {name}.wav")


def extract_gba(rom_path):
    """Analyze a GBA ROM and extract configured PCM samples."""

    print("\n=== GBA ROM Audio Extractor ===")

    if not os.path.isfile(rom_path):
        print("[Error] ROM file does not exist.")
        return False

    try:
        with open(rom_path, "rb") as rom_file:
            rom_data = rom_file.read()

        info = validate_gba_rom(rom_data)

        print(f"\nGame Title: {info['title']}")
        print(f"Game Code: {info['game_code']}")
        print(f"Maker Code: {info['maker_code']}")
        print(f"ROM Size: {len(rom_data) / 1024:.2f} KB")

        print(
            "Header: "
            + ("Valid" if info["valid_header"] else "Invalid")
        )

        print(
            "Checksum: "
            + ("Valid" if info["valid_checksum"] else "Invalid")
        )

        if not info["valid_header"]:
            print("[Error] This does not appear to be a valid GBA ROM.")
            return False

        markers = find_audio_markers(rom_data)

        print(f"\nPossible M4A markers found: {len(markers)}")

        for offset in markers[:20]:
            print(f"  Marker at ROM offset: 0x{offset:X}")

        if not markers:
            print("[Info] No recognizable M4A markers found.")
            print("[Info] The game may use another audio engine.")

        if not GBA_SAMPLE_REGIONS:
            print("\n[Warning] No verified sample regions configured.")
            print("[Info] Automatic audio-engine parsing is not yet implemented.")
            return False

        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "extracted_samples",
            info["game_code"]
        )

        os.makedirs(output_dir, exist_ok=True)

        extracted = 0

        for region in GBA_SAMPLE_REGIONS:
            try:
                extract_gba_sample(
                    rom_data, region, output_dir
                )
                extracted += 1

            except (ValueError, KeyError, wave.Error) as error:
                print(f"[Error] {region.get('name', 'Unknown')}: {error}")

        print(f"\nExtracted {extracted} of {len(GBA_SAMPLE_REGIONS)} samples.")
        print(f"Output: {output_dir}")

        return extracted > 0

    except OSError as error:
        print(f"[Error] Could not read ROM: {error}")
        return False


if __name__ == "__main__":
    path = input("Enter GBA ROM path: ").strip().strip('"')
    extract_gba(path)
    input("\nPress Enter to exit...")

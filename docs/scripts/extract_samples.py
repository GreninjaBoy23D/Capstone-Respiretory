
import os
import wave
import struct

SAMPLE_REGIONS = []

def convert_pcm(data, bits, signed):
    """Convert raw PCM data into WAV-compatible PCM."""

    if bits == 8 and signed:
        # Convert signed 8-bit PCM to unsigned WAV PCM.
        return bytes((value + 128) % 256 for value in
                     struct.unpack(f"{len(data)}b", data))

    elif bits == 8 and not signed:
        return data

    elif bits == 16:
        if len(data) % 2 != 0:
            raise ValueError("16-bit PCM data has an invalid length.")

        # WAV uses little-endian signed 16-bit PCM.
        return data

    else:
        raise ValueError(f"Unsupported PCM bit depth: {bits}")


def extract_sample(rom_data, region, output_dir):
    """Extract one sample from the ROM."""

    name = region["name"]
    offset = region["offset"]
    length = region["length"]
    sample_rate = region.get("sample_rate", 22050)
    channels = region.get("channels", 1)
    bits = region.get("bits", 8)
    signed = region.get("signed", True)

    # Validate sample information.
    if offset < 0 or length <= 0:
        raise ValueError(f"{name}: Invalid sample offset or length.")

    if offset + length > len(rom_data):
        raise ValueError(f"{name}: Sample extends beyond ROM boundaries.")

    if sample_rate <= 0 or channels not in (1, 2):
        raise ValueError(f"{name}: Invalid sample rate or channel count.")

    if bits not in (8, 16):
        raise ValueError(f"{name}: Unsupported bit depth.")

    # Read sample bytes.
    raw_data = rom_data[offset:offset + length]

    # Convert PCM data.
    pcm_data = convert_pcm(raw_data, bits, signed)

    # Create WAV file.
    output_path = os.path.join(output_dir, name + ".wav")

    with wave.open(output_path, "wb") as wav:
        wav.setnchannels(channels)
        wav.setsampwidth(bits // 8)
        wav.setframerate(sample_rate)
        wav.writeframes(pcm_data)

    print(f"[Success] Extracted: {name}.wav")


def extract_samples(rom_path):
    """Extract configured PCM samples from an imported ROM."""

    print("\n=== ROM Sample Extraction ===")

    if not os.path.isfile(rom_path):
        print("[Error] ROM file does not exist.")
        return False

    # Create output directory.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, "extracted_samples")
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(rom_path, "rb") as rom_file:
            rom_data = rom_file.read()

        if not SAMPLE_REGIONS:
            print("[Warning] No sample regions configured.")
            print("[Info] Starting ROM audio analysis...")

            print(f"ROM Size: {len(rom_data)} bytes")
            print(f"ROM Size: {len(rom_data) / 1024:.2f} KB")

            print("[Info] No game-specific audio decoder is installed.")
            print("[Info] Please configure a console-specific parser.")

            return False

        extracted = 0

        for region in SAMPLE_REGIONS:
            try:
                extract_sample(rom_data, region, output_dir)
                extracted += 1

            except (ValueError, KeyError, wave.Error) as error:
                print(f"[Error] Could not extract sample: {error}")

        print(f"\nExtraction completed: {extracted}/{len(SAMPLE_REGIONS)}")
        print(f"Output directory: {output_dir}")

        return extracted > 0

    except OSError as error:
        print(f"[Error] Failed to read ROM: {error}")
        return False


if __name__ == "__main__":
    rom_path = input("Enter imported ROM path: ").strip().strip('"')
    extract_samples(rom_path)
    input("\nPress Enter to exit...")

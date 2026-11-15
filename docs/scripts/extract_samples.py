
from gba_to_sound import extract_audio


def extract_samples(rom_path):
    return extract_audio(rom_path)


if __name__ == "__main__":
    path = input("Enter imported ROM path: ").strip().strip('"')
    extract_samples(path)
    input("\\nPress Enter to exit...")

import os
import shutil

from extract_samples import extract_audio
from soundfont_converter import build_soundfont
from gba_parsing import GBAAudioParser

VALID_EXTENSIONS = {
    ".nes", ".sfc", ".smc", ".gba", ".gbc", ".gb", ".nds",
    ".bin", ".iso", ".v64", ".z64"
}


def import_rom():
    print("=== Video Game ROM Importer ===")
    file_path = input(
        "Import ROM file by typing in the file path or dragging and dropping it: "
    ).strip().strip('"')

    if not os.path.isfile(file_path):
        print(f"\\n[Error] ROM file not found or is not a file: {file_path}")
        return False

    _, ext = os.path.splitext(file_path)
    if ext.lower() not in VALID_EXTENSIONS:
        print(f"\\n[Warning] '{ext}' is not a recognized ROM extension.")
        if input("Import anyway? (y/n): ").strip().lower() != "y":
            print("Import cancelled.")
            return False

    project_dir = os.path.dirname(os.path.abspath(__file__))
    import_dir = os.path.join(project_dir, "imported_roms")
    os.makedirs(import_dir, exist_ok=True)

    filename = os.path.basename(file_path)
    dest_path = os.path.join(import_dir, filename)

    try:
        shutil.copy2(file_path, dest_path)
        print(f"\\n[Success] ROM imported: {dest_path}")

        if ext.lower() == ".gba":
            print("\\n[Info] GBA ROM detected; analyzing audio-engine structures...")
            parser = GBAAudioParser(dest_path)
            parser.parse()

        print("\\n[Info] Extracting embedded audio and configured PCM samples...")
        extract_audio(dest_path)

        audio_dir = os.path.join(import_dir, "extracted_audio")
        soundfont_dir = os.path.join(import_dir, "soundfonts")
        os.makedirs(soundfont_dir, exist_ok=True)
        rom_stem = os.path.splitext(filename)[0]
        safe_stem = "".join(c if c.isalnum() or c in "-_." else "_" for c in rom_stem)
        sf2_path = os.path.join(soundfont_dir, safe_stem + ".sf2")
        manifest_path = os.path.join(audio_dir, "sample_manifest.json")

        print("\\n[Info] Building SoundFont from extracted WAV samples...")
        result = build_soundfont(
            sample_dir=audio_dir,
            output_path=sf2_path,
            manifest_path=manifest_path,
            preset_name=(safe_stem[:20] or "ROM Samples")
        )
        if result:
            print(f"[Success] SoundFont saved: {result}")
        else:
            print("[Info] SoundFont was not created because no compatible WAV samples were found.")

        return True

    except (OSError, ValueError, RuntimeError) as error:
        print(f"\\n[Error] Failed to import or process ROM: {error}")
        return False


if __name__ == "__main__":
    import_rom()
    input("\\nPress Enter to exit...")


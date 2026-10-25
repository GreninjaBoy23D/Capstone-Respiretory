import os
import sys
import shutil

# Define allowed video game ROM extensions
VALID_EXTENSIONS = {'.nes', '.sfc', '.smc', '.gba', '.gbc', '.gb', '.nds', '.bin', '.iso', '.v64', '.z64'}

def import_rom():
    print("=== Video Game ROM Importer ===")
    file_path = input("Enter or drag-and-drop the full path to the ROM file: ").strip('" ')

    # Validate file existence
    if not os.path.exists(file_path):
        print(f"\n[Error] File does not exist at: {file_path}")
        return False
        
    if not os.path.isfile(file_path):
        print(f"\n[Error] The path provided is a directory, not a file.")
        return False

    # Validate file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in VALID_EXTENSIONS:
        print(f"\n[Warning] '{ext}' is not a recognized ROM extension.")
        confirm = input("Do you still want to import it? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Import cancelled.")
            return False

    # Define your destination directory (e.g., a 'roms' folder where the script runs)
    dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imported_roms")
    os.makedirs(dest_dir, exist_ok=True)

    # Copy the file
    filename = os.path.basename(file_path)
    dest_path = os.path.join(dest_dir, filename)

    try:
        shutil.copy2(file_path, dest_path)
        print(f"\n[Success] Imported successfully!")
        print(f"Saved to: {dest_path}")
        return True
    except Exception as e:
        print(f"\n[Error] Failed to copy file: {e}")
        return False

if __name__ == "__main__":
    import_rom()
    print("\nPress Enter to exit...")
    input()

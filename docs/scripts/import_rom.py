import sys
import os

def import_rom(file_path):
    if not os.path.exists(file_path):
        print ("File not Found")
        return

    file_size = os.path.getsize(file_path)
    print(f"Loading ROM: {file_path}")
    print(f"File Size: {file_size} bytes")

    with open(file_path, "rb") as f:
        header = f.red(16)
        print(f"first 16 bytes (hex): {header.hex()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_rom.py <path_to_rom>")
    else:
        import_rom(sys.argv[1])


import os
import struct
import json

GBA_ROM_BASE = 0x08000000

# Known M4A-related marker
M4A_SIGNATURES = [
    b"M4A ",
]


class GBAAudioParser:

    def __init__(self, rom_path):
        self.rom_path = rom_path
        self.rom_data = b""
        self.audio_info = {
            "engine": "Unknown",
            "game_title": "",
            "game_code": "",
            "songs": [],
            "voicegroups": [],
            "markers": []
        }

    def load_rom(self):

        if not os.path.isfile(self.rom_path):
            raise FileNotFoundError("GBA ROM not found.")

        with open(self.rom_path, "rb") as file:
            self.rom_data = file.read()

        if len(self.rom_data) < 0xC0:
            raise ValueError("Invalid or incomplete GBA ROM.")

        print("[Info] GBA ROM loaded successfully.")

    def read_game_info(self):

        data = self.rom_data

        self.audio_info["game_title"] = (
            data[0xA0:0xAC].decode(
                "ascii", errors="replace"
            ).strip("\x00 ")
        )

        self.audio_info["game_code"] = (
            data[0xAC:0xB0].decode(
                "ascii", errors="replace"
            )
        )

        print(
            "[Info] Game:",
            self.audio_info["game_title"]
        )

        print(
            "[Info] Game Code:",
            self.audio_info["game_code"]
        )

    def gba_to_offset(self, address):

        if 0x08000000 <= address < 0x0A000000:

            offset = address - GBA_ROM_BASE

            if offset < len(self.rom_data):
                return offset

        return None

    def offset_to_gba(self, offset):

        if 0 <= offset < len(self.rom_data):
            return GBA_ROM_BASE + offset

        return None

    def read_u32(self, offset):

        if offset < 0 or offset + 4 > len(self.rom_data):
            return None

        return struct.unpack_from(
            "<I", self.rom_data, offset
        )[0]

    def find_m4a_markers(self):

        print("\n[Info] Searching for M4A markers...")

        for signature in M4A_SIGNATURES:

            start = 0

            while True:

                offset = self.rom_data.find(
                    signature, start
                )

                if offset == -1:
                    break

                self.audio_info["markers"].append({
                    "signature": signature.decode(
                        "ascii", errors="replace"
                    ),
                    "offset": offset,
                    "gba_address": hex(
                        self.offset_to_gba(offset)
                    )
                })

                print(
                    f"[Found] M4A marker at 0x{offset:X}"
                )

                start = offset + 1

    def check_song_header(self, offset):

        if offset + 8 > len(self.rom_data):
            return None

        data = self.rom_data

        track_count = data[offset]
        block_count = data[offset + 1]
        priority = data[offset + 2]
        reverb = data[offset + 3]

        voicegroup_address = self.read_u32(
            offset + 4
        )

        voicegroup_offset = self.gba_to_offset(
            voicegroup_address
        ) if voicegroup_address is not None else None

        # Basic plausibility checks.
        if not 1 <= track_count <= 16:
            return None

        if block_count > 16:
            return None

        if reverb > 127:
            return None

        if voicegroup_offset is None:
            return None

        return {
            "offset": offset,
            "address": self.offset_to_gba(offset),
            "track_count": track_count,
            "block_count": block_count,
            "priority": priority,
            "reverb": reverb,
            "voicegroup_address": voicegroup_address,
            "voicegroup_offset": voicegroup_offset
        }

    def find_song_headers(self):

        print("\n[Info] Scanning possible song headers...")

        candidates = []

        # Song headers are aligned to 4 bytes
        for offset in range(
            0,
            len(self.rom_data) - 8,
            4
        ):

            candidate = self.check_song_header(offset)

            if candidate is not None:
                candidates.append(candidate)

        self.audio_info["songs"] = candidates

        print(
            f"[Info] Possible song headers: {len(candidates)}"
        )

        for song in candidates[:20]:

            print(
                f"[Song Candidate] "
                f"ROM Offset: 0x{song['offset']:X} | "
                f"Tracks: {song['track_count']} | "
                f"Voice Group: 0x{song['voicegroup_address']:08X}"
            )

    def inspect_voicegroups(self):

        print("\n[Info] Inspecting voice group pointers...")

        inspected = set()

        for song in self.audio_info["songs"]:

            offset = song["voicegroup_offset"]

            if offset in inspected:
                continue

            inspected.add(offset)

            if offset + 8 > len(self.rom_data):
                continue

            first_entry = self.rom_data[offset:offset + 8]

            self.audio_info["voicegroups"].append({
                "rom_offset": offset,
                "gba_address": hex(
                    self.offset_to_gba(offset)
                ),
                "first_entry_hex": first_entry.hex(),
                "status": "Candidate voice group; needs validation"
            })

            print(
                f"[Voice Group Candidate] "
                f"ROM Offset: 0x{offset:X}"
            )

    def export_report(self):

        output_dir = os.path.join(
            os.path.dirname(
                os.path.abspath(self.rom_path)
            ),
            "gba_audio_reports"
        )

        os.makedirs(output_dir, exist_ok=True)

        game_code = self.audio_info["game_code"]

        safe_name = "".join(
            c for c in game_code
            if c.isalnum()
        ) or "UNKNOWN"

        output_path = os.path.join(
            output_dir,
            safe_name + "_audio_report.json"
        )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.audio_info,
                file,
                indent=4
            )

        print("\n[Success] Audio report exported.")
        print(f"[Info] Report: {output_path}")

    def parse(self):

        print("\n=== GBA Audio Engine Parser ===")

        self.load_rom()

        self.read_game_info()

        self.find_m4a_markers()

        self.find_song_headers()

        self.inspect_voicegroups()

        self.export_report()

        print("\n=== GBA Audio Analysis Complete ===")

if __name__ == "__main__":

    rom_path = input(
        "Enter GBA ROM file path: "
    ).strip().strip('"')

    try:

        parser = GBAAudioParser(rom_path)

        parser.parse()

    except (OSError, ValueError) as error:

        print(f"[Error] {error}")

    input("\nPress Enter to exit...")

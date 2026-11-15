
import os
import json
import struct
import wave

ROM_BASE = 0x08000000

SONG_HEADER_SIZE = 12
VOICE_SIZE = 12
SOUND_HEADER_SIZE = 16

MAX_VOICES = 128
MAX_SAMPLE_SIZE = 16 * 1024 * 1024

DEFAULT_SAMPLE_RATE = 13379


class GBAAudioExtractor:

    def __init__(self, file_path):

        self.rom_path = file_path
        self.rom = b""

        self.output_dir = os.path.join(
            os.path.dirname(os.path.abspath(file_path)),
            "extracted_samples"
        )

        self.report = {
            "engine": "M4A/Sappy",
            "songs": [],
            "instruments": [],
            "samples": [],
            "errors": []
        }

        self.visited_groups = set()
        self.visited_samples = set()

    def load_rom(self):

        with open(self.rom_path, "rb") as file:
            self.rom = file.read()

        if len(self.rom) < 0xC0:
            raise ValueError("Invalid GBA ROM.")

        title = self.rom[0xA0:0xAC].decode(
            "ascii", errors="replace"
        ).strip("\x00 ")

        game_code = self.rom[0xAC:0xB0].decode(
            "ascii", errors="replace"
        )

        self.report["game_title"] = title
        self.report["game_code"] = game_code

        os.makedirs(self.output_dir, exist_ok=True)

        print(f"[Info] Game: {title}")
        print(f"[Info] Game Code: {game_code}")
        print(f"[Info] ROM Size: {len(self.rom)} bytes")

    # ======================================
    # ADDRESS CONVERSION
    # ======================================

    def address_to_offset(self, address):

        if 0x08000000 <= address < 0x0A000000:

            offset = address - ROM_BASE

            if offset < len(self.rom):
                return offset

        return None

    def offset_to_address(self, offset):

        if 0 <= offset < len(self.rom):
            return ROM_BASE + offset

        return None

    def read_u32(self, offset):

        if offset < 0 or offset + 4 > len(self.rom):
            raise ValueError("Invalid ROM pointer location.")

        return struct.unpack_from(
            "<I", self.rom, offset
        )[0]

    # ======================================
    # PARSE SONG HEADER
    # ======================================

    def parse_song_header(self, song_offset):

        if song_offset < 0:
            raise ValueError("Invalid song header offset.")

        if song_offset + SONG_HEADER_SIZE > len(self.rom):
            raise ValueError("Song header exceeds ROM boundaries.")

        track_count = self.rom[song_offset]
        block_count = self.rom[song_offset + 1]
        priority = self.rom[song_offset + 2]
        reverb = self.rom[song_offset + 3]

        voicegroup_address = self.read_u32(
            song_offset + 4
        )

        voicegroup_offset = self.address_to_offset(
            voicegroup_address
        )

        if not 1 <= track_count <= 16:
            raise ValueError("Invalid song track count.")

        if voicegroup_offset is None:
            raise ValueError("Invalid voice group pointer.")

        song = {
            "offset": hex(song_offset),
            "track_count": track_count,
            "block_count": block_count,
            "priority": priority,
            "reverb": reverb,
            "voicegroup_address": hex(voicegroup_address),
            "voicegroup_offset": voicegroup_offset
        }

        self.report["songs"].append(song)

        print("\n[Success] Song header parsed.")
        print(f"[Info] Tracks: {track_count}")
        print(f"[Info] Voice Group: 0x{voicegroup_address:08X}")

        return voicegroup_offset

    # ======================================
    # PARSE VOICE GROUP
    # ======================================

    def parse_voicegroup(self, group_offset, depth=0):

        if depth > 8:
            return

        if group_offset in self.visited_groups:
            return

        if group_offset < 0 or group_offset + VOICE_SIZE > len(self.rom):
            return

        self.visited_groups.add(group_offset)

        print(
            f"\n[Info] Parsing voice group at "
            f"0x{group_offset:X}"
        )

        for index in range(MAX_VOICES):

            offset = group_offset + index * VOICE_SIZE

            if offset + VOICE_SIZE > len(self.rom):
                break

            voice = self.rom[offset:offset + VOICE_SIZE]

            voice_type = voice[0]
            base_key = voice[1]
            pan = voice[2]

            sample_pointer = struct.unpack_from(
                "<I", voice, 4
            )[0]

            instrument = {
                "index": index,
                "type": voice_type,
                "base_key": base_key,
                "pan": pan,
                "offset": hex(offset)
            }

            # DirectSound voice types.
            if voice_type in (0, 8, 16):

                sample_offset = self.address_to_offset(
                    sample_pointer
                )

                instrument["format"] = "DirectSound"

                instrument["sample_pointer"] = hex(
                    sample_pointer
                )

                self.report["instruments"].append(instrument)

                if sample_offset is not None:

                    self.extract_wave_data(
                        sample_offset,
                        index,
                        voice_type
                    )

                else:
                    instrument["status"] = "Invalid sample pointer"

            # Keysplit voice.
            elif voice_type == 0x40:

                self.report["instruments"].append(instrument)

                subgroup_offset = self.address_to_offset(
                    sample_pointer
                )

                if subgroup_offset is not None:

                    print(
                        f"[Info] Keysplit instrument {index}"
                    )

                    self.parse_voicegroup(
                        subgroup_offset,
                        depth + 1
                    )

            # Drum group / keysplit-all voice.
            elif voice_type == 0x80:

                self.report["instruments"].append(instrument)

                subgroup_offset = self.address_to_offset(
                    sample_pointer
                )

                if subgroup_offset is not None:

                    print(
                        f"[Info] Drum group {index}"
                    )

                    self.parse_voicegroup(
                        subgroup_offset,
                        depth + 1
                    )

            # Other voice types.
            else:

                instrument["format"] = "Non-DirectSound"

                self.report["instruments"].append(instrument)

    # ======================================
    # EXTRACT WAVEDATA
    # ======================================

    def extract_wave_data(
        self,
        wave_offset,
        instrument_index,
        voice_type
    ):

        if wave_offset in self.visited_samples:
            return

        if wave_offset < 0:
            return

        if wave_offset + SOUND_HEADER_SIZE > len(self.rom):
            return

        self.visited_samples.add(wave_offset)

        # WaveData:
        # u16 type
        # u16 status
        # u32 frequency
        # u32 loopStart
        # u32 size
        # s8 data[]

        wave_type, status, frequency, loop_start, size = (
            struct.unpack_from(
                "<HHIII",
                self.rom,
                wave_offset
            )
        )

        if size <= 0 or size > MAX_SAMPLE_SIZE:
            print("[Warning] Invalid sample size.")
            return

        data_offset = wave_offset + SOUND_HEADER_SIZE

        data_end = data_offset + size

        if data_end > len(self.rom):
            print("[Warning] Sample exceeds ROM boundaries.")
            return

        if frequency == 0:
            frequency = DEFAULT_SAMPLE_RATE

        if loop_start > size:
            print("[Warning] Invalid loop point.")
            return

        # Extract signed 8-bit PCM.
        signed_data = self.rom[data_offset:data_end]

        # WAV PCM 8-bit is unsigned.
        wav_data = bytes(
            (value + 128) & 0xFF
            for value in signed_data
        )

        filename = (
            f"instrument_{instrument_index:03d}_"
            f"{wave_offset:08X}.wav"
        )

        output_path = os.path.join(
            self.output_dir,
            filename
        )

        with wave.open(output_path, "wb") as wav:

            wav.setnchannels(1)
            wav.setsampwidth(1)
            wav.setframerate(frequency)
            wav.writeframes(wav_data)

        sample_info = {
            "instrument": instrument_index,
            "voice_type": voice_type,
            "rom_offset": hex(wave_offset),
            "sample_data_offset": hex(data_offset),
            "frequency": frequency,
            "loop_start": loop_start,
            "size": size,
            "wave_type": wave_type,
            "status": status,
            "file": filename
        }

        self.report["samples"].append(sample_info)

        print(f"[Success] Extracted: {filename}")
        print(f"  Sample Rate: {frequency} Hz")
        print(f"  Sample Size: {size} bytes")
        print(f"  Loop Start: {loop_start}")

    # ======================================
    # EXPORT REPORT
    # ======================================

    def export_report(self):

        report_path = os.path.join(
            self.output_dir,
            "gba_audio_report.json"
        )

        with open(
            report_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.report,
                file,
                indent=4
            )

        print(f"\n[Success] Report saved: {report_path}")

    # ======================================
    # MAIN EXTRACTION
    # ======================================

    def extract(self, song_offset=None, voicegroup_offset=None):

        print("\n=== GBA Audio Parsing and Extraction ===")

        self.load_rom()

        if song_offset is not None:

            print("[Info] Parsing song header...")

            voicegroup_offset = self.parse_song_header(
                song_offset
            )

        if voicegroup_offset is None:

            raise ValueError(
                "Provide a verified song header or voice group offset."
            )

        print("[Info] Starting instrument parsing...")

        self.parse_voicegroup(voicegroup_offset)

        print("\n=== Extraction Summary ===")

        print(
            f"Instruments parsed: "
            f"{len(self.report['instruments'])}"
        )

        print(
            f"Samples extracted: "
            f"{len(self.report['samples'])}"
        )

        self.export_report()

        return len(self.report["samples"]) > 0

if __name__ == "__main__":

    rom_path = input(
        "Enter GBA ROM path: "
    ).strip().strip('"')

    try:

        extractor = GBAAudioExtractor(rom_path)

        print("\nSelect input type:")
        print("1. Song header ROM offset")
        print("2. Voice group ROM offset")

        choice = input("Choice: ").strip()

        if choice == "1":

            value = input(
                "Enter song header offset (hex): "
            ).strip()

            extractor.extract(
                song_offset=int(value, 0)
            )

        elif choice == "2":

            value = input(
                "Enter voice group offset (hex): "
            ).strip()

            extractor.extract(
                voicegroup_offset=int(value, 0)
            )

        else:
            print("[Error] Invalid selection.")

    except (OSError, ValueError) as error:

        print(f"[Error] {error}")

    input("\nPress Enter to exit...")

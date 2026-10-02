Architectural Drivers
| Driver | Catagory | Description | 
|---|---|---|
|Availability|Quality| System must be/remain available 99% of the time|
|File Data Access| Functional | The tool must decode ROM files and find samples|
|The User Interaction|Functional| A user can listen, edit, and choose what to export as a SoundFont.|
|Conversion| Functional | Converts the extracted ROM samples into a compiled SoundFont file that can be exported|

Weighted Evaluation
| Evaluation Criteria |  Why it matters | Weight | Option A | Option B | 
|---|---|---|---|---|
|Program| Supports required functions and adjacencies. |25%|---|---|
|Data Storage| Allows the tool to be able to go through data imported by ROMs | 15% | --- | --- |
|User Response | Responds to ROM imports, acts of conversion, and exports. |10%|---|---|

Seam Inventory
| Seam |  What has to work | Crossed it before? | Risk |
| --- |  --- | --- | --- |
| App to ROM File |  Extracting WAV/audio samples from a ROM file. | Yes | Medium |
| Samples to Extractor |  Must be able to organize the audio into a hierarchy | No | High |
| ROM to Tool |  Map out the samples as Instruments, based of the type, regions, and key range. | No | Medium |
| Insturment Builder to SoundFont Builder |  Making of the Pitch/Key Mapping for the samples. Create correct MIDI mapping | Yes | Medium |
| SF2 Generation to SF2 Builder |  Construct the SoundFont | No | Medium |
| Tool to Output |  Write and export the final data. | Yes | Low |

Novelty Load

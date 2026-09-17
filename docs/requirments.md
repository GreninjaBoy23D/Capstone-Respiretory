# Software Requirements Specification — Kevin Xiong

**Author:** Kevin Xiong  **Version:** 1.0  **Date:** <2026-09-09>
**Status:** Draft 
---

## 1. Purpose and Scope

This application lets users extract a game's ROM file and convert their instruments into a packaged SoundFont (SF2) format. For musical composers wanting to use instruments from their favorite video games, this tool is a great way to get the instruments they like. It benefits composers and saves time through its compatibility with various ROM types, such as DS, PlayStation, Game Boy Advance, and more, requiring just one tool to get multiple soundfonts from different ROM's.

The current version of the tool only supports users who are on laptop and PC. There are no plans for a Mobile (Andriod and/or IOS) version for the time being. This tool was made for Laptop and PC users in mind, a mobile version would be implemented in a later version.

## 2. Stakeholders and Personas

| Persona | Who they are | What they need from the system | Evidence they exist |
|---|---|---|---|
| Name: Kevin Xiong, Age: 21, Role: Organizer | The person who created the tool, testing to see if the converter works. | I would like to see if my tool can be able to easily extract and convert a game ROM into a Soundfont. | I am the creator of the project who is activally learning how to extract soundfonts, such as GBA. |
| Name: Derek, Age: Around over 18, Role: User | Derek is a new, upcoming game composer who wants to use a video game soundfont in their music. | A way to get a raw soundfont by using a ROM of an N64 game. | Composers like Tee Lopes and RESOFORCE use soundfonts from games as a part of their music. Other independent content creators make covers of songs using these soundfonts. |

Stakeholder: Kevin Xiong

## 3. Definitions

| Term | Definition in this document |
|---|---|
|Soundfont|A file format that uses sample-based synthesis to play MIDI files, commonly identified by the SF2 file extension|
|ROM|A file that contains data from a read-only memory chip, often from video game cartiriges/discs.|
|MIDI|A Musical Instrument Digital Interface, it is an interface that connects to a wide variety of digitial music for playing, editing, and recording music.|

## 4. Assumptions and Dependencies

- **Assumption:** Finding a way for the program to include a variety of ROM files designed for different consoles would be no easy task. — *If false:* It would save me much more time with the right amount of research.
- **Dependency:** My Personal Laptop for Development, Tests, and/or Updates. — *If unavailable:* I would have to use a different computer or wait until I can have access to the device to continue development or update.

## 5. Functional Requirements

<!-- Repeat this block for every requirement. Group by area. -->

The User MUST be able to Extract Instruments from ROM files by importing them from their system files to the tool.
- Given that a user opens this tool, when a user imports a game ROM from their files into it, then the tool detects the type of ROM and extracts instrument samples from it.
- Given the compatibility list of ROM types (based on consoles like GBA, DS, CPS, PS1, etc) for this tool, when tries to import a ROM from outside the list of compatible formats, then the tool will get an error message saying that the ROM file is not compatible.
- **Source:** My Own Decision

The Tool MUST be able to understand the data location of a ROM when the user imports the file into the tool.
- Given that the tool imports the ROM file, when the tool finds the data necessary for the SoundFont, then the tool will be able to use that data to make the SoundFont.
- Given the programming and no clear direction for the tool, when it tries to look for the data, the tool cannot make the SoundFont at all due to the data not being detected.
- **Source:** My Own Decision


The Tool MUST be able to Map Instruments from the Samples when it finds the data for them so that they can be implemented with a MIDI key-ranged instrument.
- Given that the tool has access to the samples, when the tool can describe how the samples behave, the tool lets the samples behave as instruments with MIDI key ranges.
- Given that the tool does not recognize how the samples work, when it tries to map it as an instrument, the tool cannot make the instrument for the soundfont.
- **Source:** My Own Decision

In this version, The Tool Won’t be able to allow you to import multiple ROM files to create your own custom SoundFont, as it focuses on extracting instruments from one ROM file.
- **Source:** My Own Decision

The User SHOULD be able to rename an instrument from the extracted samples when clicking on an instrument and double tapping the name.
- Given that a user extracts the samples, when a user double clicks the name when selecting an instrument from the extracted samples, they should be able to change the name a sample of the instrument.
- Given that the samples were extracted without being renamed, when the user tries to export the instrument without renaming it, then when they use the soundfont, the name could not be changed afterwards. Not only that, it will make it confusing to find which instrument to use when using the soundfont.
- **Source:** My Own Decision


The User SHOULD be able to Play a preview of the instrument from the extracted samples when clicking on an instrument and hitting a PLAY Button.
- Given that a user extracts the samples, when a user clicks the play button when selecting an instrument from the extracted samples, they should be able to hear a sample of the instrument.
- Given that some samples do not work when played, when a user clicks the play button when selecting an instrument from the extracted samples, then no sound is heard when the sample is played.
- **Source:** My Own Decision


The User MUST be able to create the SoundFont file from the extracted samples by compiling them into a packaged SF2 file format.
- Given that the user is ready to convert samples into a soundfont, when a user proceeds to convert the samples, then the tool compiles them into a packaged soundfont file.
- Given that something goes wrong in the conversion of the samples to a soundfont, when a user tries to convert the samples, then an error message occurs, and the soundfont is not made due to something being wrong with the samples.
- **Source:** My Own Decision


The User MUST be able to export a SoundFont file from this Tool to their computer's file storage after converting the samples into a SoundFont.
- Given that the user converts the samples into the SoundFont, when a user’s conversion is complete, then the tool can export the SoundFont file to a file directory.
- Given that the directory for the export is not given, when a user tries to export the SoundFont without a directory, then the tool will not be able to export the soundfont.
- **Source:** My Own Decision


In this version, The Tool Won’t be able to group samples categorically (Such as Brass, Bass, Percussion, Drum Sets, ETC) when the SoundFont is made.
- **Source:** My Own Decision


The Tool SHOULD be able to have certain instruments have loops when exported as a SoundFont when using the newly made SoundFont.
- Given that the SoundFont was exported, when a user uses an instrument, certain instruments should have loops to produce longer notes.
- Given that the sample comes without loops, the audio of the note being played would be as long when playing long notes.
- **Source:** My Own Decision


The Tool SHOULD be able to Handle Errors when it fails to convert ROM's for SoundFonts while still being able to function.
- Given that the function fails without crashing, when a tool sends the error message,  the tool can allow you to try again.
- Given that if there was an error when trying to make the SoundFont, when the tool crashes due to failure, then the tool would not be seen as reliable and may be prone to crashing again.
- **Source:** My Own Decision

The Tool SHOULD be able to Log reports and data about the conversion from ROM's to Soundfonts, recording ROM information, warnings, errors, etc.
- Given that the function is complete, when a tool is used, then the tool creates a log file that lists out everything that happened for that conversion.
- Given that the function dosent have a logging system, when the tool does not have a log, then no files would be created to show it's conversion.
- **Source:** My Own Decision

## 6. Non-Functional Requirements

The Tool WON'T be able to use personal information from a user's computer software (such as an IPv4 Address and any Social Security Number) when the tool is used.
- Category: Privacy.
- **Source:** My Own Decision

The Tool SHOULD be freely usable without the need for a password or any other security protocol to access it.
- Category: Security.
- Given that the tool is open-source, when the tool starts up, then it is free to use without any use of a security measures, allowing anyone to use it more easily.
- Given that the tool requires a password, when a user doesn't remember their password, then they won't have access to the tool.
- **Source:** My Own Decision

The tool SHOULD be able to run without needing much memory or processing power on the device.
- Category: Performance.
- Given that the tool...., when the...., then.....
- Given that..., when..., then....
- **Source:** My Own Decision

The tool MUST be available to downloaded as a ZIP file from the GitHub page and can be placed anywhere within the device's file storage (such as folders like Downloads, OS, etc.).
- Category: Portability.
- Given that the tool...., when the...., then.....
- Given that..., when..., then....
- **Source:** My Own Decision

## 7. Out of Scope (the Won't-Have List)

Things a reasonable reader might expect and will not get in this release, each
with one line of reasoning. A short list here means you have not thought hard enough.

| Not building | Why not | Revisit when |
|---|---|---|
|Something that doesn't export stuff like videos or actual OST.|This tool is used specifically for extracting audio samples used as instruments for a SoundFont file.|N/A|
|A mobile app | The first version is specifically made for Laptop users.|Sometime after first Versions release|
|Notifications or use of email.|The tool does not require you to use your email, and notifications are not necessary for converting to SoundFont files.|N/A|
|Anything with a password.|Free client-based tool, no security measures needed to use it.|N/A|
|Nothing regarding a user's personal information.|Only uses files from your computer storage.|N/A|
|Needing to import other files for the converter such as Image files.|ROM files are the only input source.|N/A|
|Something that takes a long time to boot/install/set up.|To make it quick and easy to use.|N/A|
## 8. Open Questions

| # | Question | Who can answer it | Needed by |
|---|---|---|---|
|1|Have you heard about a Soundfont?|---|---|
|2|Have you used a Soundfont file before?|---|---|
|3|How hard was it to get a SoundFont from a ROM?|---|---|

## 9. Document Change Log

| Date | Version | Change | Reason |
|---|---|---|---|
| 2026-09-09 | 1.0 | Initial specification | Milestone 3 |

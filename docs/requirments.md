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

## 4. Assumptions and Dependencies

- **Assumption:** Finding a way for the program to include a variety of ROM files designed for different consoles would be no easy task. — *If false:* It would save me much more time with the right amount of research.
- **Dependency:** My Personal Laptop for Development, Tests, and/or Updates. — *If unavailable:* I would have to use a different computer or wait until I can have access to the device to continue development or update.

## 5. Functional Requirements

<!-- Repeat this block for every requirement. Group by area. -->

### FR-<AREA>-<nn> — <short imperative name>

**Priority:** Must | Should | Could | Won't (this release)
**Requirement:** <Actor> shall be able to <action> <object> <under what condition>.
**Rationale:** Why this exists, and which persona asked for it.
**Acceptance criteria:**
- Given <starting state>, when <the actor does this>, then <this observable thing is true>.
- Given <edge or failure case>, when <trigger>, then <defined behavior>.

**Source:** <interview, observation, regulation, your own decision — name it>

## 6. Non-Functional Requirements

Placeholder for Week 4. Do not write vague quality words here now; write nothing
and fill it in when you can make each one measurable.

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

## 9. Document Change Log

| Date | Version | Change | Reason |
|---|---|---|---|
| <YYYY-MM-DD> | 1.0 | Initial specification | Milestone 3 |

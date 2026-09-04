# Idea Canvas — Candidate < A >

**Candidate name:** <Aaron Xiong>
**Date started:** <2026-09-03>   **Well it came from:** < On Campus >

---

## 1. Problem statement

For Video game composers and fan-composers.
who want to use a specific soundfont for making music.
the problem is that the sound files are hidden withen the files of a ROM.
which costs the ammount of storage necesary to keep the file in.
Today there are not many workarounds for getting the soundfont files, but there are a few applications to convert the ROMS into Soundfonts.
which falls short because of the fact that there are a few applications that do convert a majority of ROM files.

## 2. Evidence a user exists

- **Person spoken to:** <AX>
- **Date and length:** <2026-09-03, minutes>
- **Three verbatim quotes:**
  1. "<I don't recall anything>"
  2. "< There would be some. >"
- **The workaround they already use:** <No, not in particular.>

## 3. Candidate scope (Must features only)

| # | Feature (one vertical slice each) | Hours |
|---|---|---:|
| 1 | The ability to choose specific instruments in the Soundfont. |1 |
| 2 |The ability to mute certain instruments or not in OST/MIDI files. |1 |
| 3 |The ability to mute voice clips from ROM's |1 |
| 4 |The ability to edit notes for a Soundfont |1 |
| 5 |The ability for fair use or simplistic labeling. |1 |
| | Walking skeleton + CI | |
| | Deployment + clean-machine test | |
| | **Construction total** | |

Budget: plan on **60 hours**, hard ceiling **75**. Above 75 you are borrowing from
testing and documentation, which are graded.

## 4. Out of scope — will NOT be built

1. Something that doesn't export stuff like videos or actual OST.
2. A mobile app, browser/laptop only.
3. Notifications or use of email.
4. Use of a device camera.
5. Anything with a password.
6. Nothing regarding a user's personal information.
7. Needing to import other files for the converter such as Image files.
8. Something that takes a long time to boot/install/set up.

## 5. Feasibility screen

| Gate | Verdict | Evidence (dated) |
|---|---|---|
| **Build** — novelty load ≤ 2 | fail | technology list, each marked new |
| **Get** — every dependency exercised for real | pass / fail | <status code, saved response, date> |
| **Ship** — a named deployment target, terms read | pass / fail | <target + pricing page read on YYYY-MM-DD> |
| **Show** — a stranger sees it work in 10 minutes | pass / fail | <the ten steps, written down> |

**Technologies:** Java (new) · C++ (new) · Python (knew)
**Novelty load:** <count of "new">

## 6. The one hard part

Using Imported Files: It takes a lot of knowledge to write code that lets you import a file. Not only that, but also having to go through a list of the compatibility of the specific ROM files as well.

## 7. Scorecard (1–5 each; weight in parentheses)

| Criterion | (w) | Score | Weighted |
|---|---:|---:|---:|
| Evidence a user exists | 3 | 3 | 3 |
| Fits ~45 hours of features | 3 | | |
| Novelty load | 2 | | |
| Dependencies verified | 2 | | |
| Demonstrable in ten minutes | 1 | | |
| **Total (max 55)** | | 3 | 3 |

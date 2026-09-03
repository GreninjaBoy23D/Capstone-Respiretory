# Idea Canvas — Candidate < C >

**Candidate name:** <Kevin Xiong>
**Date started:** <2026-09-03>   **Well it came from:** <Client>

---

## 1. Problem statement

For Composers and Music Creators.
who want to use Soundfonts from games to use as digital instruments for music.
the problem is there is no easy way to extract ROM files and convert samples to Soundfonts.
which costs time and efficency, not only to mention potential copyright issues.
Today there are some apps that are specifically made to make SoundFont's from ROM files.
which falls short because some apps require specific ROM's, instead of being able to use any ROM file with samples.

## 2. Evidence a user exists

- **Person spoken to:** <KX>
- **Date and length:** <2026-09-03>
- **Three verbatim quotes:**
  1. "Some composers use soundfonts from games to compose soundtracks for stuff like video games."
  2. "Some people use soundfonts to compose completely original tracks"
- **The workaround they already use:** < Soundfont Websites and Respiretories >

## 3. Candidate scope (Must features only)

| # | Feature (one vertical slice each) | Hours |
|---|---|---:|
| 1 | Able to take any ROM file and extract audio samples | |
| 2 | Able to automatically loop audio samples | |
| 3 | Able to compile the samples into a SounFont (or SF2) file format | |
| 4 | Able to export SounFont files into computer| |
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
| **Build** — novelty load ≤ 2 | pass / fail | <technology list, each marked known/new> |
| **Get** — every dependency exercised for real | pass / fail | <status code, saved response, date> |
| **Ship** — a named deployment target, terms read | pass / fail | <target + pricing page read on YYYY-MM-DD> |
| **Show** — a stranger sees it work in 10 minutes | pass / fail | <the ten steps, written down> |

**Technologies:** <name> (known/new) · <name> (known/new) · <name> (known/new)
**Novelty load:** <count of "new">

## 6. The one hard part

<Name exactly one. Say what makes it hard in two sentences. If you can name three,
you have three projects.>

## 7. Scorecard (1–5 each; weight in parentheses)

| Criterion | (w) | Score | Weighted |
|---|---:|---:|---:|
| Evidence a user exists | 3 | | |
| Fits ~45 hours of features | 3 | | |
| Novelty load | 2 | | |
| Dependencies verified | 2 | | |
| Demonstrable in ten minutes | 1 | | |
| **Total (max 55)** | | | |

# Scoping Decision — <Project Name>

**Author:** Kevin Xiong  ·  **Date:** <2026-09-03>  ·  **Course week:** 2

---

## 1. Problem

For Composers and Music Creators.
who want to use Soundfonts from games to use as digital instruments for music.
the problem is there is no easy way to extract ROM files and convert samples to Soundfonts.
which costs time and efficency (around no longer than 1-3 hours), not only to mention potential copyright issues.
Today there are some apps that are specifically made to make SoundFont's from ROM files.
which falls short because some apps require specific ROM's, instead of being able to use any ROM file with samples.

## 2. Evidence a user exists

Interviewed <JH/Candidate> on <2026-09-03>, <40> minutes, past-tense questions only.

- "<I could see even myself using that, I have used a plugin in GarageBand.>"
- "I could see that being useful if you want certain sounds."

## 3. Chosen scope — Must features

| # | Feature | Hours |
|---|---|---:|
| 1 | Getting the soundfont by ROM file conversion | |
| 2 | Being able to use the soundfont file under fair use. (Could possibly die in Week 8 if falling behind)| |
| 3 | Using the Soundfont files for certain sounds. (Could possibly die in Week 8 if falling behind)| |
| | **Feature total** | |
| | Walking skeleton + continuous integration | |
| | Deployment + clean-machine test | |
| | **Construction total** | |

Plan: 60 hours. Hard ceiling: 75. My number: <N>. The hours dependeing if on the Planned or Hard Ceiling could be a benefit to me since it could be enough or a lot of time for me to work on the project.

## 4. Should features — built only if there is room

Able to take any ROM file and extract audio samples.
Able to automatically loop audio samples (potentially cut first, or die at Week 8 if falling behind).
Able to compile the samples into a SounFont (or SF2) file format.
Able to export SounFont files to a computer.

## 5. Out of scope — will not be built

1. Something that doesn't export stuff like videos or actual OST.
2. A mobile app, browser/laptop only.
3. Notifications or use of email.
4. Use of a device camera.
5. Anything with a password.
6. Nothing regarding a user's personal information.
7. Needing to import other files for the converter such as Image files.
8. Something that takes a long time to boot/install/set up.

## 6. Accepted tradeoffs

The ability for this respiratory to be able to automatically loop samples for the finished Soundfont, a small thing that could be easy to implement. May re-implement it after initial launch.

## 7. Rejected candidates

**Rejected: Aaron Xiong.** <Which gate it failed, with the number or the quote that killed
it, and the condition for revisiting — or "closed, not deferred".>

## 8. Hour budget, reconciled

| Weeks | Phase | Hours |
|---|---|---:|
| 1–2 | Inception | 30 |
| 3–4 | Requirements | 30 |
| 5–6 | Design | 30 |
| 7 | Planning | 15 |
| 8 | Design review + midterm | 15 |
| 9–12 | Construction + verification | 60 |
| 13 | Documentation | 15 |
| 14 | Deployment + handoff | 15 |
| 15–16 | Presentation + delivery | 30 |
| | **Total** | **240** |

## 9. The one hard part

Using Imported Files: It takes a lot of knowledge to write code that lets you import a file. Not only that, but also having to go through a list of the compatibility of the specific ROM files as well.

## 10. Risks and the scope-cut trigger

| Risk | Likelihood | What it costs me | Early warning sign |
|---|---|---|---|
|Last Minute Commitment | L | M | Getting closer towards the deadline |
|Unable to find the time needed to focus on project|M|H|Noticing that not much progress have been done|
|Having to deal with knowledge beyond my level of skill|L|L|If I get stuck or confused on how to solve a problem|

**Scope-cut trigger.** If <a checkable condition> by <a real date>, I will cut.
<feature> first, then <feature>. Decided now, in advance, so I do not have to decide
it while panicking.

---

**Signed:** Kevin Xiong, <2026-09-03>
**AI use for this document:** <None>

# Idea Canvas — Candidate < B >

**Candidate name:** <Jaiden Heiner>
**Date started:** <2026-09-03>   **Well it came from:** <On-Campus>

---

## 1. Problem statement

For one that will takes ROMS and turn them into Soundfonts.
the problem is that if youre taking the sounds from a specific ROM, and converting them, it may lead to potential copyright issues, and people wouldnt be able to show thier own products if they use copyrighted sound files.
which costs A hard time selling your product if a user uses the soundfont.
Today they are able to freely use Soundfonts that were converted from ROMS.
which falls short because A lot of companies try to safeguard ROM files.

## 2. Evidence a user exists

- **Person spoken to:** <JH">
- **Date and length:** <2026-09-03, minutes>
- **Three verbatim quotes:**
  1. "<I could see even myself using that, I have used a plugin in GarageBand.>"
  2. "<It could see that being useful if you want a certain sounds.>"
- **The workaround they already use:** <GarageBand>

## 3. Candidate scope (Must features only)

| # | Feature (one vertical slice each) | Hours |
|---|---|---:|
| 1 |Getting the soundfont by ROM file conversion | |
| 2 |Being able to use the soundfont file under fair use. | |
| 3 |Using the Soundfont files for certain sounds. | |
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

**Technologies:** Java (known/new) · Python (known/new) · C++ (known/new)
**Novelty load:** <count of "new">

## 6. The one hard part

Using Imported Files: It takes a lot of knowledge to write code that lets you import a file. Not only that, but also having to go through a list of the compatibility of the specific ROM files as well.

## 7. Scorecard (1–5 each; weight in parentheses)

| Criterion | (w) | Score | Weighted |
|---|---:|---:|---:|
| Evidence a user exists | 3 | | |
| Fits ~45 hours of features | 3 | | |
| Novelty load | 2 | | |
| Dependencies verified | 2 | | |
| Demonstrable in ten minutes | 1 | | |
| **Total (max 55)** | | | |

## 8. If this candidate is rejected

<Write the rejection paragraph NOW, while you still like the idea. Name the gate it
failed, the number that killed it, and the condition under which you would revisit
it — or say plainly that it is closed, not deferred.>

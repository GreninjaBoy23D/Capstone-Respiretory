  [ ] FR-01 & FR-02  Import the ROM file and extract it samples
             → import ROM → ROM verification → locate sound samples → extract sound samples
  
  [ ] FR-05 & FR-06  edit and preview the samples
             → change name → play sample → look at details → conversion ready
  
  [ ] FR-07 & FR-08 & FR-12 Convert samples and export the SoundFont.
             → convert samples → export SF2 → log completion

**Pass 1 — Diff (mechanical).** `git diff --staged` and `git diff --staged --stat`.
Find out errors, improve or fix mistakes on coding, research and use coding experience.

**Pass 2 — Stranger (comprehension).** Read from the entry point as if you had
never seen it. Flag ambiguous names, functions doing three jobs, magic numbers,
nesting deeper than three.

**Pass 3 — Adversary (destruction).** For every input ask what the worst version
looks like:

| Input | Hostile version |
|---|---|
| ROM import | File type not supported, error importing file |
| extraction | audio parsing not formatted for ROM, ROM file uses different audio engine |
| date | today · leap day · 1900 · another time zone · deadlines  |
| network call | slow · timed out · 500 · 429 · valid HTTP, garbage body |
| collection | empty · one · one million · duplicates |

Fix now, log a defect, or accept with a written reason. All three are fine.
Silence is not.

**Pass 4 — Contract (traceability).** Read each acceptance criterion out loud and
point at the line of code that satisfies it. No line, no criterion met.

A task is DONE when ALL of the following are true:

1. Functions like how it was envisioned to.
2. Able to be run without many errors.
3. Code is clean and categorized.
4. Project is easy for users to understand.
5. Time spent on the project is utilized properly.
6. Tested, improved, and ready for users and release.
7. Able to import files, compile them, and convert them into a different format successfully.
8. Able to handle any potential errors while still being able to function.

# Definition of Done

A task is DONE when ALL of the following are true:

1. The acceptance criteria on its requirement are met, verbatim. (`FR-11 AC-__`)
2. At least one automated test exercises the new behavior and passes.
3. The full test suite passes locally AND in CI on the pushed branch.
4. Errors and edge cases named in the technical specification are handled.
5. The four-pass self-review below is complete; findings fixed or logged.
6. No secrets, credentials, or personal data appear anywhere in the diff.
7. Any assistant contribution is recorded in `docs/ai-usage.md`.
8. The issue links to its requirement id and has been moved on the board.
9. Docs touched: `README.md`, `docs/runbook.md`, or an ADR updated if this
   changed how the system is built, run, or configured.
10. Hours are logged in `docs/hours-log.csv` with a real description.

---

## The bad version, and what each line costs you

```
Definition of Done
- Code is written        <- unfalsifiable; that is what makes it a task
- It works               <- under what input? on whose machine? which criterion?
- Committed to GitHub    <- a commit proves a file changed, not that work finished
```

Nothing there can be checked by anyone but the author, which means it earns
nothing on a rubric a stranger applies.

---

## Worked example — PantryPilot, FR-12 (add an item by barcode)

| Check | Evidence |
|---|---|
| 1 | Implemented the importing ROM system in Python.|
| 2 | Tested the import system with a GBA ROM, import was a success |
| 3 | Implemented the Sample Extraction in Python. Updated Import ROM python file to use the Sample Extraction Code |
| 4 | Initial test on the sample extraction did not work. |
| 5 | Added a GBA sample extraction python file for testing purposes and to fix problems on the sample extraction. |
| 6 ||
| 7 ||
| 8 ||
| 9 ||
| 10 ||

---

## The four-pass self-review (check 5, expanded)

**Pass 1 — Diff (mechanical).** `git diff --staged` and `git diff --staged --stat`.
Hunt debug prints, commented-out blocks, files staged by accident, hard-coded
hosts, and TODOs you forgot. Five minutes; finds about half of everything.

**Pass 2 — Stranger (comprehension).** Read from the entry point as if you had
never seen it. Flag ambiguous names, functions doing three jobs, magic numbers,
nesting deeper than three.

**Pass 3 — Adversary (destruction).** For every input ask what the worst version
looks like:

| Input | Hostile version |
|---|---|
| text field | empty · 10,000 chars · emoji · `'; DROP TABLE` · padded whitespace |
| number | zero · negative · 0.1 + 0.2 · your type's maximum |
| date | today · leap day · 1900 · another time zone |
| network call | slow · timed out · 500 · 429 · valid HTTP, garbage body |
| collection | empty · one · one million · duplicates |

Fix now, log a defect, or accept with a written reason. All three are fine.
Silence is not.

**Pass 4 — Contract (traceability).** Read each acceptance criterion out loud and
point at the line of code that satisfies it. No line, no criterion met.

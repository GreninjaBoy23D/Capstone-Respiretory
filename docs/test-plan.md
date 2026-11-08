# Test Plan — GBA ROM to SoundFont

**Version:** 1.0  ·  **Author:** Kevin Xiong ·  **Date:** <2026-11-04>  ·  **Baseline commit:** <sha>

---

## 1. Scope — what is under test

[One paragraph. Name the build (commit SHA or tag) and the requirement IDs this plan
covers. Be specific: "FR-01 through FR-14 and NFR-02, NFR-05, NFR-08, at commit a1b2c3d."]
This build of the project is focused on converting GBA ROM files to a SounFont. Going off of Functional Requirements 1, 2, 3, 7, and 8, this build allows users to import a GBA ROM by putting in the file path or dragging the file into the cmd file. Then the program goes through the GBA ROM, parsing and extracting the sample audio for the Instruments. Then, users can convert the samples into a packaged SoundFont, and users can export it into a SF2 file.

## 2. Out of scope — what is NOT under test, and why

Editing and previewing the samples is not under this build, since the focus on this build is to import and extract the ROM, and convert it's samples into a SoundFont.

## 3. Test levels

| Level | What it covers here | How it runs | Roughly how many |
|---|---|---|---|
| Unit | <modules / pure logic> | `<command>` | <n> |
| Integration | <named seams: DB, HTTP client, queue> | `<command>` | <n> |
| Acceptance | <requirement acceptance criteria, end to end> | `<command or manual script>` | <n> |

## 4. Environment

| Item | Value |
|---|---|
| Runtime / language version | <exact> |
| Operating system(s) | <exact> |
| Database / storage | <exact, and how it is seeded> |
| Third-party services | <real, sandbox, or stubbed — say which> |
| Test data set | <path in repo + how it is generated> |
| Where it runs | <local + CI workflow name> |

## 5. Entry criteria — we may begin testing when

- [ ] The build under test is tagged and pushed; CI is green on the pipeline from Chapter 9.
- [ ] Every Must requirement has at least one written test case.
- [ ] The test data set is checked in and loads without manual steps.
- [ ] <your own>

## 6. Exit criteria — verification is DONE when

[Numbers, not adjectives. These are the criteria you will be held to in Week 16.]

- [ ] 100% of Must requirements have at least one passing acceptance test.
- [ ] 0 open defects at severity S1 or S2.
- [ ] Every open S3/S4 defect appears in `docs/defect-log.md` with a documented workaround.
- [ ] Every defect fixed this iteration has a named regression test that fails on the old code.
- [ ] The full suite runs from one documented command and passes in CI.
- [ ] <your own numeric target — coverage, p95 latency, accessibility check>

## 7. Risks to the testing itself

| Risk | Trigger | Response |
|---|---|---|
| <e.g. third-party sandbox unavailable> | <how you'd notice> | <stub + a manual test before release> |

## 8. Schedule

| When | What |
|---|---|
| Week 11, days 1–2 | Test plan, test case derivation, traceability matrix |
| Week 11, days 3–5 | Write and automate the suite; first full pass |
| Week 11, days 6–7 | Triage, fix S1/S2, regression tests, log |

## 9. Approval

I have read this plan and I am accountable for the exit criteria above.

Signed: <you>  ·  Date: <YYYY-MM-DD>

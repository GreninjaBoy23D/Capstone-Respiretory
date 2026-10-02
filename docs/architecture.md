# Technical Specification — ROM to SoundFont Converter

Version: v0.1   Date: 2026-10-02   Author: Kevin Xiong   Status: Draft
Requirements baseline this design satisfies: docs/requirements.md <version>

## 1. Purpose and Scope
This system is able to convert samples into a SoundFont file from a game's ROM file. It uses users' game ROM files that they import into the tool so that it can extract samples. A user can be able to edit the name of the sample and be able to play the sample in a test. The user then converts the samples into a packaged SoundFont file, which they can export onto their computer files.
In scope:      <the features this design covers, by requirement ID>
Out of scope:  <what you are deliberately not building, and why. Say it once, here.>

## 2. System Context (Level 1)
Diagram: docs/diagrams/context.<src> + context.png
| External actor / system | What it does with us | Protocol | If it is unavailable |
|---|---|---|---|

## 3. Containers (Level 2)
Diagram: docs/diagrams/containers.<src> + containers.png
| Container | Responsibility (one sentence) | Technology | Runs where | Holds secrets? |
|---|---|---|---|---|
Trust boundary: <what runs on the user's machine vs. yours; where secrets live>

## 4. Components (Level 3 — for the container with the hard part only)
| Component | Responsibility (verb first) | Owns (state) | Depends on | Serves (req IDs) |
|---|---|---|---|---|
Dependency graph is acyclic: <yes / how you broke the cycle>
Every piece of state has exactly one owner: <yes / what you fixed>

## 5. Interface Contracts
One block per interface serving a Must requirement. Eight facts each.

### <NAME>                                         (serves FR-__)
Purpose      <one line>
Auth         <who may call; what happens to who may not>
Request      <every field: type, required/optional, validation rule>
Success      <exact shape + one example>
Errors       <every failure: code, condition, body>
Idempotency  <what happens on a repeat>
Side effects <what it writes, sends, or spends>
Limits       <payload size, rate, pagination>

Error envelope used system-wide: <one shape, decided once>
Status-code policy: <what each code means in THIS system>

## 6. Data Model
### Entity: <name>                                 (serves FR-__)
Purpose        <one line: what one row IS in the real world>
  <column>  <type>  <NULL/NOT NULL>  <constraint / meaning of NULL>
Invariants     I1 ... I2 ...
Relationships  <cardinality>
Volume         <rows now, rows by Week 16>
Lifecycle      <created when; deleted how — hard/soft, cascade/restrict>

### Migrations
Mechanism      <tool, or numbered SQL applied in order + schema_migrations>
Direction      <forward-only / reversible>
Path + runner  migrations/0001-....sql, applied by <script>
Conventions    <timestamps UTC; money in minor units; enums constrained>

## 7. Sequence Flows
### Flow 1 — <the money path>                      (serves FR-__)
Numbered steps with participants and data.
| Step | What can go wrong | System behavior | User sees |
|---|---|---|---|
### Flow 2 — <the risky path: crosses a boundary you do not control>
### Flow 3 — <the failure path: Flow 2 with the boundary broken>

## 8. Error Handling and Edge Cases
| Category | Policy |
|---|---|
| Invalid input / Not authorized / Not found / Conflict / Dependency failure / Exhaustion | |

For every call that leaves this process:
| Call | Timeout (s) | Retries + backoff | Fallback | User is told? |
|---|---|---|---|---|

Edge-case register (12+ entries; these become tests in Week 11):
| # | Edge case | Expected behavior |
|---|---|---|

## 9. External and Nondeterministic Dependencies
For an AI component, the prompt contract: purpose, inputs, privacy rule, prompt
template path in this repo, model identifier + date verified, parameters, output
schema + validator, behavior on invalid output, token/latency/cost budget with a
hard cap, the non-AI fallback, and the logging + retention rule.
For any other third party: what you call, cost, limits, behavior when it is down.
| Fact | Value | Source URL | Date checked |
|---|---|---|---|

## 10. Traceability
| Requirement | Priority | Component(s) | Interface(s) | Flow |
|---|---|---|---|---|
Every Must requirement appears here. Every component appears at least once.

## 11. Open Questions and Design Risks
| # | Open question | What it blocks | Owner | Decide by |
|---|---|---|---|---|
An open question with a blocker, an owner, and a date is professional.
An unmarked hole is a landmine.

## 12. Change Log for This Document
| Version | Date | Change | Why |
|---|---|---|---|

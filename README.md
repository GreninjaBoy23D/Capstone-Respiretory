# ROM to SoundFont Converter

> For those who wish to use instruments for vaious video games for music, this is an application in which you import it's ROM file and let it convert into a SoundFont file.

**Status:** Partially working — Compatibility with other Console ROMS + Renaming and Preview Samples

**Built by:** Kevin Xiong · Capstone Project, CSC 4950

## 1. What this is and who it is for

This application allows users to import a video game ROM from thier files, and convert its extracted samples into a packaged SoundFont file. This tool can be used for those who want to use video game instruments in their digital music.

This tool is only able to import, rename, preview, and extract samples, it will not have any function when it comes to changing loop points. Since the tool focuses on extracting instrument samples, it will not focus on extracting voice clips or pre-made music from ROM files.

## 2. Demo

{{Screenshot, animated GIF, or a 60–90 second recording; for a CLI, a real terminal session. Commit the
image under `docs/img/` and use a relative path so it renders on GitHub.}}

## 3. Prerequisites

| Requirement | Version built and tested on | Check it with | What breaks without it |
|---|---|---|---|
| {{Runtime}} | {{exact version}} | `{{cmd --version}}` | {{symptom}} |
| {{Database}} | {{exact version}} | `{{cmd --version}}` | {{symptom}} |
| {{Account/key}} | n/a | see Configure | {{degraded behavior}} |

## 4. Install

```
Test Version
1. Download the ZIP.
2. Navigate through Capstone-Respiretory/docs/scripts/
3. Click on Skeleton.cmd or drag ROM file into Skeleton.cmd to import your ROM.
4. If you had just clicked on Skeleton.cmd, follow the interfaces instructions.

Canidate Version
1. Download this Project as a ZIP
2. Locate Release v0.9.0 (Canidated Release)
3. Run Skeleton.cmd
```

Expected: {{the last line of successful output, or the artifact that now exists}}.
Takes about {{N}} minutes on a first run.

## 5. Configure

```
cp .env.example .env
```

| Variable | Required? | What it is | Default |
|---|---|---|---|
| `ROM File` | yes | Find and download a compatible video game ROM file to import it to the tool. | none |
| `{{VAR}}` | no | {{plain-English meaning}} | `{{default}}` |

Never commit `.env`. Placeholder values only in this file and in `.env.example`.

## 6. Run

```
{{setup / migration command}}
{{run command}}
```

Expected: {{exact success line}} — then open {{URL}} and you should see {{what}}.

**Verify it actually works:** {{one concrete action a stranger can take — create a record, run a query —
and the result they should get. This is the difference between "it started" and "it works."}}

## 7. Test

```
{{test command}}
```

Expected: {{N}} tests, {{N}} passing, {{N}} skipped, about {{N}} seconds.
Known failing/skipped tests and why: {{list, or "none"}}.

## 8. Project layout

```
{{dir}}/     {{what lives here}}
{{dir}}/     {{...}}
docs/        specification, architecture, runbook, decision records
```

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| {{exact error text}} | {{cause}} | {{command or step}} |
| {{exact error text}} | {{cause}} | {{command or step}} |

## 10. License

{{SPDX identifier}} — see `LICENSE`.

## 11. Contact and further reading

{{How to reach you}} · Architecture: `docs/architecture.md` · Operations: `docs/runbook.md` ·
Decisions: `docs/adr/README.md` · New here? `docs/onboarding.md`

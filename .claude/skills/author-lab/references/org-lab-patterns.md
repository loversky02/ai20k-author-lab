# Patterns from VinUni-AI20k labs

Read 21 lab repos in the org (Oct 2026). This file names what to copy and where to find it; open the repo for the full text. Repo names are as listed by `gh repo list VinUni-AI20k`.

Contents: Copy these · Avoid these · Pilot → Student practice · Coach doc skeletons

## Copy these

| Pattern | Where to look |
|---|---|
| The K4 doc set: README / CHECKPOINTS / RUBRIC / RULES / SUBMISSION (+ TEAM) with a read-in-order table | K4-Track02-Day18-Lakehouse, K4-L3-Day23-AI-Product-Growth, K4-Track2-Day24-DataGovernance, K4-L3B-Day04-PromptEng-ToolCalling |
| Objectives as can-do / measured-by / pass-level | Day23 Sensor Fusion Student, README §2 |
| Checkpoint template Cần làm / Sản phẩm / Cần hiểu / Tự kiểm tra, commit `CPx:` | Day23 Sensor Fusion `CHECKPOINTS.md`; Day18 |
| Minute-budgeted checkpoints summing to the session, a spare slot, one pytest file per checkpoint | K4-Track2-Day24-DataGovernance `CHECKPOINTS.md` |
| Setup explicitly outside the clock, preflight command | Day24 README "Chuẩn bị trước buổi học" |
| "When behind" rule and sub-milestones in long steps | Day14 Robotaxi Tracking `docs/lab.md`; Day8 Annotation |
| Adequate vs Strong worked example in the rubric | Day18 `docs/RUBRIC.md` |
| Numeric deductions and per-criterion caps on judgment rows; grade reasoning, not the chosen number | Day23 AI Product Growth `RUBRIC.md` |
| Independent fail conditions ("Điều kiện trượt") | Day24 `RUBRIC.md` |
| Run validity: `provider_error_cases == 0`, all cases measured | L3B Day04 `RUBRIC.md` |
| Validator that fails on placeholders + CI + a fully worked example | Day22 Responsible AI `scripts/validate-lab.py`, `examples/hr-hiring` |
| "Validator pass is necessary, not points" | Day22 `docs/rubric.md` |
| Hidden test categories published, cases hidden; hard cap for leaks | Day04 AgentTriage README / BRIEF |
| Public scorer, frozen directory hashed, "reading the scorer is not cheating" | Day16 AgentArena Student README §3, §8 |
| TEAM.md with per-member INDIVIDUAL block; every member submits the same URL | L3B Day04 `TEAM.md`, `SUBMISSION.md` |
| Checkbox-style rubric rows with counts + TA 2-minute verify list per checkpoint | Hackathon 3A `04-rubric.md` |
| "Do not fork — data/ would go public" | Hackathon 3A README "Nộp bài" |
| Precise late rule: default deadline, who may change it, which timestamp counts, −10, no force-push, oral check | Day23 Sensor Fusion `RULES.md` |
| Self-check that says it is not grading and prints "SẴN SÀNG NỘP" | Day23 `tools/check_submission.py`; Day8 `make check-submission`; Day11 `lab11.py check` |
| Gatekeeper `make verify` for the mechanical half of the rubric | Day21 Finetuning |
| Rubric row names the trap ("most points are lost here") | Day21 Finetuning rubric 2.x |
| Screenshots numbered and mapped to rubric rows | Day21 CI/CD `nop-bai/README.md` |
| Honest caveats: tested on Python 3.11 only; asserts hardcoded; "chưa đo" | Day18 README; Day14 test matrix |
| Measured timings with date and hardware | Day21 Finetuning `docs/MEASURED-*.md` |
| Lock-before-reference (hash collected before answers ship) | Day8, Day11 |

## Avoid these

| Anti-pattern | Seen in |
|---|---|
| No rubric, no points, no deadline | Day16-Track2 Assignment; Day14 (no numeric rubric) |
| Late penalty "theo thông báo coach"; deadline "ngày lab" | Day18, Day24, L3B Day04, Day8 |
| Bonus contradictions (ungraded vs 20 points; required vs optional; cap 92 vs 100) | Day19; Hackathon README vs rubric |
| README and rubric disagree on scope (4 vs 8 notebooks) | Day19 |
| Two copies of the spec that drift (README vs BRIEF.html, different commands) | Day04 AgentTriage |
| Required path gitignored | Day18, Day24 |
| Core 80 with bands to 100 | Day21 CI/CD |
| Slide and repo durations disagree (120 vs 240) | Day8 |
| Reader-judged criteria with no anchors | Day11 |
| Template missing a section the rubric requires | Day23 AI Product Growth |
| Repo name rule in two conflicting forms | Day22 |
| 600-line step file with no minutes | Day21 CI/CD `tasks/buoc-2.md` |
| Cloud cost / account as a hidden prerequisite | Day21 CI/CD, Day16-Track2 |

## Pilot → Student practice

1. A **private pilot repo** holds `learner/` (the source of truth for the student template) and `coach/` (runbook, answer key, debrief, reference data).
2. A deterministic release script writes the Student repo and has a `--check` mode that proves the Student tree is byte-identical to `learner/` (Day8 `build/release.py`, Day11 `builder/student_repo.py`).
3. Pre-publish grep of the Student tree for weights, tokens, TODO, answers (Day11 RUNBOOK).
4. Dry runs: solo, a group of 3, a degraded branch (no key / slow network), a clean machine (Day11).
5. `PILOT_RECORD.md` with blank timing tables, filled only from real sessions — "do not fill with estimates" (Day11).
6. Student repo private until lab day, then public; learners create their own repo and submit the link.
7. After the session: `errors-seen.md` feeds the next iteration's troubleshooting table.

`lab-release` implements the release gate for this workspace; follow it rather than re-deriving the steps.

## Coach doc skeletons

Templates in `templates/coach/` follow these, taken from Day8 (`coach/DEMO_SCRIPT.md`, `coach/DEBRIEF.md`) and Day11 (`coach/RUNBOOK.md`, `PILOT_RECORD.md`):

- **RUNBOOK** — header with status label (draft / dry-run done / piloted); before-session table (task / command / done when); timeline (minute / coach says / learner does / watch for / if behind); edge-case rules with one default answer applied to everyone; do / do not (what not to reveal, and until when); spot-check (which 3 submissions to open); after-session cleanup.
- **ANSWER_KEY** — location (private only); per rubric row: expected evidence, accepted variants, plausible-but-wrong answers and their points; reference outputs with the command and seed; tolerances with measured date; disagreement log.
- **DEBRIEF** — per concept (3–6): Chỉ (what to show) / Hỏi (question to the class) / Chốt (takeaway) / Không chứng minh (what this evidence does not prove); real class numbers or a clear "ví dụ" label; 3-question anonymous form.

---
name: author-lab
description: Help a coach author the content of an ai20k lab before release — measurable objectives, an alignment table, timed practice steps with runnable checkpoints, the submission contract, a rubric graders can apply the same way twice, group roles with per-member tasks, the AI-use rule, and the coach runbook / answer key / debrief. Ships templates, a lint script and a worked example lab. Use when a coach says "soạn lab", "viết đề lab", "thiết kế bài lab", "viết rubric", "tiêu chí chấm", "checkpoint", "bài nhóm / phân vai", "review đề lab", "author a lab", "write the lab README", "design the rubric", or asks why graders disagreed on a lab. Also use to research the latest tools/models for a lab or to refresh an old lab — "research công nghệ mới cho lab", "cập nhật lab cũ", "update lab", "nâng cấp lab", "lab cũ chạy không được nữa".
---

# author-lab

Write what a lab asks learners to do, what they hand in, and how it is graded — so that a learner knows what to do and submit without asking, and two graders (human, Codex, Claude, or a script) give the same score.

Where it sits:

| Step | Skill |
|---|---|
| Folder skeleton, mock path, pinned deps, `verify` | `scaffold-lab` (run it first, or after the spec here is approved) |
| **Objectives → rubric → steps → submission → roles → coach docs** | **`author-lab` (this skill)** |
| Run the lab end to end as a learner | `lab-verifier` agent / `run-lab` |
| Cohort simulation, rankability, student/instructor split, push | `lab-release` |
| Deck frames about the lab agree with the repo | `lab-deck-cross-check` |

The coach owns every decision. You draft, check and point out gaps. **Never invent** a timing, a threshold, a dataset, a test session or a pilot result: measured numbers come from a real dry run; until then write `CHƯA ĐO` / `chưa dry run`.

## Two entry points before phase 0 → `references/research-and-refresh.md`

- **Research new tech for a lab:** ask the AI for a sourced table (version + release date, official URL, key/cost, runs on Colab/Windows/VN, licence, recent breaking changes), open every link, prefer a stable release with a zero-key path, smoke-test in a clean environment, pin `==` and record each tool in `LAB_SPEC.md` §0b. Write each fact as *đã chạy dd/mm* or *theo docs*; vendor benchmarks are never the lab's finding.
- **Refresh an old lab:** never while a cohort can still submit. Run it fresh (README in a clean env, both controls, lint), classify each failure (dependency drift, API change, retired model, dead link, runtime change, threshold drift), read what the last cohort taught (disagreement log, RUNBOOK times, troubleshooting, debrief, per-row score spread), then sort each change into **patch / content / contract** — a contract change re-runs phases 1–7. Bump the version and write *Thay đổi so với bản trước* in the README.

## The order is the method (backward design)

Write the assessment before the activities. A step that no rubric row checks is dead time; a rubric row no step teaches is a trap. Do the phases in this order and do not draft practice steps before the rubric exists.

```
Lab authoring progress:
- [ ] 0 Intake            — lab card filled; open questions listed
- [ ] 1 Objectives        — 3–5, Bloom verb + condition + pass level
- [ ] 2 Evidence & rubric — each objective → ≥1 rubric row; D/J split; formula; fail conditions
- [ ] 3 Steps             — use → modify → create; minutes; checkpoint; stuck hint; buffer
- [ ] 4 Submission        — exact paths, repo name, SHA rule, absolute deadline, late rule
- [ ] 5 Team (if group)   — roles, owned artifacts, handoffs, INDIVIDUAL block, scoring split
- [ ] 6 Rules             — AI-use level, no fabricated output, secrets, frozen files
- [ ] 7 Grader-readiness  — blank template ≈ 0, reference = full marks, lint clean
- [ ] 8 Coach docs        — RUNBOOK, ANSWER_KEY, DEBRIEF (private)
- [ ] 9 Handoff           — scaffold-lab / lab-verifier / lab-release
```

Copy this checklist into your reply and tick it as you go.

### 0 Intake

Fill `templates/LAB_SPEC.md` §0 (the lab card) from the coach's prompt, the day's deck and the slide objectives. Ask only what you cannot find: audience level, duration and what is outside the clock, individual or team (size), environment (local / Colab / cloud, keys or zero-key), grading mode (script / LLM judge / human / mix), AI-use level, deadline. Before saying a day has no lab, run `gh repo list VinUni-AI20k --limit 200 | grep -i day<NN>` — labs live off-tree.

### 1 Objectives and alignment → `references/objectives-and-alignment.md`

3–5 objectives for a 2–4 h lab (a default, not a law; warn above 5). Each row: **làm được** (observable verb + object) / **đo bằng** (artifact or command) / **mức đạt** (number or named condition). Reject *hiểu, biết, nắm được, làm quen* and rewrite. Then fill the alignment table in `LAB_SPEC.md` §2 and flag orphans both ways.

### 2 Evidence and rubric → `references/rubric-design.md`

Start from `templates/RUBRIC.md`. Rules that matter most:

- One formula line: `final = min(100, core + bonus)`. Core sums to 100 (or state it). Bands cover the same range.
- Every row has an id, points, the **exact evidence location** (path, command, notebook cell output) and a type: **D** (a script decides) or **J** (judgment). Default to D wherever a check exists.
- Every J row has Adequate vs Strong anchors, numeric deductions and a cap. "Good / clear / reasonable / đầy đủ / hợp lý" alone is not a criterion.
- Criteria are independent: say what happens downstream when step 1 fails (fixture provided, or row N is graded against it), so one mistake is not penalised twice.
- Fail conditions (fabricated output, leaked key, edited tests, wrong repo) are listed apart from the score.
- **Evidence validity** is written down: executed outputs count, screenshots do or do not replace them, run must show 0 provider errors and all cases measured.
- The floor policy is stated (none, or a number) — an unstated floor was the largest source of grader disagreement in K4.
- Self-check the anti-gaming property: a learner who copies the rubric's keywords into the template must not score.

### 3 Steps and checkpoints → `references/steps-and-checkpoints.md`

Use → modify → create, with fading support: the first step runs complete code, the middle steps have gaps, the last step is open. Each step: minutes, product (a file or output), **a runnable self-check with a pass condition**, and a stuck hint. Minutes sum to the session minus 15–25 % buffer; add a "nếu bị chậm" rule saying which step to drop. Setup goes outside the clock with a one-command preflight. Write each checkpoint with `templates/CHECKPOINTS.md` (Cần làm / Sản phẩm / Cần hiểu / Tự kiểm tra; commit message `CPx: …`).

### 4 Submission contract → `references/submission-and-evidence.md`

`templates/SUBMISSION.md`. Exact repo name pattern, public/private, exact file paths and formats, the graded commit (**last commit before the deadline**, 40-char SHA on the LMS), absolute deadline with date and timezone, numeric late rule, no force-push after the deadline, how the learner verifies their own submission. Required paths must not be in `.gitignore`. Filenames must be Windows-safe (no `: * ? " < > |`). If the repo holds two variants (AWS / GCP), say which one is graded.

### 5 Group labs → `references/group-labs.md`

`templates/TEAM.md` + `templates/CONTRIBUTIONS.md`. A role table where each member owns an artifact another member needs (positive interdependence), a per-member **INDIVIDUAL** block with that member's own raw evidence, a score split (team rows vs individual rows), what a member who did not contribute gets, and a peer-rating step with behaviour anchors. Commits are a cross-check, never the only evidence. Give each member a different input (e.g. a case set chosen by the last digit of the MSSV) so individual sections cannot be copied.

### 6 Rules

`templates/README.md` §Quy định. State the AI-use level for this lab, that the learner must be able to explain every line they submit, that AI use is declared in `REFLECTION.md`, and that fabricated results, test sessions, testers or feedback are a fail condition. Name the files learners must not edit (tests, fixed case sets, scorer) and say editing them voids the row.

### 7 Grader-readiness gates (do not skip)

These come from real K4 grading incidents — read `references/grader-pitfalls.md` once per lab.

1. **Negative control:** grade the untouched learner template with the real grader / rubric. It must score near 0. If the template already contains every keyword the grader looks for, the grader is measuring the template.
2. **Positive control:** run the reference solution *starting from the learner template* and confirm every rubric threshold is reachable (counts, row numbers, latencies). A threshold the template cannot reach costs the whole cohort.
3. **Lint:** `python3 .claude/skills/author-lab/scripts/lint_lab.py <lab-dir>` — fix every ERROR; read every WARN. It checks README sections, rubric total vs bands, objective → rubric coverage, minutes vs duration, deadline, Windows-safe names, gitignored deliverables, placeholders, vague grading words, unpinned `requirements.txt` lines and the team section.
4. Two graders (or two judge runs) grade 3–5 sample submissions; any row where they split gets a sharper anchor.

### 8 Coach docs (private)

`templates/coach/RUNBOOK.md` (minute / coach says / learner does / watch for / if behind), `ANSWER_KEY.md` (per rubric row: expected evidence, accepted variants, tolerances, disagreement log), `DEBRIEF.md` (Chỉ / Hỏi / Chốt / Không chứng minh). These never ship in the student repo; `lab-release` does the split.

### 9 Handoff

Report to the coach: the lint output, the two control results, open questions with who decides, and what is still `CHƯA ĐO`. Then `scaffold-lab` (if not yet), `lab-verifier` for an end-to-end learner run, `lab-release` before anything goes public.

## Output files

For a lab folder `DayNN-TrackX-Topic-Lab/`:

```
README.md          # learner entry point (14 sections, templates/README.md)
CHECKPOINTS.md     # per-step detail
RUBRIC.md          # the only scoring authority
SUBMISSION.md      # contract + self-verify checklist
TEAM.md            # group labs only
CONTRIBUTIONS.md   # group labs only
submission/REFLECTION.md
docs/LAB_SPEC.md   # design doc: card, objectives, alignment, decisions (may stay private)
coach/             # RUNBOOK, ANSWER_KEY, DEBRIEF, reference solution — private repo only
```

Learner-facing prose in Vietnamese; commands, filenames, rubric ids and code in English so graders match exactly. README and RUBRIC must come from one criteria table — never let them drift (Day19 README listed 4 notebooks while the rubric graded 8).

Two blank markers, never mixed: `<FILL…>` is for the coach and must be gone before release (lint ERROR); `_(điền)_` marks a cell the learner fills and ships as is — the lab's self-check should report any `_(điền)_` still present at submission.

## Worked example

`examples/judge-calibration-lab/` — a 180-minute team-of-3 lab, zero-key, stdlib only: calibrate an LLM-as-judge against human labels (accuracy, Cohen's kappa, confusion matrix, position-bias swap test). It shows every template filled in, a per-member case split, a self-check that says it is not grading, and both grader-readiness controls:

```bash
cd .claude/skills/author-lab/examples/judge-calibration-lab
python3 check.py                                   # learner self-check, blank template: CHƯA SẴN SÀNG
python3 check.py --solution coach/reference        # reference solution: SẴN SÀNG NỘP
python3 coach/grade_d.py --template                # negative control: 0/65
python3 coach/grade_d.py --solution coach/reference   # positive control: 65/65
python3 ../../scripts/lint_lab.py .                # 0 ERROR
```

Copy from it: `coach/ANSWER_KEY.md` lists measured scores for plausible-but-wrong submissions (kappa divided by n − 1 → R1 15; inverted swap check → R3 5; one-idea judge fix → R4 5), which is how the D thresholds were set. `coach/reference/` holds a full team submission (REPORT, three INDIVIDUAL files) for calibrating J rows. `docs/LAB_SPEC.md` §6 records every readiness check with its date; dry run and two-grader agreement are still marked CHƯA.

## References

| File | Read when |
|---|---|
| `references/objectives-and-alignment.md` | Phase 1 |
| `references/steps-and-checkpoints.md` | Phase 3 |
| `references/rubric-design.md` | Phase 2; any LLM-judged row |
| `references/submission-and-evidence.md` | Phase 4 |
| `references/group-labs.md` | any team lab |
| `references/grader-pitfalls.md` | Phase 7; reviewing an existing lab |
| `references/research-and-refresh.md` | choosing a new tool/model for a lab; updating an old lab |
| `references/org-lab-patterns.md` | looking for a model to copy from VinUni-AI20k repos |
| `references/sources.md` | citing why a rule exists |

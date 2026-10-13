# Research new tech · Refresh an old lab

Two entry points that come before or instead of phase 0. Both end in the normal phases: research feeds the lab card and objectives; a refresh re-enters at the first phase it touches and re-runs phase 7.

## A. Research a technology for a lab

Goal: a lab built on something that **runs on the learner's machine on the day of class**, not on what a launch post claims.

### A1 Ask the AI for a sourced table, not a summary

Prompt the research assistant (web search on) with the lab's objective and constraints, and ask for this table:

| Option | Current stable version + release date | Source (official docs / release notes / repo) | Install + minimal run | Key / cost / free tier | Runs in VN, on Colab, on Windows? | Licence | Deprecation / breaking changes in last 6 months |
|---|---|---|---|---|---|---|---|

Rules for what goes in it:

- Primary sources only for version, API and pricing facts: official docs, changelog, GitHub releases, the paper. A blog or video may point to a source; it is not one.
- Every row carries the date it was checked. A fact without a date is stale by default.
- Vendor benchmark numbers are quoted as the vendor's, never as the lab's finding.
- Open every link the AI returns. Drop the row if the link is dead or does not say what the table says.

### A2 Choose with the lab's constraints, not novelty

| Prefer | Over | Why |
|---|---|---|
| Stable release ≥ 2 weeks old with a patch release | a release from the week of class | first releases break install paths; the class becomes the bug report |
| Zero-key path (local model, mock, fixture) + optional real provider | key-only | keys, quotas and card requirements block a cohort; R rows must not depend on a provider being up |
| One new tool per lab | several | learners debug one unknown at a time |
| A tool the objective needs | a tool that is merely current | the objective decides; the tool is replaceable |

If the newest option is the point of the lab (e.g. a "what is new in X" day), say so in the lab card and keep a fallback version that is known to work.

### A3 Smoke-test before writing any step

In a clean environment (fresh venv / fresh Colab runtime), from the pinned versions:

1. Install exactly as the README will say.
2. Run the minimal example; save the real output.
3. Run it again on a second OS or Colab if learners use both.

Write each fact as **đã chạy dd/mm** (you ran it) or **theo docs** (you read it). Only "đã chạy" facts may appear as expected output in README or CHECKPOINTS.

### A4 Pin and record

- `requirements.txt` with `==` for every package the lab imports (lint warns on unpinned lines); Python version in README.
- Model names: pin the exact ID the lab was tested with and name a fallback; note the provider's retirement date if published.
- Fill the **Phiên bản & nguồn** table in `LAB_SPEC.md` §0b: tool, version, checked date, source URL, smoke-test status.

## B. Refresh an existing lab

Goal: the next cohort gets a lab that runs today, keeps what worked, and fixes what graders and learners hit last time — without changing rules under a cohort that is still submitting.

### B1 Never during an open submission window

Changing README, RUBRIC or tests while a cohort can still submit makes two cohorts graded by different rules inside one window. Refresh on a branch; release after the last deadline (including late days). A typo fix that changes no rule is the only exception — announce it.

### B2 Find what broke (run, don't read)

1. Clone the student repo fresh. Follow the README exactly in a clean environment with today's package index.
2. Run the two controls (blank template ≈ 0, reference = full marks) and `lint_lab.py`.
3. List every failure with its cause:

| Symptom | Cause class | Example |
|---|---|---|
| install fails / resolver conflict | dependency drift (unpinned or yanked) | `pip` resolves a new major version |
| `AttributeError`, renamed argument | upstream API change | SDK moved `client.chat` → `client.responses` |
| model not found / 404 | model retired | dated model ID removed by provider |
| dataset / URL 404 | source gone | link rot, dataset moved |
| Colab cell fails, local works | runtime change | Colab Python or CUDA bump |
| grader score ≠ expected on reference | threshold depended on old behaviour | latency or token counts changed |

### B3 Collect what the last cohort taught you

Read, in this order: `coach/ANSWER_KEY.md` grader-disagreement log · `coach/RUNBOOK.md` measured times and edge-case rulings · README troubleshooting rows · issues / chat questions asked more than twice · the debrief form answers · score distribution per rubric row (a row everyone fails or everyone aces measures nothing). Check every finding against `grader-pitfalls.md`.

### B4 Classify each change

| Class | Examples | What to re-run |
|---|---|---|
| **Patch** | version bump, model ID swap, dead link, typo, new troubleshooting row | smoke test, controls, lint |
| **Content** | a step rewritten, new tool, timing changed | that step's checkpoint, alignment table, controls, lint, dry run of the changed steps |
| **Contract** | objective, rubric row, points, threshold, deliverable path, deadline rule | full phases 1–7; treat as a new lab version |

A change to a threshold must come from a measurement on the refreshed reference, the same as for a new lab.

### B5 Record the version

- README top: `**Phiên bản:** vN (dd/mm/yyyy)` and a short **Thay đổi so với vN−1** list (what changed for learners, not internal edits).
- Keep the previous version's tag so a regrade of last cohort uses last cohort's rules.
- Update `LAB_SPEC.md` §0b dates and §6 readiness rows; move resolved troubleshooting rows to "đã sửa ở vN".

## AI does / coach decides

| AI drafts | Coach decides |
|---|---|
| sourced option table, install transcript, failure list with causes, diff of README vs RUBRIC, changelog draft | which tool, whether a change is patch/content/contract, any threshold, release timing |

The AI never writes "đã chạy" for something it did not run in this session, and never fills a measured time from estimates.

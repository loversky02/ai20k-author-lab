# Submission contract and evidence

The submission contract answers, without a coach: *what files, where, in which repo, by when, which commit counts, and how do I check I did it right.*

## Required fields

| Field | Rule | Model |
|---|---|---|
| Repo | Exact name pattern with all parts: `K4-<LỚP>-DAY<NN>-<HoVaTen>-<MSSV>-<Topic>`; public or private; fork or new empty repo | Day23 Sensor Fusion, Hackathon 3A |
| Fork or not | Say it. If the template holds private data, **do not fork** — create an empty repo (Hackathon: forking would publish `data/`) | Hackathon 3A |
| Files | Exact paths, formats and limits (words, pages, MB, screenshot count) | Day18 `submission/` list |
| Graded commit | "Commit cuối cùng trước hạn"; learner pastes the 40-char SHA on the LMS | Day23 RULES, Day18 SUBMISSION |
| Deadline | Absolute: `23:59 13/10/2026 (GMT+7)`. Never "cuối ngày lab", "theo coach", "theo thông báo lớp" | Day23 |
| Late rule | A number: `−10 điểm/ngày, tối đa 2 ngày, sau đó 0`. Who may announce a change and how early | Day23 (−10) |
| After deadline | No force-push; fixes go in a new commit, recorded in SUBMISSION.md, not graded unless the coach agrees | Day18 RULES |
| Channel | VLearn / LMS form; for teams, who submits (each member submits the same URL — L3B Day04) | L3B Day04 |
| Self-verify | Open the repo in a private window; run `check.py`; confirm SHA on GitHub equals SHA on LMS | Day21 CI/CD |
| Oral check | If used: when, how long, what "cannot explain" costs | Day23 (5 min, up to a week) |

## Repo hygiene rules the template must satisfy

- **No required path in `.gitignore`.** Day18 required `submission/notebooks/` while `notebooks/` was ignored; Day24 required `reports/attack-*.log` that needed `git add -f`. `lint_lab.py` checks this.
- **Windows-safe filenames** for everything the template ships *and* everything learners are told to create: no `: * ? " < > |`, no trailing dot or space, no names differing only in case. A K4 submission with `screenshots/top:free-h.png` checked out empty on Windows and the grader saw nothing.
- **One graded variant.** If the repo has `terraform/` (AWS) and `terraform-gcp/`, say which one is graded, or require a `PROVIDER.txt`. In Day16 T2 two graders picked different directories for the same learners.
- **Secrets never committed.** `.env.example` with names only; the rubric fail condition covers leaked keys.
- **Size limits** (`data/` > 20 MB = −5 in Day23) and what must not be committed (raw datasets, model weights).

## Evidence learners must produce

Prefer evidence the grader can recompute over evidence the grader must trust.

| Evidence | Strength | Notes |
|---|---|---|
| Tests / scorer the grader re-runs | strongest | pin version and seed |
| Executed notebook outputs | strong | committed with outputs; say outputs are required |
| Machine-written result files (`metrics.json`, logs) | strong if regenerable | include the command that wrote them |
| Commit history with `CPx:` messages | supporting | timeline, not quality |
| Screenshots | supporting | URL bar / terminal prompt visible; numbered and mapped to rubric rows (Day21 CI/CD `01..05-*.png`) |
| Prose report | judgment | must cite their own numbers and ids |

The template must contain every section the learner is required to fill (Day23 required a "Chưa đo được" section the template lacked), with `<!-- TODO -->` markers the self-check flags while they remain.

## Anti-copy design

- Give each learner (or each team member) **different inputs**: a case slice by the last digit of the MSSV, a seed derived from the MSSV, a different subset of failure cases to analyse.
- Ask for analysis of **their own run**: an error case they found, a number from their data, a choice they defend.
- Ask for raw evidence per member (their own log, their own notes) rather than a shared summary that can be copied between members (Day18–19 T1: identical "individual" notes across members).

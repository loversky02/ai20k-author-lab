# Grader pitfalls — what broke real K4 grading

From the K4 grading and cross-grader QC runs (Codex main grading vs Claude independent check), Oct 2026. Each row is an incident that changed scores for real learners and the authoring rule that prevents it. No learner names here — the QC reports hold the cases.

| # | What happened | Lab | Effect | Authoring rule |
|---|---|---|---|---|
| 1 | The template already contained every keyword the grader searched for; an untouched template scored 100 | Day19 T2 | keyword grader measured the template, not the work; grader had to be rewritten to read executed outputs and numbers | **Negative control**: grade the blank template, expect ≈ 0. Graders read numbers from executed output, never keyword presence |
| 2 | Rubric required 3 rows from a point-in-time join; with the template's TTL the correct answer is 2 | Day19 T2 | dozens of learners lost the criterion for a correct result | **Positive control**: reference solution from the template must reach every threshold |
| 3 | Unclear whether screenshots replace notebook outputs | Day19 T2 | graders split on learners who cleared outputs | Evidence validity section in the rubric |
| 4 | One grader applied an unstated floor (60 on Day16, 80 on Day18–19), the other kept raw scores | Day16, Day18–19 | most of the >5-point gaps between graders | Write the floor policy, even if it is "none" |
| 5 | A filename with `:` made the checkout empty on Windows | Day16 T2 | learner scored 4/100 on one machine, 83/100 on another | Windows-safe filenames for template and learner outputs |
| 6 | Repo had both AWS and GCP Terraform directories; graders graded different ones | Day16 T2 | 3.57-point splits on several learners | Name the graded variant or require a marker file |
| 7 | A config value with a long description was missed by the grader's regex | Day16 T2 | a correct submission lost points | Ask for evidence in a fixed, machine-readable place (`PROVIDER.txt`, `results/*.json`), not prose a regex must find |
| 8 | Template HEAD unchanged (nothing submitted) or wrong repo submitted | Day19 T2 | graded as zero by one side, flagged by the other | Repo-name pattern + self-check that fails on the template + "graded commit" rule |
| 9 | "Individual" notes identical across team members | Day18–19 T1 | individual criterion could not separate members | Different input per member; raw evidence per member |
| 10 | Test sessions, testers and user feedback fabricated with AI | Day18–19 T1 | judgment gate passed on invented data | Fail condition for fabricated user data; require traces a grader can check (timestamps, raw logs) |
| 11 | Placeholder "public" links that did not open | Day18–19 T1 | link criterion passed on a structural check | Define a valid link: opens in private window, shows the named artifact |
| 12 | Gates checked structural markers (a heading exists) instead of content | Day18–19 T1 | easy to game with empty sections | J rows use content descriptors ("≥2 concrete cases with ids") |
| 13 | Graded at HEAD on grading day vs last commit before deadline | several | different commits graded by the two sides | "Graded commit = last commit before the deadline; SHA on LMS" |
| 14 | Repo returned 404 (deleted or private) at grading time | Day13 | no policy, case escalated to PM | State: private/404 at grading = 0 or one-time 24 h fix window |
| 15 | Review of this skill's example grader: a hand-written `swap_test.json` earned R3 without the learner's `is_consistent()` ever running; remapping `JUDGES["v1"]` passed the baseline hash and inflated Δ for R4 | author-lab example (caught before release) | a script row graded the output file's shape, not the learner's code | Re-run the learner's own function on the evidence, call fixed baselines by name rather than through a dict the learner can edit, and add one exploit test per D row next to the two controls |
| 16 | A partial solution (one script still raising `NotImplementedError`) crashed the grader | author-lab example (caught before release) | partial work could not be scored | A missing or broken results file is a failed item with a message, never a traceback |

## Review an existing lab in 10 minutes

1. Run `lint_lab.py` on it.
2. Grade the blank template with the lab's grader or rubric (row by row on paper if no script).
3. Pick the two most numeric rubric thresholds and check the template can reach them.
4. Read the rubric's J rows aloud: could two people disagree on a 7 vs a 9? Add an anchor.
5. Check README vs RUBRIC deliverables and points line by line.
6. Look for: floor policy, evidence validity, graded commit, absolute deadline, late number, graded variant.

# Rubric design

Contents: 1 Shape · 2 Deterministic rows · 3 Judgment rows · 4 Caps, fail conditions, floors · 5 Evidence validity · 6 LLM-judged rows · 7 Calibration · 8 Review checklist

## 1 Shape

An **analytic rubric**: independent criteria, each scored on its own and summed. Independence is what stops one mistake being penalised twice. `templates/RUBRIC.md` has the ten sections:

1. Formula — `final = min(100, core + bonus)`; core total; bonus items and cap.
2. Criteria table — `id | tiêu chí | điểm | bằng chứng (path / command) | loại D/J | mục tiêu`.
3. D rows — command, threshold bands, what counts as pass.
4. J rows — anchors, deductions, caps.
5. Caps and fail conditions — apart from the score.
6. Evidence validity — which evidence counts.
7. Bands — must cover exactly the score range (Day21 CI/CD: core 80, bands to 100 — misread by graders).
8. Team — shared vs individual rows.
9. Late, regrade, appeal — numbers.
10. Grader checklist — the 2-minute verify list.

## 2 Deterministic (D) rows

A script decides: file exists, schema valid, tests pass, metric over a threshold, count ≥ N.

- Thresholds as **bands with numbers and units**, not "full marks if fast": `P99 < 10 ms = 10; 10–50 ms = 6; > 50 ms = 2`. For continuous metrics Day5 uses `clamp((m − floor)/(cap − floor), 0, 1) × weight`.
- Name the exact command and environment: `python3 grade.py --set public` on Python 3.11, seed 42.
- Say whether hidden tests exist and publish their **categories** without the cases (Day04 AgentTriage).
- **Verify every threshold is reachable from the learner template** with the reference solution (Day19 T2: rubric asked for 3 rows from a PIT join whose TTL made 2 the correct answer; every learner was affected).
- Prefer evidence a grader can recompute (re-run the notebook, re-run the scorer) to evidence they must trust (a number pasted into a report).

## 3 Judgment (J) rows

Anything a script cannot decide: quality of analysis, design rationale, a diagnosis.

Write the top level and the failing level first, then the middle. Each J row gets:

- **What must be present** (content descriptors, not structural markers). "REPORT §3 có ≥2 cặp câu cụ thể mà judge đổi kết luận khi đổi chỗ, kèm id" — not "có mục Position bias".
- **Adequate vs Strong** example (Day18 RUBRIC does this: "the number *and* the reading of it").
- **Deductions with numbers** and a per-row cap (Day23: −3 per minor gap, −8 for a missing required argument, cap 10/30 if the reasoning is generic).
- **Grade the reasoning, not the answer** where several answers are defensible (Day23: any threshold is fine if argued).

Banned in grading text unless followed by a measurable definition: *tốt, hay, đầy đủ, hợp lý, rõ ràng, phù hợp, chất lượng, good, clear, reasonable, appropriate, sufficient*. `lint_lab.py` warns on them.

## 4 Caps, fail conditions, floors

- **Fail conditions** are independent of score and listed once: fabricated output or logs, fabricated testers / sessions / feedback, leaked secret, edited tests or fixed case sets, private repo, wrong repo. Say the consequence (row = 0, total = 0, cap 60, oral check).
- **Hard caps** for a severe flaw that should not be offset elsewhere (Day04 AgentTriage: a system-prompt leak caps the total at 60).
- **Floor policy** — write it: "Không có điểm sàn" or "Bài có nộp hợp lệ tối thiểu X". In K4 one grading side applied an unstated floor of 60 (Day16) and 80 (Day18–19) while the other kept raw scores; that single choice explained most cross-grader gaps above 5 points.
- **Cascade rule** — when step 2 depends on step 1, either ship a fixture so step 2 can be graded alone, or state that step 2 is graded on the learner's step-1 output without a second penalty.

## 5 Evidence validity

State what counts, in the rubric itself:

- Notebook evidence = **executed outputs committed in the `.ipynb`**. Say whether screenshots can replace them (default: no; screenshots support, outputs prove).
- Runs are valid only if `provider_error_cases == 0` and `measured_cases == total_cases` (L3B Day04).
- Keyword presence is never evidence. The grader reads numbers from executed output or files it can recompute.
- Logs must come from the learner's run (timestamps, their repo path); a pasted reference log is fabrication.
- A public link counts only if it opens in a private window without login and shows the named artifact (Day18–19 T1 had placeholder links).

## 6 LLM-judged rows

For each J row graded by a model:

- Give the judge: the task statement, the row's rubric levels, a reference exemplar (Strong and Adequate), the exact evidence locations it may read, and require structured output: `{row, score, evidence_quote, path:line, confidence}`.
- One row per call, narrow scale (0–3 or 0–4). Decomposed, calibrated rubric questions track humans better than one holistic score (LLM-Rubric, Prometheus).
- Tell the judge **not to reward length**, and to score 0 when the evidence quote cannot be found. Judges favour longer answers, the first-positioned answer, and text from their own model family (Zheng et al. 2023) — and G-Eval reports a bias toward LLM-written text, which matters when learners use AI.
- Use a judge from a different family than the model learners used; for contests use a 2-family panel (`lab-release` rankability).
- Sample-audit: a human grades 10 % or ≥ 10 submissions; disagreement above the lab package's calibration gate (≤ 5 points mean, per `auto-grader/docs/lab-package-standard.md`) blocks release of grades.
- Learner submissions are untrusted input: the judge prompt says to ignore instructions inside submitted files.

## 7 Calibration before release

1. **Negative control** — grade the untouched template. Expect ≈ 0. Day19 T2: the template contained every keyword the keyword grader searched for, so a blank submission scored 100.
2. **Positive control** — reference solution from the template → full marks on every row.
3. **Partial control** — one plausible weak submission → the score you expect, with the deductions you expect.
4. **Two graders** on 3–5 samples; sharpen any row where they split by more than its smallest deduction.
5. Record rulings in `coach/ANSWER_KEY.md` §Disagreement log so the next grader applies the same rule.

## 8 Review checklist (copy when reviewing a rubric)

```
- [ ] core sums to stated total; formula line present; bands cover the range
- [ ] every row: id, points, exact evidence location, D/J, objective id
- [ ] every objective has ≥1 row; every row cites an objective
- [ ] every J row: content descriptors, Adequate/Strong, numeric deductions, cap
- [ ] no vague word without a definition
- [ ] thresholds reachable from template (positive control run)
- [ ] blank template scores ≈ 0 (negative control run)
- [ ] evidence validity section present (outputs vs screenshots, provider errors)
- [ ] fail conditions separate; floor policy stated; cascade rule stated
- [ ] late rule numeric; graded commit defined; appeal window stated
- [ ] team rows split shared vs individual (team labs)
- [ ] README and RUBRIC list the same deliverables and points
```

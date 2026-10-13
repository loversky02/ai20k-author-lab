# Objectives and alignment

## Write objectives as can-do / measured-by / pass-level

Every objective is one row with three cells. Copy the shape Day23 Sensor Fusion uses in its README §2 (the strongest objective table in the org).

| # | Làm được (verb + object + condition) | Đo bằng | Mức đạt |
|---|---|---|---|
| O1 | Cài đặt hàm `cohen_kappa()` từ định nghĩa, không dùng thư viện | `tests/test_metrics.py` | 6/6 test pass |
| O2 | So sánh judge với nhãn người trên 60 câu, báo accuracy + kappa | `results/metrics.json` | file có đủ 3 khoá, số khớp khi chạy lại |
| O3 | Phát hiện position bias bằng phép đổi chỗ A/B | `results/swap.json` + 1 đoạn trong `REPORT.md` | flip rate được đo và giải thích bằng ≥2 cặp cụ thể |

Rules:

- **One observable verb per row.** Use revised-Bloom verbs: cài đặt, chạy, đo, so sánh, phân tích, chẩn đoán, thiết kế, đánh giá, bảo vệ (một lựa chọn). Reject *hiểu, biết, nắm được, làm quen với, nhận thức được* — they cannot be observed. Rewrite: "hiểu kappa" → "giải thích vì sao kappa thấp hơn accuracy trên tập lệch lớp, dẫn số của nhóm".
- **Condition** says with what: data, tools, allowed AI, time, zero-key or real endpoint.
- **Pass level** is a number or a named condition a grader can check without asking you. "Đúng", "tốt", "hợp lý" are not pass levels.
- **3–5 objectives for a 2–4 h lab.** Six or more usually means two labs; say so to the coach. This is a working default, not a sourced rule.
- **Match the verb level to the time.** A 2-hour lab can reach *apply / analyse* for one technique. *Create / evaluate* needs a scaffolded earlier step.
- **Take objectives from the day's slides**, not from a generic syllabus. If the deck promises something the lab does not assess, tell the coach (see `lab-deck-cross-check`).

## The alignment table

Fill `LAB_SPEC.md` §2. Each objective must appear in at least one step and one rubric row; each rubric row must cite an objective.

| Objective | Step(s) that practise it | Rubric row(s) that assess it | Evidence |
|---|---|---|---|
| O1 | CP1 | R1 | test output |
| O2 | CP2 | R2 | `results/metrics.json` |
| O3 | CP4 | R4, R5 | `results/swap.json`, REPORT §3 |
| — | CP0 preflight | — | (setup; not graded — allowed) |

Flag in both directions:

- **Objective with no rubric row** → it will not be learned (learners study what is graded). Add a row or drop the objective.
- **Rubric row with no objective** → it grades something the lab never taught (a hidden requirement). Add the objective and a step, or drop the row.
- **Step with no rubric row** → fine only for setup, warm-up or a worked example; otherwise it is dead time.
- **Verb mismatch** → objective says *implement*, rubric only checks a screenshot of output. The check must test the verb.

`scripts/lint_lab.py` checks the first two mechanically when objectives are written `O1…` and rubric rows cite them (`O1` in the row or in a `Mục tiêu` column).

## Bonus

Bonus extends an objective (harder dataset, second endpoint, write-up in English); it never introduces a skill the core needs. State the cap and that `final = min(100, core + bonus)`.

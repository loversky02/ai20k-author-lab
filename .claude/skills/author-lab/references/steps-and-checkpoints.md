# Steps and checkpoints

## Shape of the practice: use → modify → create, with fading

| Phase | Learner does | Support | Typical share of time |
|---|---|---|---|
| Use | Runs a complete working starter or worked example; reads the output | Full code, expected output shown | 10–20 % |
| Modify | Fills gaps in given code (TODO with a test), changes a parameter and predicts the effect | Stubs + tests + hints | 40–50 % |
| Create | Builds or diagnoses something open-ended on their own data/case | Spec + rubric only | 25–35 % |

Why: novices learn more from worked examples than from solving unaided, and the same guidance hurts stronger learners — so remove support as the lab goes (worked-example effect, expertise reversal; see `sources.md`). Do not give every step the same amount of scaffolding. The create step is where the learner's own run produces evidence that is hard to outsource.

## Every step has five fields

| Field | Rule | Bad | Good |
|---|---|---|---|
| Minutes | Integer, from a dry run when one exists; else mark `ước lượng` | "khoảng 30p" | `25 (ước lượng, chưa dry run)` |
| Product | A file, a cell output, a commit | "hiểu pipeline" | `results/metrics.json` |
| Self-check | One runnable command | "kiểm tra lại code" | `python3 check.py cp2` |
| Pass when | Observable result of that command | "chạy được" | `CP2 PASS — kappa ∈ [-1, 1], n = 60` |
| Stuck hint | What to look at first, not the answer | "hỏi coach" | "Nếu kappa > accuracy: bạn đang chia cho p_o thay vì (1 − p_e)" |

Commit after each checkpoint with message `CPx: <one line>` (Day23 convention) — it gives graders a timeline and makes copied work visible.

## Time budget

- Minutes of all graded steps ≤ session minutes × 0.75–0.85. The rest is buffer for setup trouble, questions and the submission itself. Put submission (push, SHA, LMS) on the schedule as its own 10-minute row.
- Setup (install, keys, dataset download) is **outside the clock**, with a preflight command whose expected output is printed in the README (Day24 does this best).
- Add a **"nếu bị chậm"** rule: which step to skip, and what it costs in the rubric. Example: "Đến phút 120 chưa xong CP3 → bỏ CP3b (bonus), chuyển thẳng CP4."
- A single step longer than ~45 minutes needs an internal milestone (Day14 uses sub-milestones at 55/85/110).
- Minutes are measured, not guessed, before release: record actual times per step from a dry run in `coach/RUNBOOK.md`. Never fill a pilot record with estimates.
- README duration, deck duration and the sum of the step table must agree (Day8: slide said 120, repo said 240).

## Checkpoint file

`templates/CHECKPOINTS.md` per checkpoint:

```
## CP2 — Đo độ đồng thuận (25 phút)
**Cần làm:** cài đặt accuracy, cohen_kappa, confusion_matrix trong src/metrics.py; chạy scripts/evaluate.py.
**Sản phẩm:** results/metrics.json
**Cần hiểu:** vì sao kappa thấp hơn accuracy khi một nhãn chiếm 70 %.
**Tự kiểm tra:** python3 check.py cp2  →  "CP2 PASS"
**Bị kẹt?** in ra p_o và p_e trước khi tính kappa.
Commit: `CP2: metrics + evaluate`
```

## Self-check tools

A self-check tool (`check.py`, `make verify`, `lab11.py check`) is worth building for any lab with code. Rules:

- It says on its first line that it is **not grading** and that passing it means "ready to submit", not "full marks".
- It **fails on the untouched template** (otherwise learners submit the template thinking they are done).
- It checks structure, required files, schema and the deterministic rows. It never prints the answer key.
- It prints one clear final line (`SẴN SÀNG NỘP` / `CHƯA SẴN SÀNG — 2 lỗi`).
- It uses only what the learner already has installed (stdlib if possible).

## Troubleshooting table

Collect the top failures from the dry run into README §Xử lý sự cố as symptom / cause / fix. Do not invent entries; add them after each pilot from `errors-seen`.

"""Score the D rows (R1-R4) of RUBRIC.md. Coach-only; never ship in the learner repo.

    python3 coach/grade_d.py <submission-repo>        # a cloned learner repo
    python3 coach/grade_d.py --template               # negative control: untouched template, expect 0/65
    python3 coach/grade_d.py --solution coach/reference   # positive control: reference on the template, expect 65/65

The submission is untrusted: it is copied to a temp dir, the frozen tests are written over its copy,
and its judge code runs in a separate interpreter. Run it in a container or VM for a real cohort.
Kappa for R4 is computed with the coach's metrics, so a wrong cohen_kappa() costs R1 only.
J rows (R5, R6, B1) are printed as "người chấm" — read RUBRIC.md §4.
"""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check", LAB / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)
spec = importlib.util.spec_from_file_location("ref_metrics", LAB / "coach" / "reference" / "src" / "metrics.py")
ref_metrics = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref_metrics)


def kappa(root, verdicts):
    rows = check.load_jsonl(root / "data" / "answers.jsonl")
    return ref_metrics.cohen_kappa([r["human_label"] for r in rows], [verdicts[r["id"]] for r in rows])


def grade(root):
    rows, notes = {}, []
    frozen_ok = all((root / rel).is_file() and check.sha(root / rel) == h for rel, h in check.FROZEN.items()
                    if rel.startswith("data/") or rel == "scripts/run_eval.py")
    baseline_ok = check.baseline_sha(root / "src" / "judge.py") == check.BASELINE_SHA
    if not frozen_ok or not baseline_ok:
        notes.append("file cố định / judge_v1 bị sửa → R2–R4 = 0 (RUBRIC §5)")

    passed, total = check.run_tests(root, tests_file=LAB / "tests" / "test_metrics.py")
    rows["R1"] = (25 if passed == 8 else 15 if passed >= 6 else 0, f"{passed}/{total} test pass (bản tests cố định)")

    v1_ok, v1_msg, v1 = check.verify_run(root, "v1")
    v2_ok, v2_msg, v2 = check.verify_run(root, "v2")
    valid = (frozen_ok and baseline_ok) * (v1_ok + v2_ok)
    rows["R2"] = ({2: 15, 1: 7, 0: 0}[valid], f"{v1_msg} | {v2_msg}")
    if any("không khớp lần chạy lại" in m for m in (v1_msg, v2_msg)):
        notes.append("results/ có verdict khác lần chạy lại: hỏi nhóm, nếu sửa tay thì áp RUBRIC §5 (tổng = 0)")

    s_ok, s_msg, swap = check.verify_swap(root)
    if s_ok and frozen_ok and baseline_ok:
        right = [r for r in swap["rows"] if r["consistent"] == (r["original"] != r["swapped"])]
        consistency = sum(r["original"] != r["swapped"] for r in swap["rows"]) / len(swap["rows"])
        correct = len(right) == len(swap["rows"]) and abs(swap["consistency"] - round(consistency, 4)) < 1e-4
        rows["R3"] = (15 if correct else 5, s_msg + ("" if correct else " — consistency sai so với tính lại"))
    else:
        rows["R3"] = (0, s_msg)

    if valid == 2:
        k1, k2 = kappa(root, v1["verdicts"]), kappa(root, v2["verdicts"])
        d = k2 - k1
        rows["R4"] = (10 if d >= 0.10 else 5 if d > 0 else 0, f"kappa v1={k1:.3f} v2={k2:.3f} Δ={d:+.3f} (metrics của người chấm)")
    else:
        rows["R4"] = (0, "cần cả hai run hợp lệ (R2 = 15)")
    return rows, notes


def main(argv):
    if "--solution" in argv:
        root = check.overlay(argv[argv.index("--solution") + 1])
        label = "lời giải mẫu chạy từ template"
    else:
        src = LAB if "--template" in argv else Path(argv[0]).resolve()
        root = Path(tempfile.mkdtemp(prefix="judge-grade-")) / "repo"
        shutil.copytree(src, root, ignore=shutil.ignore_patterns("coach", ".git", "__pycache__"))
        label = "template chưa sửa" if "--template" in argv else str(src)
    rows, notes = grade(root)
    print(f"# Chấm tiêu chí D — {label}")
    for rid, (pts, why) in rows.items():
        print(f"{rid}  {pts:>3}  {why}")
    total = sum(p for p, _ in rows.values())
    print(f"D  {total:>3}/65")
    print("R5 (20, cá nhân), R6 (15), B1 (+5): người chấm theo RUBRIC §4")
    for n in notes:
        print("! " + n)
    print(json.dumps({rid: p for rid, (p, _) in rows.items()} | {"D_total": total}))


if __name__ == "__main__":
    main(sys.argv[1:])

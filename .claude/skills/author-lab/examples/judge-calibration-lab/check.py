"""Self-check before you submit. This is NOT grading: it tells you whether every required file is
there and whether your results reproduce. Points come from RUBRIC.md.

    python3 check.py                  # check this repo
    python3 check.py --solution DIR   # copy this repo to a temp dir, overlay DIR, run the scripts, check

Prints one line per item and ends with "SẴN SÀNG NỘP" or "CHƯA SẴN SÀNG: N mục".
"""
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parent
FROZEN = {  # sha256 of files you must not edit
    "tests/test_metrics.py": "68991d65845ceed1ccdd484878ee6a52aabe3be7f8e12d5c247a4e12e62c43aa",
    "scripts/run_eval.py": "f5aeefbf5c85f09ce139f7d8b48fbf58cb28afffdcac160f8020e9981a704a97",
    "data/answers.jsonl": "e255797db81b0d05196c3445e3a2d3436aa3107ed432aa6b396492cfef20cefd",
    "data/pairs.jsonl": "9c29cdc05af297bf733993f94e98ecc7e26f11e6f4927a25c8577d4ab686add7",
}
BASELINE_SHA = "6c4eca98304e59e6cb4e893b453c49540475d134017f4ebfcdf29d904e366972"  # judge_v1, pairwise_v1, numbers, REFUSAL_MARKERS in src/judge.py
ID_RE = re.compile(r"\ba\d{2}\b")
BLANK = "_(điền)_"  # marks a cell the learner must fill


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_sha(judge_py):
    """Hash of the fixed baseline code in src/judge.py, so v2 can change freely but v1 cannot."""
    if not judge_py.is_file():
        return None
    src = judge_py.read_text(encoding="utf-8")
    keep = {"numbers", "judge_v1", "pairwise_v1", "REFUSAL_MARKERS"}
    parts = []
    for node in ast.parse(src).body:
        name = getattr(node, "name", None) or (isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None))
        if name in keep:
            parts.append(ast.get_source_segment(src, node))
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()


def py(root, code):
    """Run code in a fresh interpreter rooted at root (isolated from this process's imports)."""
    r = subprocess.run([sys.executable, "-I", "-c", "import sys; sys.path.insert(0, '.')\n" + code],
                       cwd=root, capture_output=True, text=True, timeout=120)
    if r.returncode:
        raise RuntimeError(r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "failed")
    return json.loads(r.stdout)


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def read_json(path, keys):
    """(obj, error) — a results file that is not JSON or lacks a key is a failed item, not a crash."""
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        return None, f"{path.name}: không đọc được JSON ({e.__class__.__name__})"
    missing = [k for k in keys if not isinstance(obj, dict) or k not in obj]
    return (None, f"{path.name}: thiếu trường {missing}") if missing else (obj, None)


def run_tests(root, tests_file=None):
    """(passed, total) for the metrics tests; tests_file overrides the repo's copy (graders use the frozen one)."""
    if tests_file:
        shutil.copy(tests_file, root / "tests" / "test_metrics.py")
    r = subprocess.run([sys.executable, "-m", "unittest", "-v", "tests.test_metrics"], cwd=root,
                       capture_output=True, text=True, timeout=120)
    out = r.stdout + r.stderr
    total = re.search(r"Ran (\d+) test", out)
    return len(re.findall(r" \.\.\. ok$", out, re.M)), int(total.group(1)) if total else 0


def recompute_verdicts(root, judge):
    # v1 goes through the hashed judge_v1 itself, so remapping JUDGES["v1"] makes the run file not reproduce
    fn = "judge_v1" if judge == "v1" else f"JUDGES['{judge}']"
    return py(root, f"""import json
from src.judge import JUDGES, judge_v1
rows = [json.loads(l) for l in open('data/answers.jsonl', encoding='utf-8') if l.strip()]
print(json.dumps({{r['id']: {fn}(r['question'], r['reference'], r['answer']) for r in rows}}))""")


def recompute_pairs(root):
    return py(root, """import json
from src.judge import pairwise_v1
rows = [json.loads(l) for l in open('data/pairs.jsonl', encoding='utf-8') if l.strip()]
print(json.dumps({p['id']: [pairwise_v1(p['question'], p['reference'], p['answer_a'], p['answer_b']),
                             pairwise_v1(p['question'], p['reference'], p['answer_b'], p['answer_a'])] for p in rows}))""")


def recompute_consistent(root, pairs):
    """Call the submission's is_consistent() on each (original, swapped); raises if it is not implemented."""
    return py(root, f"""import json, importlib.util
spec = importlib.util.spec_from_file_location('swap_test', 'scripts/swap_test.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
print(json.dumps({{k: bool(m.is_consistent(o, s)) for k, (o, s) in {json.dumps(pairs)}.items()}}))""")


def verify_run(root, judge):
    """(ok, message, run) — the committed run file reproduces when the judge is re-run on the fixed data."""
    path = root / "results" / f"judge_run_{judge}.json"
    if not path.is_file():
        return False, f"thiếu {path.relative_to(root)} — chạy `python3 scripts/run_eval.py --judge {judge}`", None
    run, err = read_json(path, ("data_sha256", "verdicts", "overall"))
    if err:
        return False, err, None
    if run.get("data_sha256") != sha(root / "data" / "answers.jsonl"):
        return False, f"{path.name}: data_sha256 không khớp data/answers.jsonl", run
    try:
        fresh = recompute_verdicts(root, judge)
    except RuntimeError as e:
        return False, f"{path.name}: không chạy lại được judge {judge}: {e}", run
    if run.get("verdicts") != fresh:
        diff = sorted(k for k in fresh if run.get("verdicts", {}).get(k) != fresh[k])
        return False, f"{path.name}: verdict không khớp lần chạy lại ({len(diff)} id, vd {diff[:3]}) — chạy lại script rồi commit", run
    rows = load_jsonl(root / "data" / "answers.jsonl")
    acc = sum(fresh[r["id"]] == r["human_label"] for r in rows) / len(rows)
    if abs((run["overall"] or {}).get("accuracy", -1) - round(acc, 4)) > 1e-4:
        return False, f"{path.name}: accuracy trong file khác accuracy tính lại", run
    return True, f"{path.name}: tái lập được, n={len(rows)}, accuracy={acc:.3f}", run


def verify_swap(root):
    path = root / "results" / "swap_test.json"
    if not path.is_file():
        return False, "thiếu results/swap_test.json — chạy `python3 scripts/swap_test.py`", None
    out, err = read_json(path, ("data_sha256", "n_pairs", "consistency", "inconsistent_ids", "rows"))
    if err:
        return False, err, None
    if out.get("data_sha256") != sha(root / "data" / "pairs.jsonl"):
        return False, "swap_test.json: data_sha256 không khớp data/pairs.jsonl", out
    try:
        fresh = recompute_pairs(root)
    except RuntimeError as e:
        return False, f"swap_test.json: không chạy lại được pairwise_v1: {e}", out
    rows = out["rows"] if isinstance(out["rows"], list) else []
    if {r.get("id"): [r.get("original"), r.get("swapped")] for r in rows} != fresh:
        return False, "swap_test.json: verdict không khớp lần chạy lại", out
    try:
        flags = recompute_consistent(root, fresh)
    except RuntimeError as e:
        return False, f"swap_test.json: không gọi được is_consistent() trong scripts/swap_test.py: {e}", out
    if {r["id"]: r.get("consistent") for r in rows} != flags:
        return False, "swap_test.json: cột consistent không khớp is_consistent() của bạn — chạy lại script rồi commit", out
    return True, f"swap_test.json: tái lập được, n_pairs={out['n_pairs']}, consistency={out['consistency']:.3f}", out


def individual_files(root):
    d = root / "submission" / "INDIVIDUAL"
    return sorted(p for p in d.glob("*.md") if not p.name.startswith("_")) if d.is_dir() else []


def check_individual(path, run_v1, rows):
    text = path.read_text(encoding="utf-8")
    m = re.search(r"^Slice:\s*([ABC])\b", text, re.M)
    if not m:
        return False, f"{path.name}: thiếu dòng `Slice: A|B|C`"
    s = m.group(1)
    wrong = {d["id"] for d in (run_v1 or {}).get("disagreements", []) if d["slice"] == s}
    cited = set(ID_RE.findall(text))
    ok_ids = cited & wrong
    if len(ok_ids) < 3:
        return False, f"{path.name}: cần ≥3 id judge v1 sai thuộc slice {s}; đang có {len(ok_ids)} ({sorted(ok_ids)})"
    if not re.search(r"(?im)^##\s*dùng ai", text) or BLANK in text:
        return False, f"{path.name}: thiếu mục `## Dùng AI` hoặc còn {BLANK}"
    return True, f"{path.name}: slice {s}, {len(ok_ids)} id lỗi hợp lệ"


def check_report(root, runs, swap):
    p = root / "submission" / "REPORT.md"
    if not p.is_file():
        return False, "thiếu submission/REPORT.md"
    text = p.read_text(encoding="utf-8")
    if BLANK in text:
        return False, f"REPORT.md còn {BLANK}"
    need = []
    for j in ("v1", "v2"):
        k = (runs.get(j) or {}).get("overall", {}).get("kappa")
        if k is None:
            return False, f"judge_run_{j}.json chưa có kappa — làm xong CP2 rồi chạy lại"
        need.append(f"{k:.2f}")
    if swap:
        need.append(f"{swap['consistency']:.2f}")
    missing = [n for n in need if n not in text]
    if missing:
        return False, f"REPORT.md không có số đo của bạn: {missing} (kappa v1, kappa v2, consistency, 2 chữ số thập phân)"
    return True, "REPORT.md có đủ số đo khớp results/"


def check(root):
    items = []
    for rel, h in FROZEN.items():
        p = root / rel
        items.append((p.is_file() and sha(p) == h, f"file cố định không đổi: {rel}"))
    items.append((baseline_sha(root / "src" / "judge.py") == BASELINE_SHA, "judge_v1 / pairwise_v1 không đổi"))
    passed, total = run_tests(root)
    items.append((passed == total == 8, f"tests: {passed}/{total} pass (`python3 -m unittest tests.test_metrics -v`)"))
    runs = {}
    for j in ("v1", "v2"):
        ok, msg, run = verify_run(root, j)
        runs[j] = run if ok else None
        items.append((ok, msg))
    ok, msg, swap = verify_swap(root)
    items.append((ok, msg))
    if swap and ok:
        items.append((swap["consistency"] < 1.0 and swap["inconsistent_ids"], "swap test tìm thấy cặp không nhất quán (is_consistent đã cài?)"))
    rows = load_jsonl(root / "data" / "answers.jsonl")
    inds = individual_files(root)
    items.append((len(inds) >= 1, f"submission/INDIVIDUAL/: {len(inds)} file thành viên"))
    for p in inds:
        items.append(check_individual(p, runs.get("v1"), rows))
    items.append(check_report(root, runs, swap))
    for name in ("TEAM.md", "CONTRIBUTIONS.md"):
        t = (root / name).read_text(encoding="utf-8") if (root / name).is_file() else BLANK
        items.append((BLANK not in t, f"{name} đã điền (không còn {BLANK})"))
    return items


def overlay(solution):
    tmp = Path(tempfile.mkdtemp(prefix="judge-lab-"))
    shutil.copytree(LAB, tmp / "lab", ignore=shutil.ignore_patterns("coach", "results", ".git", "__pycache__"))
    root = tmp / "lab"
    shutil.copytree(Path(solution).resolve(), root, dirs_exist_ok=True)
    # a partial solution may leave a script unimplemented; the missing results/ file is then reported, not raised
    for cmd in (["scripts/run_eval.py", "--judge", "v1"], ["scripts/run_eval.py", "--judge", "v2"], ["scripts/swap_test.py"]):
        subprocess.run([sys.executable, *cmd], cwd=root, capture_output=True, timeout=120)
    return root


def main(argv):
    root = LAB
    if "--solution" in argv:
        root = overlay(argv[argv.index("--solution") + 1])
        print(f"(kiểm tra bản sao tại {root})")
    items = check(root)
    for ok, msg in items:
        print(("✓ " if ok else "✗ ") + msg)
    bad = sum(1 for ok, _ in items if not ok)
    print("SẴN SÀNG NỘP" if not bad else f"CHƯA SẴN SÀNG: {bad} mục")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

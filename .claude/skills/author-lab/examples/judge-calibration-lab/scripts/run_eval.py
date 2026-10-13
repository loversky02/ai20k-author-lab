"""Run a judge over data/answers.jsonl and write results/judge_run_<judge>.json. Do not edit.

    python3 scripts/run_eval.py --judge v1
    python3 scripts/run_eval.py --judge v2

Metrics you have not implemented yet are written as null and printed as "CHƯA CÀI (CP2)".
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src import metrics  # noqa: E402
from src.judge import JUDGES  # noqa: E402

DATA = ROOT / "data" / "answers.jsonl"


def load(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def safe(fn, *args):
    try:
        return fn(*args)
    except NotImplementedError:
        return None


def summarise(rows, verdicts):
    y_true = [r["human_label"] for r in rows]
    y_pred = [verdicts[r["id"]] for r in rows]
    kappa = safe(metrics.cohen_kappa, y_true, y_pred)
    return {"n": len(rows), "accuracy": round(metrics.accuracy(y_true, y_pred), 4),
            "kappa": None if kappa is None else round(kappa, 4),
            "confusion": safe(metrics.confusion, y_true, y_pred)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", choices=sorted(JUDGES), required=True)
    args = ap.parse_args()
    rows = load(DATA)
    judge = JUDGES[args.judge]
    verdicts = {r["id"]: judge(r["question"], r["reference"], r["answer"]) for r in rows}
    out = {
        "judge": args.judge,
        "data_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "overall": summarise(rows, verdicts),
        "by_slice": {s: summarise([r for r in rows if r["slice"] == s], verdicts) for s in "ABC"},
        "disagreements": [{"id": r["id"], "slice": r["slice"], "human": r["human_label"], "judge": verdicts[r["id"]]}
                          for r in rows if verdicts[r["id"]] != r["human_label"]],
        "verdicts": verdicts,
    }
    path = ROOT / "results" / f"judge_run_{args.judge}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    o = out["overall"]
    kappa = "CHƯA CÀI (CP2)" if o["kappa"] is None else f'{o["kappa"]:.3f}'
    print(f'judge={args.judge}  n={o["n"]}  accuracy={o["accuracy"]:.3f}  kappa={kappa}  '
          f'disagreements={len(out["disagreements"])}  -> {path.relative_to(ROOT)}')


if __name__ == "__main__":
    main()

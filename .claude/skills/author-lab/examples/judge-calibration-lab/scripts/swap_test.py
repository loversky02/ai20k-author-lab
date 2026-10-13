"""Position-bias swap test for the pairwise judge (CP3).

    python3 scripts/swap_test.py

Each pair is judged twice: (answer_a, answer_b), then swapped (answer_b, answer_a).
A judge without position bias picks the same underlying answer both times.
You implement is_consistent(); the rest is done. Writes results/swap_test.json.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.judge import pairwise_v1  # noqa: E402

DATA = ROOT / "data" / "pairs.jsonl"


def is_consistent(original, swapped):
    """original = verdict on (a, b); swapped = verdict on (b, a). Both are 'A' or 'B'.

    Return True when both verdicts point at the same underlying answer.
    """
    raise NotImplementedError("CP3: implement is_consistent()")


def main():
    with open(DATA, encoding="utf-8") as f:
        pairs = [json.loads(line) for line in f if line.strip()]
    rows = []
    for p in pairs:
        original = pairwise_v1(p["question"], p["reference"], p["answer_a"], p["answer_b"])
        swapped = pairwise_v1(p["question"], p["reference"], p["answer_b"], p["answer_a"])
        rows.append({"id": p["id"], "original": original, "swapped": swapped,
                     "consistent": is_consistent(original, swapped), "human_pref": p["human_pref"]})
    n = len(rows)
    out = {
        "data_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest(),
        "n_pairs": n,
        "consistency": round(sum(r["consistent"] for r in rows) / n, 4),
        "first_position_rate": round(sum(r["original"] == "A" for r in rows) / n, 4),
        "human_agreement": round(sum(r["original"] == r["human_pref"] for r in rows) / n, 4),
        "inconsistent_ids": [r["id"] for r in rows if not r["consistent"]],
        "rows": rows,
    }
    path = ROOT / "results" / "swap_test.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f'n_pairs={n}  consistency={out["consistency"]:.3f}  first_position_rate={out["first_position_rate"]:.3f}  '
          f'human_agreement={out["human_agreement"]:.3f}  -> {path.relative_to(ROOT)}')


if __name__ == "__main__":
    main()

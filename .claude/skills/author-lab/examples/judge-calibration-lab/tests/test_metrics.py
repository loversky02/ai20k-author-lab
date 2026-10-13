"""Frozen tests for src/metrics.py. Do not edit — editing voids rubric row R1.

    python3 -m unittest tests.test_metrics -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.metrics import cohen_kappa, confusion  # noqa: E402

P, F = "pass", "fail"


class TestConfusion(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(confusion([P, P, F, F], [P, F, F, P]),
                         {P: {P: 1, F: 1}, F: {P: 1, F: 1}})

    def test_zeros_present(self):
        self.assertEqual(confusion([P, P], [P, P]), {P: {P: 2, F: 0}, F: {P: 0, F: 0}})

    def test_total_matches_items(self):
        y_true, y_pred = [P, F, F, P, P, F, P], [P, P, F, F, P, F, P]
        c = confusion(y_true, y_pred)
        self.assertEqual(sum(sum(r.values()) for r in c.values()), len(y_true))

    def test_length_mismatch(self):
        with self.assertRaises(ValueError):
            confusion([P, F], [P])


class TestKappa(unittest.TestCase):
    def test_perfect(self):
        self.assertAlmostEqual(cohen_kappa([P, F, P, F], [P, F, P, F]), 1.0)

    def test_textbook_value(self):
        # 20 pass/pass, 5 pass/fail, 10 fail/pass, 15 fail/fail -> p_o=0.70, p_e=0.50, kappa=0.40
        y_true = [P] * 25 + [F] * 25
        y_pred = [P] * 20 + [F] * 5 + [P] * 10 + [F] * 15
        self.assertAlmostEqual(cohen_kappa(y_true, y_pred), 0.40, places=6)

    def test_constant_judge_is_zero(self):
        # a judge that always says pass agrees 75% of the time here, but adds nothing over chance
        self.assertAlmostEqual(cohen_kappa([P, P, P, F], [P, P, P, P]), 0.0)

    def test_single_label_both_sides(self):
        self.assertAlmostEqual(cohen_kappa([P, P, P], [P, P, P]), 1.0)


if __name__ == "__main__":
    unittest.main()

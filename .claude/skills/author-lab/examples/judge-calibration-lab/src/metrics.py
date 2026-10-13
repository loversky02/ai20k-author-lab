"""Agreement between a judge and human labels.

accuracy() is complete — read it first (CP1). confusion() and cohen_kappa() are yours (CP2);
tests/test_metrics.py says exactly what they must return.
"""
LABELS = ("pass", "fail")


def _check(y_true, y_pred):
    if len(y_true) != len(y_pred):
        raise ValueError(f"length mismatch: {len(y_true)} human labels, {len(y_pred)} judge labels")
    if not y_true:
        raise ValueError("no labels")


def accuracy(y_true, y_pred):
    """Fraction of items where the judge agrees with the human."""
    _check(y_true, y_pred)
    return sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)


def confusion(y_true, y_pred, labels=LABELS):
    """Counts as {human_label: {judge_label: n}} with every label present, zeros included.

    Example: confusion(["pass", "fail"], ["pass", "pass"]) ==
             {"pass": {"pass": 1, "fail": 0}, "fail": {"pass": 1, "fail": 0}}
    """
    _check(y_true, y_pred)
    raise NotImplementedError("CP2: implement confusion()")


def cohen_kappa(y_true, y_pred, labels=LABELS):
    """Cohen's kappa = (p_o - p_e) / (1 - p_e).

    p_o = observed agreement (= accuracy). p_e = chance agreement = sum over labels of
    P(human says label) * P(judge says label). If p_e == 1 (both sides always give the same
    single label) return 1.0 when p_o == 1, else 0.0.
    """
    _check(y_true, y_pred)
    raise NotImplementedError("CP2: implement cohen_kappa()")

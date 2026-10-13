"""Rule-based stand-ins for an LLM judge. Zero-key, deterministic, so every team measures the same thing.

judge_v1 and pairwise_v1 are fixed baselines — do not edit them.
judge_v2 is your team's judge (CP4): change it however you like, but it must stay deterministic
(no randomness, no network) so the grader can re-run it and get your exact verdicts.
"""
import re

REFUSAL_MARKERS = ("không có thông tin", "xin lỗi", "liên hệ bộ phận")


def numbers(text):
    """Set of numbers in text, thousands separators removed: '2.000.000đ' -> {'2000000'}."""
    return {re.sub(r"[.,]", "", m) for m in re.findall(r"\d[\d.,]*\d|\d", text)}


def judge_v1(question, reference, answer):
    """Baseline: pass if the answer repeats every number in the reference and is not a refusal."""
    if any(m in answer.lower() for m in REFUSAL_MARKERS):
        return "fail"
    ref = numbers(reference)
    return "pass" if ref and ref <= numbers(answer) else "fail"


RUDE_MARKERS = ("hỏi hoài", "đọc chính sách trên web đi", "ừ thì")
PROMISE_MARKERS = ("tặng", "tự động gia hạn", "giảm thêm")
WORD_NUMBERS = {"một tuần": "7", "nửa năm": "6"}


def words(text):
    return set(re.findall(r"\w+", text.lower()))


def judge_v2(question, reference, answer):
    """Reference judge: refusal / rude / invented promise -> fail; otherwise pass when at least half of
    the reference numbers appear (number words count), or, for a reference without numbers, when the
    answer shares enough words with it."""
    a = answer.lower()
    if any(m in a for m in REFUSAL_MARKERS + RUDE_MARKERS):
        return "fail"
    if any(m in a and m not in reference.lower() for m in PROMISE_MARKERS):
        return "fail"
    ref = numbers(reference)
    got = numbers(answer) | {v for k, v in WORD_NUMBERS.items() if k in a}
    if ref:
        return "pass" if len(ref & got) / len(ref) >= 0.5 else "fail"
    overlap = len(words(answer) & words(reference)) / max(1, len(words(reference)))
    return "pass" if overlap >= 0.3 else "fail"


def pairwise_v1(question, reference, answer_a, answer_b):
    """Which answer is better, 'A' or 'B'? Scores each with judge_v1; a tie goes to the first position."""
    va = judge_v1(question, reference, answer_a)
    vb = judge_v1(question, reference, answer_b)
    if va == vb:
        return "A"
    return "A" if va == "pass" else "B"


JUDGES = {"v1": judge_v1, "v2": judge_v2}

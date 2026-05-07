from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

from .baseline import TitlePrediction
from .dataset import TitleExample


@dataclass(frozen=True)
class Accuracy:
    correct: int
    total: int

    @property
    def value(self) -> float:
        return (self.correct / self.total) if self.total else 0.0


def _acc(pairs: list[tuple[str, str]]) -> Accuracy:
    correct = sum(1 for gold, pred in pairs if gold == pred)
    return Accuracy(correct=correct, total=len(pairs))


def compute(examples: list[TitleExample], preds: list[TitlePrediction]) -> dict:
    if len(examples) != len(preds):
        raise ValueError("examples/preds length mismatch")

    overall = {
        "canonical_title": _acc([(e.canonical_title, p.canonical_title) for e, p in zip(examples, preds)]),
        "canonical_function": _acc([(e.canonical_function, p.canonical_function) for e, p in zip(examples, preds)]),
        "canonical_seniority": _acc([(e.canonical_seniority, p.canonical_seniority) for e, p in zip(examples, preds)]),
    }

    per_lang_pairs: dict[str, dict[str, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for e, p in zip(examples, preds):
        per_lang_pairs[e.lang]["canonical_title"].append((e.canonical_title, p.canonical_title))
        per_lang_pairs[e.lang]["canonical_function"].append((e.canonical_function, p.canonical_function))
        per_lang_pairs[e.lang]["canonical_seniority"].append((e.canonical_seniority, p.canonical_seniority))

    per_lang = {}
    for lang, fields in per_lang_pairs.items():
        per_lang[lang] = {field: _acc(pairs) for field, pairs in fields.items()}

    # Error buckets: what gold titles are most commonly missed?
    missed_title = Counter()
    missed_function = Counter()
    missed_seniority = Counter()
    for e, p in zip(examples, preds):
        if e.canonical_title != p.canonical_title:
            missed_title[e.canonical_title] += 1
        if e.canonical_function != p.canonical_function:
            missed_function[e.canonical_function] += 1
        if e.canonical_seniority != p.canonical_seniority:
            missed_seniority[e.canonical_seniority] += 1

    return {
        "overall": overall,
        "per_lang": per_lang,
        "error_buckets": {
            "canonical_title": missed_title.most_common(10),
            "canonical_function": missed_function.most_common(10),
            "canonical_seniority": missed_seniority.most_common(10),
        },
    }


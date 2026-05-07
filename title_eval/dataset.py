from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class TitleExample:
    raw_title: str
    lang: str
    canonical_title: str
    canonical_function: str
    canonical_seniority: str


def load_jsonl(path: Path) -> list[TitleExample]:
    examples: list[TitleExample] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        examples.append(
            TitleExample(
                raw_title=str(row["raw_title"]).strip(),
                lang=str(row["lang"]).strip(),
                canonical_title=str(row["canonical_title"]).strip(),
                canonical_function=str(row["canonical_function"]).strip(),
                canonical_seniority=str(row["canonical_seniority"]).strip(),
            )
        )
    return examples


def iter_langs(examples: Iterable[TitleExample]) -> list[str]:
    return sorted({ex.lang for ex in examples})


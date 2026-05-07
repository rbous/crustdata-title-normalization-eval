from __future__ import annotations

import re
from dataclasses import dataclass

from .dataset import TitleExample


@dataclass(frozen=True)
class TitlePrediction:
    canonical_title: str
    canonical_function: str
    canonical_seniority: str


_NON_ALNUM = re.compile(r"[^a-z0-9+]+")


def _norm(text: str) -> str:
    return _NON_ALNUM.sub(" ", text.lower()).strip()


def _tokens(text: str) -> set[str]:
    return {t for t in _norm(text).split() if t}


def predict(example: TitleExample) -> TitlePrediction:
    """Very small heuristic baseline.

    Intentionally simple: it exists to define the evaluation surface, not to be a good model.
    """

    title = _norm(example.raw_title)
    toks = _tokens(example.raw_title)

    # Seniority
    if any(t in toks for t in ("vp", "vice", "head", "director", "dir", "chief", "cxo", "cto", "ceo", "cfo")):
        seniority = "leadership"
    elif any(t in toks for t in ("senior", "sr", "staff", "principal", "lead")):
        seniority = "senior"
    elif any(t in toks for t in ("intern", "stagiaire", "praktikant")):
        seniority = "intern"
    elif any(t in toks for t in ("junior", "jr")):
        seniority = "junior"
    else:
        seniority = "mid"

    # Function + canonical title (coarse)
    if "revops" in title or ("revenue" in toks and "operations" in toks) or ("sales" in toks and "ops" in toks):
        function = "revenue-operations"
        canonical_title = "revenue-operations-manager"
    elif "data" in toks and any(t in toks for t in ("engineer", "engineering", "ingénieur", "ingenieur")):
        function = "data"
        canonical_title = "data-engineer"
    elif any(t in toks for t in ("ml", "machine", "learning")) and any(t in toks for t in ("engineer", "engineering")):
        function = "machine-learning"
        canonical_title = "machine-learning-engineer"
    elif any(t in toks for t in ("nlp", "language", "linguist")):
        function = "machine-learning"
        canonical_title = "nlp-engineer"
    elif any(t in toks for t in ("recruiter", "talent", "sourcing", "recrutement")):
        function = "recruiting"
        canonical_title = "recruiter"
    elif any(t in toks for t in ("product", "pm")):
        function = "product"
        canonical_title = "product-manager"
    elif any(t in toks for t in ("software", "engineer", "developer", "développeur", "entwickler")):
        function = "software"
        canonical_title = "software-engineer"
    else:
        function = "other"
        canonical_title = "other"

    return TitlePrediction(
        canonical_title=canonical_title,
        canonical_function=function,
        canonical_seniority=seniority,
    )


from __future__ import annotations

import argparse
from pathlib import Path

from .baseline import predict
from .dataset import load_jsonl
from .metrics import compute
from .report import write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run title normalization eval.")
    parser.add_argument("--dataset", required=True, help="Path to JSONL dataset.")
    parser.add_argument("--out", required=True, help="Path to write JSON report.")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    out_path = Path(args.out)

    examples = load_jsonl(dataset_path)
    preds = [predict(ex) for ex in examples]
    report = compute(examples, preds)
    write_report(out_path, report)

    overall = report["overall"]
    per_lang = report["per_lang"]

    def fmt(acc) -> str:
        return f"{acc.value * 100:.1f}% ({acc.correct}/{acc.total})"

    print("== Overall ==")
    print(f"canonical_title:    {fmt(overall['canonical_title'])}")
    print(f"canonical_function: {fmt(overall['canonical_function'])}")
    print(f"canonical_seniority:{fmt(overall['canonical_seniority'])}")
    print("")
    print("== Per-language (canonical_title) ==")
    for lang in sorted(per_lang.keys()):
        print(f"{lang}: {fmt(per_lang[lang]['canonical_title'])}")
    print("")
    print(f"Wrote report: {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


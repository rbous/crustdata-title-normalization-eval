# Crustdata proof-of-work: Title normalization eval kit

This is a small, runnable evaluation harness for **mapping messy, multilingual job titles** to:

- a **canonical title**
- a **job function**
- a **seniority level**

It is intentionally dependency-free (stdlib only) so it is easy to run anywhere.

## Quickstart

From this folder:

```powershell
python -m title_eval.run --dataset data/sample_titles.jsonl --out out/report.json
```

You should see a short summary printed, and a JSON report written to `out/report.json`.

## What this is (and is not)

- ✅ A scaffold to iterate quickly: dataset → baseline → metrics → error buckets.
- ✅ A clean dataset format that can be expanded from “title only” to “title + company + snippet”.
- ✅ A place to swap in an encoder / dual-encoder / classifier head later.
- ❌ Not a production model (the baseline is deliberately simple).

## Dataset format

`data/sample_titles.jsonl` is JSONL. Each row includes:

- `raw_title` (string)
- `lang` (string, e.g. `en`, `fr`, `de`)
- `canonical_title` (string)
- `canonical_function` (string)
- `canonical_seniority` (string)

## Extending

Next iterations that map directly to the internship description:

1. Add hard negatives + near-duplicate titles per canonical label.
2. Add multilingual perturbations (translation + abbreviations).
3. Replace `baseline.py` with an encoder retrieval baseline.
4. Add a CI check for “no regression on golden set”.


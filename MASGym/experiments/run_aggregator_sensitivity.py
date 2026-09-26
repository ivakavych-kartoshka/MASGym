"""Aggregator-sensitivity check (paper RQ1).

Re-ranks the full synthetic matrix under the three aggregators discussed in
Remark 9.3 -- the product u*sigma (default), the worst-coordinate min(u,sigma),
and the weighted geometric mean u^w * sigma^(1-w) -- and reports how much the
induced ranking of configurations changes.

Motivation: Theorem 9.4 characterises u*sigma as the *unique* aggregator
satisfying the desiderata (D1)-(D4). A uniqueness theorem is only useful to a
reader if it is also robust in practice: if swapping the aggregator for a
defensible alternative reordered the configurations, the headline ranking would
be an artefact of a modelling choice. This script answers that directly.

Local and offline: it only re-reads metrics already on disk. No model, no API.
scipy is not a project dependency, so Spearman is computed as Pearson on
mid-ranks (the standard tie-corrected identity).
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
for _p in (_ROOT / "src", _ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np
import pandas as pd

from masgym.methods.aggregators import AGGREGATORS

# Remark 9.3's weighted log-linear alternative. Reported for w in a small grid
# because the ranking induced by u^w * sigma^(1-w) is not invariant to w.
WEIGHTS = (0.25, 0.5, 0.75)


def _sigma(asr: pd.Series) -> pd.Series:
    """Security level sigma = 1 - ASR_sys."""
    return 1.0 - asr


def _apply(fn, u: np.ndarray, s: np.ndarray, *extra) -> np.ndarray:
    """Aggregators in masgym.methods.aggregators are scalar-only (they call
    float() on their arguments for validation), so apply them element-wise."""
    return np.fromiter(
        (fn(float(a), float(b), *extra) for a, b in zip(u, s)),
        dtype=float,
        count=len(u),
    )


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Tie-corrected Spearman rho: Pearson correlation of mid-ranks."""
    ra = pd.Series(a).rank(method="average").to_numpy(dtype=float)
    rb = pd.Series(b).rank(method="average").to_numpy(dtype=float)
    if ra.std() == 0.0 or rb.std() == 0.0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--matrix",
        default="outputs/full_matrix/matrix_metrics.csv",
        help="per-configuration metrics CSV (default: %(default)s)",
    )
    ap.add_argument(
        "--scenarios",
        default="single_attacker,colluding,compromised_orchestrator",
        help="comma-separated attack scenarios to include; 'benign' is excluded "
        "because it is not a ranking of interest (default: %(default)s)",
    )
    ap.add_argument("--out", default="outputs/aggregator_sensitivity")
    ap.add_argument("--json-only", action="store_true")
    args = ap.parse_args()

    src = pathlib.Path(args.matrix)
    if not src.is_file():
        raise SystemExit(f"missing input: {src} (run experiments/run_full_matrix.py first)")

    df = pd.read_csv(src)
    keep = [s.strip() for s in args.scenarios.split(",") if s.strip()]
    df = df[df["scenario"].isin(keep)].copy()
    if df.empty:
        raise SystemExit(f"no rows matched scenarios={keep}")

    u = df["pna_sys"].to_numpy(dtype=float)
    s = _sigma(df["asr_sys"])

    # Baseline ranking: the product aggregator the paper reports.
    base = _apply(AGGREGATORS["product"], u, s)
    rows = []
    for name in ("min", "weighted_geometric"):
        if name == "weighted_geometric":
            for w in WEIGHTS:
                alt = _apply(AGGREGATORS[name], u, s, w)
                rows.append(
                    {
                        "aggregator": f"weighted_geometric(w={w})",
                        "spearman_vs_product": spearman(base, alt),
                        "kendall_tau_vs_product": float("nan"),
                        "top5_overlap_with_product": _top_k_overlap(base, alt, 5),
                        "n_configurations": int(len(df)),
                    }
                )
        else:
            alt = _apply(AGGREGATORS[name], u, s)
            rows.append(
                {
                    "aggregator": name,
                    "spearman_vs_product": spearman(base, alt),
                    "kendall_tau_vs_product": float("nan"),
                    "top5_overlap_with_product": _top_k_overlap(base, alt, 5),
                    "n_configurations": int(len(df)),
                }
            )

    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    out = pd.DataFrame(rows)
    out.to_csv(pathlib.Path(args.out) / "aggregator_sensitivity.csv", index=False)

    payload = {
        "check": "aggregator_sensitivity",
        "paper_rq": "RQ1",
        "product_is_default": True,
        "n_configurations": int(len(df)),
        "scenarios": keep,
        "rank_correlation": rows,
        "reading": (
            "Spearman rho near 1 means the aggregator choice does not reorder "
            "configurations, so the headline ranking is not an artefact of "
            "choosing u*sigma over defensible alternatives."
        ),
        "provenance": {
            "source": str(src),
            "synthetic": True,
            "note": "re-analysis of existing synthetic matrix; no model or API call",
        },
    }
    pathlib.Path(args.out).mkdir(parents=True, exist_ok=True)
    (pathlib.Path(args.out) / "aggregator_sensitivity.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    if not args.json_only:
        print(out.to_string(index=False))
    print(f"\nwrote {args.out}/aggregator_sensitivity.{{csv,json}}")
    return 0


def _top_k_overlap(base: np.ndarray, alt: np.ndarray, k: int) -> int:
    """How many of the k best configurations under `alt` are also in base's top k."""
    k = min(k, len(base))
    idx_b = set(np.argsort(-base)[:k].tolist())
    idx_a = set(np.argsort(-alt)[:k].tolist())
    return len(idx_b & idx_a)


if __name__ == "__main__":
    raise SystemExit(main())




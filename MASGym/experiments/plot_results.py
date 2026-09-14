"""Plot MASGym results from result CSV/JSON files (never from hard-coded numbers).

Every figure produced from the synthetic generator is stamped
"SYNTHETIC SMOKE-TEST - NOT A PAPER RESULT" so it cannot be mistaken for a paper figure.
Uses a non-interactive matplotlib backend so it runs headless on EC2.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from masgym.utils.io import ensure_dir  # noqa: E402
from masgym.utils.logging import get_logger  # noqa: E402

logger = get_logger(__name__)
_SYNTH_STAMP = "SYNTHETIC SMOKE-TEST - NOT A PAPER RESULT"


def _stamp(ax) -> None:
    ax.text(
        0.5, 0.5, _SYNTH_STAMP, transform=ax.transAxes, fontsize=13, color="red",
        alpha=0.18, ha="center", va="center", rotation=20, zorder=10,
    )


def plot_sweep(sweep_csv: str | Path, out_dir: str | Path) -> Path:
    """Bar chart of ASR_sys and NRP_sys across swept configurations."""
    out = ensure_dir(out_dir)
    df = pd.read_csv(sweep_csv)
    labels = [
        f"b={r.beta:g}{'/coll' if r.colluding else ''}{'/orch' if r.orchestrator_compromised else ''}"
        for r in df.itertuples()
    ]
    x = range(len(df))
    fig, ax = plt.subplots(figsize=(max(6, 0.7 * len(df)), 4))
    ax.bar([i - 0.2 for i in x], df["asr_sys"], width=0.4, label="ASR_sys", color="#c83f2a")
    ax.bar([i + 0.2 for i in x], df["nrp_sys"], width=0.4, label="NRP_sys", color="#1f61a4")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_ylabel("rate")
    ax.set_title("MASGym adversary sweep (synthetic)")
    ax.legend()
    _stamp(ax)
    fig.tight_layout()
    path = out / "sweep_asr_nrp.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    logger.info("wrote %s", path)
    return path


def plot_corb_pareto(corb_csv: str | Path, out_dir: str | Path) -> Path:
    """Scatter of the CoRB trajectory in (cost, ASR) with the round index as color."""
    out = ensure_dir(out_dir)
    df = pd.read_csv(corb_csv)
    fig, ax = plt.subplots(figsize=(6, 4))
    sc = ax.scatter(df["mean_tokens"], df["asr_sys"], c=df["round"], cmap="viridis", s=40)
    ax.set_xlabel("mean tokens/episode (synthetic cost proxy)")
    ax.set_ylabel("ASR_sys")
    ax.set_title("CoRB trajectory (synthetic)")
    fig.colorbar(sc, ax=ax, label="round")
    _stamp(ax)
    fig.tight_layout()
    path = out / "corb_trajectory.png"
    fig.savefig(path, dpi=130)
    plt.close(fig)
    logger.info("wrote %s", path)
    return path

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Iterable, List

import matplotlib.pyplot as plt
import pandas as pd


def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_json(path: Path | str, data: Dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def aggregate_generation_histories(histories: List[pd.DataFrame]) -> pd.DataFrame:
    if not histories:
        raise ValueError("No histories provided")
    merged = []
    for run_idx, h in enumerate(histories):
        tmp = h.copy()
        tmp["run"] = run_idx
        merged.append(tmp)
    stacked = pd.concat(merged, ignore_index=True)
    numeric_cols = stacked.select_dtypes(include="number").columns.tolist()
    if "generation" not in numeric_cols:
        raise ValueError("History must include numeric column 'generation'")
    if "run" in numeric_cols:
        numeric_cols.remove("run")
    grouped = stacked.groupby("generation")[numeric_cols].agg(["mean", "std"])
    grouped.columns = [f"{a}_{b}" for a, b in grouped.columns]
    grouped = grouped.reset_index()
    return grouped


def save_history_plot(
    agg_history: pd.DataFrame,
    y_col_mean: str,
    y_col_std: str,
    title: str,
    out_path: Path | str,
    y_label: str,
) -> None:
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    x = agg_history["generation"].to_numpy()
    y = agg_history[y_col_mean].to_numpy()
    s = agg_history[y_col_std].fillna(0.0).to_numpy()

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, linewidth=2)
    plt.fill_between(x, y - s, y + s, alpha=0.2)
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel(y_label)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(p, dpi=150)
    plt.close()


def summarize_best_of_runs(histories: Iterable[pd.DataFrame], maximize: bool = True) -> pd.DataFrame:
    rows = []
    for run_idx, h in enumerate(histories):
        if maximize:
            row = h.loc[h["best_fitness"].idxmax()]
        else:
            row = h.loc[h["best_fitness"].idxmin()]
        rows.append(
            {
                "run": run_idx,
                "best_of_run_fitness": float(row["best_fitness"]),
                "generation_of_best": int(row["generation"]),
            }
        )
    return pd.DataFrame(rows)


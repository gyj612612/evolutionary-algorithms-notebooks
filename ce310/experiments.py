from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .ga import GAConfig, run_ga
from .utils import (
    aggregate_generation_histories,
    ensure_dir,
    save_history_plot,
    summarize_best_of_runs,
    write_json,
)


def first_ideal_generation(
    history: pd.DataFrame, ideal_fitness: float, maximize: bool = True
) -> Optional[int]:
    if maximize:
        hit = history.loc[history["best_fitness"] >= ideal_fitness]
    else:
        hit = history.loc[history["best_fitness"] <= ideal_fitness]
    if hit.empty:
        return None
    return int(hit["generation"].iloc[0])


def run_condition(
    condition_name: str,
    base_config: Dict[str, Any],
    fitness_fn,
    out_dir: Path | str,
    n_runs: int = 10,
    seed_start: int = 1000,
    generation_hook=None,
    ideal_fitness: Optional[float] = None,
    maximize: bool = True,
    resume_if_exists: bool = True,
) -> Dict[str, Any]:
    condition_dir = ensure_dir(Path(out_dir) / condition_name)

    runs_summary_path = condition_dir / "runs_summary.csv"
    best_runs_path = condition_dir / "best_of_runs.csv"
    agg_path = condition_dir / "generation_aggregated.csv"
    summary_path = condition_dir / "condition_summary.json"

    if resume_if_exists and runs_summary_path.exists() and best_runs_path.exists() and agg_path.exists():
        runs_df = pd.read_csv(runs_summary_path)
        best_df = pd.read_csv(best_runs_path)
        agg = pd.read_csv(agg_path)
        if len(runs_df) == n_runs:
            if summary_path.exists():
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
            else:
                summary = {
                    "condition": condition_name,
                    "n_runs": int(len(runs_df)),
                    "best_of_run_mean": float(best_df["best_of_run_fitness"].mean()),
                    "best_of_run_std": float(best_df["best_of_run_fitness"].std()),
                    "final_best_mean": float(runs_df["final_best_fitness"].mean()),
                    "final_best_std": float(runs_df["final_best_fitness"].std()),
                }
            return {
                "condition_dir": str(condition_dir),
                "runs_df": runs_df,
                "best_df": best_df,
                "agg_df": agg,
                "summary": summary,
            }

    histories: List[pd.DataFrame] = []
    run_rows: List[Dict[str, Any]] = []

    for run in range(n_runs):
        run_seed = seed_start + run
        cfg = GAConfig(**{**base_config, "seed": run_seed, "maximize": maximize})
        result = run_ga(cfg, fitness_fn, generation_hook=generation_hook)

        run_dir = ensure_dir(condition_dir / f"run_{run:02d}")
        result.history.to_csv(run_dir / "history.csv", index=False)
        write_json(run_dir / "config.json", result.config)

        histories.append(result.history)
        row = {
            "condition": condition_name,
            "run": run,
            "seed": run_seed,
            "final_best_fitness": float(result.history.iloc[-1]["best_fitness"]),
            "final_mean_fitness": float(result.history.iloc[-1]["mean_fitness"]),
            "best_of_run_fitness": float(result.history["best_fitness"].max() if maximize else result.history["best_fitness"].min()),
        }
        if "execute_calls" in result.history.columns:
            row["total_execute_calls"] = float(result.history["execute_calls"].sum())
            row["mean_execute_calls_per_generation"] = float(result.history["execute_calls"].mean())
        if "execute_calls_nominal" in result.history.columns:
            row["total_execute_calls_nominal"] = float(result.history["execute_calls_nominal"].sum())
            row["mean_execute_calls_nominal_per_generation"] = float(
                result.history["execute_calls_nominal"].mean()
            )
        if "duplicate_ratio" in result.history.columns:
            row["mean_duplicate_ratio_per_generation"] = float(result.history["duplicate_ratio"].mean())
        if ideal_fitness is not None:
            g = first_ideal_generation(result.history, ideal_fitness=ideal_fitness, maximize=maximize)
            row["ideal_found"] = 0 if g is None else 1
            row["first_ideal_generation"] = -1 if g is None else g
        run_rows.append(row)

    runs_df = pd.DataFrame(run_rows)
    runs_df.to_csv(condition_dir / "runs_summary.csv", index=False)

    best_df = summarize_best_of_runs(histories, maximize=maximize)
    best_df.to_csv(condition_dir / "best_of_runs.csv", index=False)

    agg = aggregate_generation_histories(histories)
    agg.to_csv(condition_dir / "generation_aggregated.csv", index=False)
    save_history_plot(
        agg,
        y_col_mean="best_fitness_mean",
        y_col_std="best_fitness_std",
        title=f"{condition_name} - Best Fitness",
        out_path=condition_dir / "best_fitness_curve.png",
        y_label="Best Fitness",
    )
    save_history_plot(
        agg,
        y_col_mean="mean_fitness_mean",
        y_col_std="mean_fitness_std",
        title=f"{condition_name} - Mean Fitness",
        out_path=condition_dir / "mean_fitness_curve.png",
        y_label="Mean Fitness",
    )

    overall = {
        "condition": condition_name,
        "n_runs": int(n_runs),
        "best_of_run_mean": float(best_df["best_of_run_fitness"].mean()),
        "best_of_run_std": float(best_df["best_of_run_fitness"].std()),
        "final_best_mean": float(runs_df["final_best_fitness"].mean()),
        "final_best_std": float(runs_df["final_best_fitness"].std()),
    }
    if "mean_execute_calls_per_generation" in runs_df.columns:
        overall["mean_execute_calls_per_generation"] = float(
            runs_df["mean_execute_calls_per_generation"].mean()
        )
    if "mean_execute_calls_nominal_per_generation" in runs_df.columns:
        overall["mean_execute_calls_nominal_per_generation"] = float(
            runs_df["mean_execute_calls_nominal_per_generation"].mean()
        )
    if (
        "mean_execute_calls_per_generation" in runs_df.columns
        and "mean_execute_calls_nominal_per_generation" in runs_df.columns
    ):
        actual = float(runs_df["mean_execute_calls_per_generation"].mean())
        nominal = float(runs_df["mean_execute_calls_nominal_per_generation"].mean())
        if nominal > 0:
            overall["execute_call_reduction_ratio"] = float(1.0 - (actual / nominal))
    if "mean_duplicate_ratio_per_generation" in runs_df.columns:
        overall["mean_duplicate_ratio_per_generation"] = float(
            runs_df["mean_duplicate_ratio_per_generation"].mean()
        )
    if ideal_fitness is not None:
        ideal_found = runs_df["ideal_found"].mean()
        ideal_rows = runs_df.loc[runs_df["first_ideal_generation"] >= 0, "first_ideal_generation"]
        overall["ideal_found_fraction"] = float(ideal_found)
        overall["first_ideal_generation_mean"] = float(ideal_rows.mean()) if not ideal_rows.empty else None
    write_json(condition_dir / "condition_summary.json", overall)

    return {
        "condition_dir": str(condition_dir),
        "runs_df": runs_df,
        "best_df": best_df,
        "agg_df": agg,
        "summary": overall,
    }

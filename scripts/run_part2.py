from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import json
import matplotlib.pyplot as plt
import pandas as pd
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ce310.experiments import run_condition
from ce310.gp import make_gp_fitness_function, make_primitive_frequency_hook
from ce310.utils import ensure_dir, write_json


RESULT_ROOT = Path("results") / "part2"


def load_best_part1_params() -> Dict[str, int]:
    path = Path("results") / "part1" / "selected_part1_params.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if "best_pop_size" in data and "best_tournament_size" in data:
            return {
                "best_pop_size": int(data["best_pop_size"]),
                "best_tournament_size": int(data["best_tournament_size"]),
            }
        if "pop_size" in data and "tournament_size" in data:
            return {
                "best_pop_size": int(data["pop_size"]),
                "best_tournament_size": int(data["tournament_size"]),
            }
        return {
            "best_pop_size": 100,
            "best_tournament_size": 3,
        }
    return {"best_pop_size": 100, "best_tournament_size": 3}


def base_cfg(pop_size: int, genome_length: int, tournament_size: int) -> Dict:
    return {
        "pop_size": pop_size,
        "genome_length": genome_length,
        "generations": 50,
        "tournament_size": tournament_size,
        "p_clone": 0.2,
        "p_crossover": 0.7,
        "p_mutation_operator": 0.1,
        "p_bit_mutation": 1.0 / genome_length,
        "experiment_name": "part2",
    }


def run_encoding_comparison(
    best_pop: int,
    best_t: int,
    program_length: int,
    n_runs: int = 5,
    resume_if_exists: bool = True,
) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task5_encoding_comparison")
    rows = []
    seed_cursor = 40000
    for encoding in ["3bit", "7bit"]:
        bits_per_instr = 3 if encoding == "3bit" else 7
        genome_length = bits_per_instr * program_length
        cfg = base_cfg(pop_size=best_pop, genome_length=genome_length, tournament_size=best_t)
        for problem in ["problem1", "problem2"]:
            condition = f"{encoding}_{problem}"
            ideal = 0.0 if problem == "problem2" else None
            out = run_condition(
                condition_name=condition,
                base_config=cfg,
                fitness_fn=make_gp_fitness_function(program_length, encoding, problem),
                generation_hook=make_primitive_frequency_hook(program_length, encoding),
                out_dir=out_dir,
                n_runs=n_runs,
                seed_start=seed_cursor,
                ideal_fitness=ideal,
                maximize=True,
                resume_if_exists=resume_if_exists,
            )
            rows.append(
                {
                    "condition": condition,
                    "encoding": encoding,
                    "problem": problem,
                    **out["summary"],
                }
            )
            seed_cursor += 100
    df = pd.DataFrame(rows).sort_values(["problem", "encoding"]).reset_index(drop=True)
    df.to_csv(out_dir / "encoding_comparison_summary.csv", index=False)
    return df


def run_task7_experiments(
    program_length: int,
    encoding: str = "3bit",
    pops: List[int] | None = None,
    tournaments: List[int] | None = None,
    n_runs: int = 10,
    resume_if_exists: bool = True,
) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task7_experiments")
    rows: List[Dict] = []
    seed_cursor = 50000
    bits_per_instr = 3 if encoding == "3bit" else 7
    genome_length = bits_per_instr * program_length
    if pops is None:
        pops = [50, 100, 200]
    if tournaments is None:
        tournaments = [2, 3, 5]

    for problem in ["problem1", "problem2"]:
        for pop in pops:
            for t in tournaments:
                cfg = base_cfg(pop_size=pop, genome_length=genome_length, tournament_size=t)
                condition = f"{problem}_{encoding}_pop{pop}_t{t}"
                ideal = 0.0 if problem == "problem2" else None
                out = run_condition(
                    condition_name=condition,
                    base_config=cfg,
                    fitness_fn=make_gp_fitness_function(program_length, encoding, problem),
                    generation_hook=make_primitive_frequency_hook(program_length, encoding),
                    out_dir=out_dir,
                    n_runs=n_runs,
                    seed_start=seed_cursor,
                    ideal_fitness=ideal,
                    maximize=True,
                    resume_if_exists=resume_if_exists,
                )
                rows.append(
                    {
                        "condition": condition,
                        "problem": problem,
                        "encoding": encoding,
                        "pop_size": pop,
                        "tournament_size": t,
                        **out["summary"],
                    }
                )
                seed_cursor += 100
    df = pd.DataFrame(rows).sort_values(["problem", "pop_size", "tournament_size"]).reset_index(drop=True)
    df.to_csv(out_dir / "task7_summary.csv", index=False)
    return df


def plot_primitive_trends(condition_dir: Path, out_path: Path, title: str) -> None:
    agg_path = condition_dir / "generation_aggregated.csv"
    if not agg_path.exists():
        return
    agg = pd.read_csv(agg_path)
    freq_cols = [c for c in agg.columns if c.startswith("freq_") and c.endswith("_mean")]
    if not freq_cols:
        return

    plt.figure(figsize=(10, 6))
    for col in freq_cols:
        primitive = col.replace("freq_", "").replace("_mean", "")
        plt.plot(agg["generation"], agg[col], label=primitive, linewidth=1.8)
    plt.title(title)
    plt.xlabel("Generation")
    plt.ylabel("Primitive Frequency")
    plt.ylim(0.0, 1.0)
    plt.grid(alpha=0.3)
    plt.legend(ncol=4, fontsize=8)
    plt.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, dpi=150)
    plt.close()


def run_task8_primitive_report(task7_df: pd.DataFrame) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task8_primitives")
    rows = []
    base_dir = RESULT_ROOT / "task7_experiments"

    for problem in ["problem1", "problem2"]:
        sub = task7_df[task7_df["problem"] == problem].copy()
        if sub.empty:
            continue
        # Use best mean best-of-run configuration per problem.
        best = sub.sort_values("best_of_run_mean", ascending=False).iloc[0]
        condition = best["condition"]
        condition_dir = base_dir / condition
        out_path = out_dir / f"{problem}_primitive_trends.png"
        plot_primitive_trends(condition_dir, out_path, title=f"{problem} primitive trends ({condition})")
        rows.append(
            {
                "problem": problem,
                "selected_condition": condition,
                "best_of_run_mean": float(best["best_of_run_mean"]),
                "best_of_run_std": float(best["best_of_run_std"]),
                "plot_file": str(out_path),
            }
        )

    df = pd.DataFrame(rows)
    df.to_csv(out_dir / "task8_selected_conditions.csv", index=False)
    return df


def build_part2_report(
    encoding_df: pd.DataFrame,
    task7_df: pd.DataFrame,
    task8_df: pd.DataFrame,
    selected_params: Dict[str, int],
) -> None:
    out_path = RESULT_ROOT / "part2_report_summary.md"
    lines = []
    lines.append("# CE310 Part 2 Auto Summary")
    lines.append("")
    lines.append("## Selected GA Baseline from Part 1")
    lines.append(f"- pop_size={selected_params['best_pop_size']}")
    lines.append(f"- tournament_size={selected_params['best_tournament_size']}")
    lines.append("")
    lines.append("## Task 5 Encoding Comparison")
    for _, r in encoding_df.iterrows():
        lines.append(
            f"- `{r['condition']}`: mean best-of-run={r['best_of_run_mean']:.3f}, "
            f"std={r['best_of_run_std']:.3f}"
        )
    lines.append("")
    lines.append("## Task 7 Experiments")
    lines.append("- Summary file: `results/part2/task7_experiments/task7_summary.csv`")
    for _, r in task7_df.iterrows():
        extra = ""
        if "ideal_found_fraction" in r and pd.notna(r["ideal_found_fraction"]):
            extra = f", ideal_found_fraction={r['ideal_found_fraction']:.3f}"
        cost = ""
        if "mean_execute_calls_per_generation" in r and pd.notna(r["mean_execute_calls_per_generation"]):
            cost = f", avg_execute_calls/gen={r['mean_execute_calls_per_generation']:.1f}"
        cost_nom = ""
        if (
            "mean_execute_calls_nominal_per_generation" in r
            and pd.notna(r["mean_execute_calls_nominal_per_generation"])
        ):
            cost_nom = (
                f", nominal_execute_calls/gen={r['mean_execute_calls_nominal_per_generation']:.1f}"
            )
        reduction = ""
        if "execute_call_reduction_ratio" in r and pd.notna(r["execute_call_reduction_ratio"]):
            reduction = f", call_reduction={100.0 * r['execute_call_reduction_ratio']:.1f}%"
        lines.append(
            f"- `{r['condition']}`: mean best-of-run={r['best_of_run_mean']:.3f}, "
            f"std={r['best_of_run_std']:.3f}{extra}{cost}{cost_nom}{reduction}"
        )
    lines.append("")
    lines.append("## Task 8 Primitive Trends")
    for _, r in task8_df.iterrows():
        lines.append(
            f"- `{r['problem']}` best condition `{r['selected_condition']}` -> `{r['plot_file']}`"
        )
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("- All run histories, configs, and aggregated stats are in `results/part2/`.")
    lines.append("- Each condition records per-generation fitness stats and primitive frequencies.")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_int_list(csv: str) -> List[int]:
    return [int(x.strip()) for x in csv.split(",") if x.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CE310 Part2 GP experiments.")
    parser.add_argument("--quick", action="store_true", help="Run a reduced experiment set for quick iteration.")
    parser.add_argument("--program-length", type=int, default=30)
    parser.add_argument("--encoding", choices=["3bit", "7bit"], default="3bit")
    parser.add_argument("--runs-encoding", type=int, default=5)
    parser.add_argument("--runs-task7", type=int, default=10)
    parser.add_argument("--pops", type=str, default="50,100,200")
    parser.add_argument("--tournaments", type=str, default="2,3,5")
    parser.add_argument("--no-resume", action="store_true", help="Force recomputation even if condition outputs exist.")
    args = parser.parse_args()

    ensure_dir(RESULT_ROOT)
    selected = load_best_part1_params()
    best_pop = selected["best_pop_size"]
    best_t = selected["best_tournament_size"]
    program_length = args.program_length
    pops = parse_int_list(args.pops)
    tournaments = parse_int_list(args.tournaments)
    runs_encoding = args.runs_encoding
    runs_task7 = args.runs_task7
    resume_if_exists = not args.no_resume

    if args.quick:
        pops = [50, 100]
        tournaments = [2, 3]
        runs_encoding = min(runs_encoding, 3)
        runs_task7 = min(runs_task7, 5)

    # estimate with one entry per (pop,tournament), each solving both problems
    nominal_calls_task7 = sum(pop * len(tournaments) * runs_task7 * 50 * (2 + 21) for pop in pops)
    nominal_calls_task5 = 2 * best_pop * runs_encoding * 50 * (2 + 21)
    nominal_calls = nominal_calls_task7 + nominal_calls_task5
    print(
        "Planned nominal execute() calls (before caching/skip): "
        f"{nominal_calls:,} | resume={resume_if_exists} | quick={args.quick}"
    )

    write_json(RESULT_ROOT / "selected_baseline_from_part1.json", selected)
    encoding_df = run_encoding_comparison(
        best_pop=best_pop,
        best_t=best_t,
        program_length=program_length,
        n_runs=runs_encoding,
        resume_if_exists=resume_if_exists,
    )
    task7_df = run_task7_experiments(
        program_length=program_length,
        encoding=args.encoding,
        pops=pops,
        tournaments=tournaments,
        n_runs=runs_task7,
        resume_if_exists=resume_if_exists,
    )
    task8_df = run_task8_primitive_report(task7_df)
    build_part2_report(encoding_df=encoding_df, task7_df=task7_df, task8_df=task8_df, selected_params=selected)
    print("Part 2 experiments completed.")


if __name__ == "__main__":
    main()

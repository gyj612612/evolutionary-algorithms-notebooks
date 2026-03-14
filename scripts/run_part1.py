from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ce310.experiments import run_condition
from ce310.part1_problems import (
    fitness_one_max,
    make_fitness_15max,
    make_fitness_soft15max,
    make_fitness_soft15trap_integer,
)
from ce310.utils import ensure_dir, write_json


RESULT_ROOT = Path("results") / "part1"


def build_cfg(
    pop_size: int,
    genome_length: int,
    tournament_size: int,
    p_clone: float,
    p_mutation_operator: float,
    p_bit_factor: float,
) -> Dict:
    p_xo = 1.0 - p_clone - p_mutation_operator
    if p_xo <= 0:
        raise ValueError("Invalid operator probability setup")
    return {
        "pop_size": pop_size,
        "genome_length": genome_length,
        "generations": 50,
        "tournament_size": tournament_size,
        "p_clone": p_clone,
        "p_crossover": p_xo,
        "p_mutation_operator": p_mutation_operator,
        "p_bit_mutation": p_bit_factor / genome_length,
        "experiment_name": "part1",
    }


def run_task1_baseline(
    selected_params: Dict[str, float],
    n_runs: int,
    resume_if_exists: bool,
) -> Dict:
    out_dir = ensure_dir(RESULT_ROOT / "task1_onemax")
    cfg = build_cfg(
        pop_size=int(selected_params["pop_size"]),
        genome_length=100,
        tournament_size=int(selected_params["tournament_size"]),
        p_clone=float(selected_params["p_clone"]),
        p_mutation_operator=float(selected_params["p_mutation_operator"]),
        p_bit_factor=float(selected_params["p_bit_factor"]),
    )
    return run_condition(
        condition_name="onemax_L100",
        base_config=cfg,
        fitness_fn=fitness_one_max,
        out_dir=out_dir,
        n_runs=n_runs,
        seed_start=10000,
        ideal_fitness=100.0,
        maximize=True,
        resume_if_exists=resume_if_exists,
    )


def run_stage1_pop_t_tuning(
    n_runs: int,
    resume_if_exists: bool,
    pops: List[int],
    tournaments: List[int],
) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task3_tuning_stage1")
    rows: List[Dict] = []
    idx = 0
    for pop in pops:
        for t in tournaments:
            condition = f"pop{pop}_t{t}"
            cfg = build_cfg(
                pop_size=pop,
                genome_length=120,  # L=30, 4-bit
                tournament_size=t,
                p_clone=0.2,
                p_mutation_operator=0.1,
                p_bit_factor=1.0,
            )
            out = run_condition(
                condition_name=condition,
                base_config=cfg,
                fitness_fn=make_fitness_15max(length_l=30, encoding="4bit"),
                out_dir=out_dir,
                n_runs=n_runs,
                seed_start=11000 + 100 * idx,
                ideal_fitness=30.0,
                maximize=True,
                resume_if_exists=resume_if_exists,
            )
            rows.append(
                {
                    "condition": condition,
                    "pop_size": pop,
                    "tournament_size": t,
                    "p_clone": 0.2,
                    "p_mutation_operator": 0.1,
                    "p_bit_factor": 1.0,
                    **out["summary"],
                }
            )
            idx += 1
    df = pd.DataFrame(rows).sort_values("best_of_run_mean", ascending=False).reset_index(drop=True)
    df.to_csv(out_dir / "stage1_summary.csv", index=False)
    return df


def run_stage2_operator_tuning(
    best_pop: int,
    best_t: int,
    n_runs: int,
    resume_if_exists: bool,
    p_clones: List[float],
    p_mutops: List[float],
    p_bit_factors: List[float],
) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task3_tuning_stage2")
    rows: List[Dict] = []
    idx = 0
    for p_clone in p_clones:
        for p_mutop in p_mutops:
            for p_bit_factor in p_bit_factors:
                p_xo = 1.0 - p_clone - p_mutop
                if p_xo <= 0:
                    continue
                condition = f"pc{p_clone:.2f}_pmop{p_mutop:.2f}_pbf{p_bit_factor:.2f}"
                cfg = build_cfg(
                    pop_size=best_pop,
                    genome_length=120,  # L=30, 4-bit
                    tournament_size=best_t,
                    p_clone=p_clone,
                    p_mutation_operator=p_mutop,
                    p_bit_factor=p_bit_factor,
                )
                out = run_condition(
                    condition_name=condition,
                    base_config=cfg,
                    fitness_fn=make_fitness_15max(length_l=30, encoding="4bit"),
                    out_dir=out_dir,
                    n_runs=n_runs,
                    seed_start=13000 + 100 * idx,
                    ideal_fitness=30.0,
                    maximize=True,
                    resume_if_exists=resume_if_exists,
                )
                rows.append(
                    {
                        "condition": condition,
                        "pop_size": best_pop,
                        "tournament_size": best_t,
                        "p_clone": p_clone,
                        "p_mutation_operator": p_mutop,
                        "p_crossover": p_xo,
                        "p_bit_factor": p_bit_factor,
                        **out["summary"],
                    }
                )
                idx += 1
    df = pd.DataFrame(rows).sort_values("best_of_run_mean", ascending=False).reset_index(drop=True)
    df.to_csv(out_dir / "stage2_summary.csv", index=False)
    return df


def run_task3_main(selected_params: Dict[str, float], n_runs: int, resume_if_exists: bool) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task3_main")
    rows: List[Dict] = []
    seed_cursor = 20000
    for encoding in ["4bit", "15bit"]:
        for length_l in [10, 30]:
            block = 4 if encoding == "4bit" else 15
            genome_length = block * length_l
            cfg = build_cfg(
                pop_size=int(selected_params["pop_size"]),
                genome_length=genome_length,
                tournament_size=int(selected_params["tournament_size"]),
                p_clone=float(selected_params["p_clone"]),
                p_mutation_operator=float(selected_params["p_mutation_operator"]),
                p_bit_factor=float(selected_params["p_bit_factor"]),
            )
            for objective in ["15max", "soft15max"]:
                if objective == "15max":
                    fitness_fn = make_fitness_15max(length_l=length_l, encoding=encoding)
                    ideal = float(length_l)
                else:
                    fitness_fn = make_fitness_soft15max(length_l=length_l, encoding=encoding)
                    ideal = 15.0
                condition = f"{encoding}_L{length_l}_{objective}"
                out = run_condition(
                    condition_name=condition,
                    base_config=cfg,
                    fitness_fn=fitness_fn,
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
                        "L": length_l,
                        "objective": objective,
                        "ideal_fitness": ideal,
                        **out["summary"],
                    }
                )
                seed_cursor += 100
    df = pd.DataFrame(rows).sort_values(["objective", "encoding", "L"]).reset_index(drop=True)
    df.to_csv(out_dir / "task3_summary.csv", index=False)
    return df


def run_task4_deceptive(selected_params: Dict[str, float], n_runs: int, resume_if_exists: bool) -> pd.DataFrame:
    out_dir = ensure_dir(RESULT_ROOT / "task4_trap")
    rows: List[Dict] = []
    seed_cursor = 30000
    for encoding in ["4bit", "15bit"]:
        for length_l in [10, 30]:
            block = 4 if encoding == "4bit" else 15
            genome_length = block * length_l
            cfg = build_cfg(
                pop_size=int(selected_params["pop_size"]),
                genome_length=genome_length,
                tournament_size=int(selected_params["tournament_size"]),
                p_clone=float(selected_params["p_clone"]),
                p_mutation_operator=float(selected_params["p_mutation_operator"]),
                p_bit_factor=float(selected_params["p_bit_factor"]),
            )
            condition = f"{encoding}_L{length_l}_soft15trap_int"
            out = run_condition(
                condition_name=condition,
                base_config=cfg,
                fitness_fn=make_fitness_soft15trap_integer(length_l=length_l, encoding=encoding),
                out_dir=out_dir,
                n_runs=n_runs,
                seed_start=seed_cursor,
                ideal_fitness=15.0,
                maximize=True,
                resume_if_exists=resume_if_exists,
            )
            rows.append(
                {
                    "condition": condition,
                    "encoding": encoding,
                    "L": length_l,
                    "objective": "soft15trap_int",
                    "deceptive_local_optimum": 14.0,
                    "global_optimum": 15.0,
                    **out["summary"],
                }
            )
            seed_cursor += 100
    df = pd.DataFrame(rows).sort_values(["encoding", "L"]).reset_index(drop=True)
    df.to_csv(out_dir / "task4_summary.csv", index=False)
    return df


def build_part1_report(
    stage1_df: pd.DataFrame,
    stage2_df: pd.DataFrame,
    selected_params: Dict[str, float],
    task1_summary: Dict,
    task3_df: pd.DataFrame,
    task4_df: pd.DataFrame,
) -> None:
    out_path = RESULT_ROOT / "part1_report_summary.md"
    s1 = stage1_df.iloc[0]
    s2 = stage2_df.iloc[0]

    soft_baseline = task3_df[task3_df["objective"] == "soft15max"][
        ["encoding", "L", "best_of_run_mean", "ideal_found_fraction"]
    ].rename(
        columns={
            "best_of_run_mean": "soft15max_best_mean",
            "ideal_found_fraction": "soft15max_ideal_found_fraction",
        }
    )
    trap_cmp = task4_df.merge(soft_baseline, on=["encoding", "L"], how="left")
    trap_cmp["delta_best_mean_trap_minus_soft"] = (
        trap_cmp["best_of_run_mean"] - trap_cmp["soft15max_best_mean"]
    )
    trap_cmp["delta_ideal_found_fraction_trap_minus_soft"] = (
        trap_cmp["ideal_found_fraction"] - trap_cmp["soft15max_ideal_found_fraction"]
    )
    trap_cmp.to_csv(RESULT_ROOT / "task4_deceptive_vs_soft15max.csv", index=False)

    lines = []
    lines.append("# CE310 Part 1 Auto Summary")
    lines.append("")
    lines.append("## Selected Parameters")
    lines.append(
        f"- `pop_size={int(selected_params['pop_size'])}`, `tournament_size={int(selected_params['tournament_size'])}`, "
        f"`p_clone={selected_params['p_clone']:.3f}`, `p_xo={selected_params['p_crossover']:.3f}`, "
        f"`p_mutop={selected_params['p_mutation_operator']:.3f}`, `p_bit={selected_params['p_bit_mutation']:.5f}`"
    )
    lines.append("")
    lines.append("## Task 1 (OneMax)")
    lines.append("- Condition: `onemax_L100`")
    lines.append(f"- Mean best-of-run: **{task1_summary['summary']['best_of_run_mean']:.3f}**")
    lines.append(f"- Std best-of-run: **{task1_summary['summary']['best_of_run_std']:.3f}**")
    if "ideal_found_fraction" in task1_summary["summary"]:
        lines.append(f"- Ideal-found fraction: **{task1_summary['summary']['ideal_found_fraction']:.3f}**")
    lines.append("")
    lines.append("## Task 3 Tuning")
    lines.append(
        f"- Stage1 best (`pop`, `T`): ({int(s1['pop_size'])}, {int(s1['tournament_size'])}) "
        f"with mean best-of-run **{s1['best_of_run_mean']:.3f}**"
    )
    lines.append(
        f"- Stage2 best operators: `p_clone={s2['p_clone']:.3f}`, `p_xo={s2['p_crossover']:.3f}`, "
        f"`p_mutop={s2['p_mutation_operator']:.3f}`, `p_bit_factor={s2['p_bit_factor']:.3f}` "
        f"with mean best-of-run **{s2['best_of_run_mean']:.3f}**"
    )
    lines.append("")
    lines.append("## Task 3 Main Experiments")
    lines.append("- File: `results/part1/task3_main/task3_summary.csv`")
    for _, r in task3_df.iterrows():
        lines.append(
            f"- `{r['condition']}`: mean best-of-run={r['best_of_run_mean']:.3f}, "
            f"std={r['best_of_run_std']:.3f}, ideal-found={r.get('ideal_found_fraction', float('nan')):.3f}"
        )
    lines.append("")
    lines.append("## Task 4 Deceptive Problem (Soft-15 Trap Integer)")
    lines.append("- File: `results/part1/task4_trap/task4_summary.csv`")
    lines.append("- Comparison file: `results/part1/task4_deceptive_vs_soft15max.csv`")
    for _, r in trap_cmp.iterrows():
        lines.append(
            f"- `{r['condition']}`: trap mean={r['best_of_run_mean']:.3f}, "
            f"soft15max mean={r['soft15max_best_mean']:.3f}, "
            f"delta={r['delta_best_mean_trap_minus_soft']:.3f}, "
            f"trap ideal-found={r['ideal_found_fraction']:.3f}, "
            f"soft ideal-found={r['soft15max_ideal_found_fraction']:.3f}"
        )
    lines.append("")
    lines.append("## Reproducibility")
    lines.append("- All run histories, configs, and aggregated stats are under `results/part1/`.")
    lines.append("- Every condition stores per-generation best/mean/std plus run-level summaries.")

    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_int_list(csv: str) -> List[int]:
    return [int(x.strip()) for x in csv.split(",") if x.strip()]


def parse_float_list(csv: str) -> List[float]:
    return [float(x.strip()) for x in csv.split(",") if x.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CE310 Part1 GA experiments.")
    parser.add_argument("--quick", action="store_true", help="Run reduced experiment counts for fast iteration.")
    parser.add_argument("--no-resume", action="store_true", help="Force recomputation even if outputs exist.")
    parser.add_argument("--runs-task1", type=int, default=10)
    parser.add_argument("--runs-tune-stage1", type=int, default=5)
    parser.add_argument("--runs-tune-stage2", type=int, default=3)
    parser.add_argument("--runs-main", type=int, default=10)
    parser.add_argument("--pops", type=str, default="20,50,100,200,300")
    parser.add_argument("--tournaments", type=str, default="2,3,5,7")
    parser.add_argument("--p-clones", type=str, default="0.1,0.2,0.3")
    parser.add_argument("--p-mutops", type=str, default="0.05,0.1,0.2")
    parser.add_argument("--p-bit-factors", type=str, default="0.5,1.0,1.5")
    args = parser.parse_args()

    resume_if_exists = not args.no_resume
    pops = parse_int_list(args.pops)
    tournaments = parse_int_list(args.tournaments)
    p_clones = parse_float_list(args.p_clones)
    p_mutops = parse_float_list(args.p_mutops)
    p_bit_factors = parse_float_list(args.p_bit_factors)

    runs_task1 = args.runs_task1
    runs_tune_stage1 = args.runs_tune_stage1
    runs_tune_stage2 = args.runs_tune_stage2
    runs_main = args.runs_main

    if args.quick:
        pops = [50, 100, 200]
        tournaments = [2, 3, 5]
        p_clones = [0.1, 0.2]
        p_mutops = [0.1, 0.2]
        p_bit_factors = [0.5, 1.0]
        runs_task1 = min(runs_task1, 5)
        runs_tune_stage1 = min(runs_tune_stage1, 3)
        runs_tune_stage2 = min(runs_tune_stage2, 2)
        runs_main = min(runs_main, 5)

    ensure_dir(RESULT_ROOT)

    stage1_df = run_stage1_pop_t_tuning(
        n_runs=runs_tune_stage1,
        resume_if_exists=resume_if_exists,
        pops=pops,
        tournaments=tournaments,
    )
    best_pop = int(stage1_df.iloc[0]["pop_size"])
    best_t = int(stage1_df.iloc[0]["tournament_size"])

    stage2_df = run_stage2_operator_tuning(
        best_pop=best_pop,
        best_t=best_t,
        n_runs=runs_tune_stage2,
        resume_if_exists=resume_if_exists,
        p_clones=p_clones,
        p_mutops=p_mutops,
        p_bit_factors=p_bit_factors,
    )
    best = stage2_df.iloc[0]
    selected_params = {
        "pop_size": int(best["pop_size"]),
        "tournament_size": int(best["tournament_size"]),
        "p_clone": float(best["p_clone"]),
        "p_crossover": float(best["p_crossover"]),
        "p_mutation_operator": float(best["p_mutation_operator"]),
        "p_bit_factor": float(best["p_bit_factor"]),
        "p_bit_mutation": float(best["p_bit_factor"]) / 120.0,
    }
    write_json(RESULT_ROOT / "selected_part1_params.json", selected_params)

    task1 = run_task1_baseline(
        selected_params=selected_params,
        n_runs=runs_task1,
        resume_if_exists=resume_if_exists,
    )
    task3_df = run_task3_main(
        selected_params=selected_params,
        n_runs=runs_main,
        resume_if_exists=resume_if_exists,
    )
    task4_df = run_task4_deceptive(
        selected_params=selected_params,
        n_runs=runs_main,
        resume_if_exists=resume_if_exists,
    )
    build_part1_report(
        stage1_df=stage1_df,
        stage2_df=stage2_df,
        selected_params=selected_params,
        task1_summary=task1,
        task3_df=task3_df,
        task4_df=task4_df,
    )

    print("Part 1 experiments completed.")
    print(
        "Selected params:",
        f"pop={selected_params['pop_size']}, T={selected_params['tournament_size']}, ",
        f"p_clone={selected_params['p_clone']:.3f}, p_xo={selected_params['p_crossover']:.3f}, ",
        f"p_mutop={selected_params['p_mutation_operator']:.3f}, p_bit_factor={selected_params['p_bit_factor']:.3f}",
    )


if __name__ == "__main__":
    main()


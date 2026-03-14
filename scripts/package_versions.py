from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ce310.experiments import run_condition
from ce310.gp import make_gp_fitness_function, make_primitive_frequency_hook
from ce310.part1_problems import (
    fitness_one_max,
    make_fitness_15max,
    make_fitness_15trap,
    make_fitness_soft15max,
)
from ce310.utils import ensure_dir, write_json


ROOT = Path(__file__).resolve().parents[1]
BACKUP_ROOT = ROOT / "backups"


def _reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _copy_common_submit_files(target_dir: Path, part1_path: Path, part2_path: Path) -> None:
    shutil.copy2(part1_path, target_dir / "Part1.ipynb")
    shutil.copy2(part2_path, target_dir / "Part2.ipynb")
    shutil.copy2(ROOT / "AI_LOG_TEMPLATE.md", target_dir / "AI_LOG_TEMPLATE.md")
    shutil.copy2(ROOT / "PROJECT_DELIVERY.md", target_dir / "PROJECT_DELIVERY.md")


def _zip_dir(src_dir: Path, out_zip_without_ext: Path) -> Path:
    out_zip = shutil.make_archive(str(out_zip_without_ext), "zip", str(src_dir))
    return Path(out_zip)


def _legacy_base_cfg(pop_size: int, genome_length: int, tournament_size: int) -> Dict:
    return {
        "pop_size": pop_size,
        "genome_length": genome_length,
        "generations": 50,
        "tournament_size": tournament_size,
        "p_clone": 0.2,
        "p_crossover": 0.7,
        "p_mutation_operator": 0.1,
        "p_bit_mutation": 1.0 / genome_length,
        "experiment_name": "part1_v1",
    }


def _run_legacy_part1(results_root: Path) -> Dict[str, int]:
    part1_root = ensure_dir(results_root / "part1")

    # Task1
    task1_out = ensure_dir(part1_root / "task1_onemax")
    cfg = _legacy_base_cfg(pop_size=100, genome_length=100, tournament_size=3)
    task1 = run_condition(
        condition_name="onemax_L100",
        base_config=cfg,
        fitness_fn=fitness_one_max,
        out_dir=task1_out,
        n_runs=10,
        seed_start=10000,
        ideal_fitness=100.0,
        maximize=True,
        resume_if_exists=False,
    )

    # Task3 tuning
    tune_out = ensure_dir(part1_root / "task3_tuning")
    rows: List[Dict] = []
    idx = 0
    for pop in [20, 50, 100, 200]:
        for t in [2, 3, 5, 7]:
            out = run_condition(
                condition_name=f"pop{pop}_t{t}",
                base_config=_legacy_base_cfg(pop_size=pop, genome_length=120, tournament_size=t),
                fitness_fn=make_fitness_15max(length_l=30, encoding="4bit"),
                out_dir=tune_out,
                n_runs=5,
                seed_start=11000 + 100 * idx,
                ideal_fitness=30.0,
                maximize=True,
                resume_if_exists=False,
            )
            rows.append({"condition": f"pop{pop}_t{t}", "pop_size": pop, "tournament_size": t, **out["summary"]})
            idx += 1
    tuning_df = pd.DataFrame(rows).sort_values("best_of_run_mean", ascending=False).reset_index(drop=True)
    tuning_df.to_csv(tune_out / "tuning_summary.csv", index=False)
    best_pop = int(tuning_df.iloc[0]["pop_size"])
    best_t = int(tuning_df.iloc[0]["tournament_size"])

    selected = {"best_pop_size": best_pop, "best_tournament_size": best_t}
    write_json(part1_root / "selected_part1_params.json", selected)

    # Task3 main
    task3_out = ensure_dir(part1_root / "task3_main")
    rows = []
    seed_cursor = 20000
    for encoding in ["4bit", "15bit"]:
        for length_l in [10, 30]:
            block = 4 if encoding == "4bit" else 15
            cfg = _legacy_base_cfg(best_pop, block * length_l, best_t)
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
                    out_dir=task3_out,
                    n_runs=10,
                    seed_start=seed_cursor,
                    ideal_fitness=ideal,
                    maximize=True,
                    resume_if_exists=False,
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
    task3_df = pd.DataFrame(rows).sort_values(["objective", "encoding", "L"]).reset_index(drop=True)
    task3_df.to_csv(task3_out / "task3_summary.csv", index=False)

    # Task4 legacy trap
    task4_out = ensure_dir(part1_root / "task4_trap")
    rows = []
    seed_cursor = 30000
    for encoding in ["4bit", "15bit"]:
        for length_l in [10, 30]:
            block = 4 if encoding == "4bit" else 15
            cfg = _legacy_base_cfg(best_pop, block * length_l, best_t)
            condition = f"{encoding}_L{length_l}_trap"
            out = run_condition(
                condition_name=condition,
                base_config=cfg,
                fitness_fn=make_fitness_15trap(length_l=length_l, encoding=encoding),
                out_dir=task4_out,
                n_runs=10,
                seed_start=seed_cursor,
                ideal_fitness=float(length_l),
                maximize=True,
                resume_if_exists=False,
            )
            rows.append(
                {
                    "condition": condition,
                    "encoding": encoding,
                    "L": length_l,
                    "objective": "15trap",
                    **out["summary"],
                }
            )
            seed_cursor += 100
    task4_df = pd.DataFrame(rows).sort_values(["encoding", "L"]).reset_index(drop=True)
    task4_df.to_csv(task4_out / "task4_summary.csv", index=False)

    # Legacy summary
    lines = []
    lines.append("# CE310 Part 1 Auto Summary (Legacy V1)")
    lines.append("")
    lines.append("## Task 1 (OneMax)")
    lines.append(f"- Mean best-of-run: **{task1['summary']['best_of_run_mean']:.3f}**")
    lines.append(f"- Std best-of-run: **{task1['summary']['best_of_run_std']:.3f}**")
    lines.append(f"- Ideal-found fraction: **{task1['summary'].get('ideal_found_fraction', float('nan')):.3f}**")
    lines.append("")
    lines.append("## Task 3 Tuning")
    lines.append(f"- Selected params: `pop_size={best_pop}`, `tournament_size={best_t}`")
    lines.append("")
    lines.append("## Task 3 Main")
    for _, r in task3_df.iterrows():
        lines.append(f"- `{r['condition']}`: mean={r['best_of_run_mean']:.3f}, std={r['best_of_run_std']:.3f}")
    lines.append("")
    lines.append("## Task 4 Trap")
    for _, r in task4_df.iterrows():
        lines.append(f"- `{r['condition']}`: mean={r['best_of_run_mean']:.3f}, std={r['best_of_run_std']:.3f}")
    (part1_root / "part1_report_summary.md").write_text("\n".join(lines), encoding="utf-8")

    return selected


def _plot_primitive_trends(condition_dir: Path, out_path: Path, title: str) -> None:
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


def _run_legacy_part2(results_root: Path, selected: Dict[str, int]) -> None:
    part2_root = ensure_dir(results_root / "part2")
    best_pop = int(selected["best_pop_size"])
    best_t = int(selected["best_tournament_size"])
    write_json(part2_root / "selected_baseline_from_part1.json", selected)

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
            "experiment_name": "part2_v1",
        }

    # Task5 encoding comparison
    enc_out = ensure_dir(part2_root / "task5_encoding_comparison")
    rows = []
    seed_cursor = 40000
    for encoding in ["3bit", "7bit"]:
        bits_per_instr = 3 if encoding == "3bit" else 7
        cfg = base_cfg(best_pop, bits_per_instr * 30, best_t)
        for problem in ["problem1", "problem2"]:
            out = run_condition(
                condition_name=f"{encoding}_{problem}",
                base_config=cfg,
                fitness_fn=make_gp_fitness_function(30, encoding, problem),
                generation_hook=make_primitive_frequency_hook(30, encoding),
                out_dir=enc_out,
                n_runs=5,
                seed_start=seed_cursor,
                ideal_fitness=0.0 if problem == "problem2" else None,
                maximize=True,
                resume_if_exists=False,
            )
            rows.append({"condition": f"{encoding}_{problem}", "encoding": encoding, "problem": problem, **out["summary"]})
            seed_cursor += 100
    encoding_df = pd.DataFrame(rows).sort_values(["problem", "encoding"]).reset_index(drop=True)
    encoding_df.to_csv(enc_out / "encoding_comparison_summary.csv", index=False)

    # Task7
    task7_out = ensure_dir(part2_root / "task7_experiments")
    rows = []
    seed_cursor = 50000
    for problem in ["problem1", "problem2"]:
        for pop in [50, 100, 200]:
            for t in [2, 3, 5]:
                out = run_condition(
                    condition_name=f"{problem}_3bit_pop{pop}_t{t}",
                    base_config=base_cfg(pop, 90, t),
                    fitness_fn=make_gp_fitness_function(30, "3bit", problem),
                    generation_hook=make_primitive_frequency_hook(30, "3bit"),
                    out_dir=task7_out,
                    n_runs=10,
                    seed_start=seed_cursor,
                    ideal_fitness=0.0 if problem == "problem2" else None,
                    maximize=True,
                    resume_if_exists=False,
                )
                rows.append(
                    {
                        "condition": f"{problem}_3bit_pop{pop}_t{t}",
                        "problem": problem,
                        "encoding": "3bit",
                        "pop_size": pop,
                        "tournament_size": t,
                        **out["summary"],
                    }
                )
                seed_cursor += 100
    task7_df = pd.DataFrame(rows).sort_values(["problem", "pop_size", "tournament_size"]).reset_index(drop=True)
    task7_df.to_csv(task7_out / "task7_summary.csv", index=False)

    # Task8
    task8_out = ensure_dir(part2_root / "task8_primitives")
    rows = []
    for problem in ["problem1", "problem2"]:
        sub = task7_df[task7_df["problem"] == problem].copy()
        best = sub.sort_values("best_of_run_mean", ascending=False).iloc[0]
        condition = best["condition"]
        out_path = task8_out / f"{problem}_primitive_trends.png"
        _plot_primitive_trends(task7_out / condition, out_path, f"{problem} primitive trends ({condition})")
        rows.append(
            {
                "problem": problem,
                "selected_condition": condition,
                "best_of_run_mean": float(best["best_of_run_mean"]),
                "best_of_run_std": float(best["best_of_run_std"]),
                "plot_file": str(out_path),
            }
        )
    task8_df = pd.DataFrame(rows)
    task8_df.to_csv(task8_out / "task8_selected_conditions.csv", index=False)

    # Legacy summary
    lines = []
    lines.append("# CE310 Part 2 Auto Summary (Legacy V1)")
    lines.append("")
    lines.append("## Selected GA Baseline from Part 1")
    lines.append(f"- pop_size={best_pop}")
    lines.append(f"- tournament_size={best_t}")
    lines.append("")
    lines.append("## Task 5 Encoding Comparison")
    for _, r in encoding_df.iterrows():
        lines.append(f"- `{r['condition']}`: mean={r['best_of_run_mean']:.3f}, std={r['best_of_run_std']:.3f}")
    lines.append("")
    lines.append("## Task 7")
    for _, r in task7_df.iterrows():
        lines.append(
            f"- `{r['condition']}`: mean={r['best_of_run_mean']:.3f}, std={r['best_of_run_std']:.3f}, "
            f"ideal_found={r.get('ideal_found_fraction', float('nan')):.3f}"
        )
    lines.append("")
    lines.append("## Task 8")
    for _, r in task8_df.iterrows():
        lines.append(f"- `{r['problem']}` -> `{r['plot_file']}`")
    (part2_root / "part2_report_summary.md").write_text("\n".join(lines), encoding="utf-8")


def _write_manifest(version_dir: Path, version_name: str, notes: Dict) -> None:
    manifest = {"version": version_name, **notes}
    (version_dir / "VERSION_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def build_version2_package() -> Path:
    v2_dir = BACKUP_ROOT / "version2"
    _reset_dir(v2_dir)
    _copy_common_submit_files(v2_dir, ROOT / "Part1.ipynb", ROOT / "Part2.ipynb")
    shutil.copytree(ROOT / "results", v2_dir / "results", dirs_exist_ok=True)
    _write_manifest(
        v2_dir,
        "version2",
        {
            "description": "Current optimized version (Task1 one-max around 99.9).",
            "source": "Current workspace state",
        },
    )
    zip_path = _zip_dir(v2_dir, BACKUP_ROOT / "version2_final_submission")
    return zip_path


def build_version1_package() -> Path:
    v1_dir = BACKUP_ROOT / "version1"
    _reset_dir(v1_dir)
    _copy_common_submit_files(v1_dir, ROOT / "Part1.ipynb", ROOT / "Part2.ipynb")

    results_root = ensure_dir(v1_dir / "results")
    selected = _run_legacy_part1(results_root=results_root)
    _run_legacy_part2(results_root=results_root, selected=selected)

    _write_manifest(
        v1_dir,
        "version1",
        {
            "description": "Legacy baseline version (Task1 one-max expected around 96.1).",
            "source": "Reproduced with legacy pipeline/params",
            "selected_params_part1": selected,
        },
    )
    zip_path = _zip_dir(v1_dir, BACKUP_ROOT / "version1_final_submission")
    return zip_path


def main() -> None:
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    v2_zip = build_version2_package()
    v1_zip = build_version1_package()
    print("Built packages:")
    print(f"- {v1_zip}")
    print(f"- {v2_zip}")


if __name__ == "__main__":
    main()


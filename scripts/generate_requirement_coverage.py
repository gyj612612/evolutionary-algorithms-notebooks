from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def exists(path: Path) -> str:
    return "Yes" if path.exists() else "No"


def main() -> None:
    part1_task3 = RESULTS / "part1" / "task3_main" / "task3_summary.csv"
    part1_task4 = RESULTS / "part1" / "task4_trap" / "task4_summary.csv"
    part2_task7 = RESULTS / "part2" / "task7_experiments" / "task7_summary.csv"
    part2_task8 = RESULTS / "part2" / "task8_primitives" / "task8_selected_conditions.csv"

    lines = []
    lines.append("# CE310 Requirement Coverage Matrix")
    lines.append("")
    lines.append("This file maps coursework marking requirements to concrete generated artifacts.")
    lines.append("")

    lines.append("## Deliverables")
    lines.append(f"- Part1 notebook present: **{exists(ROOT / 'Part1.ipynb')}**")
    lines.append(f"- Part2 notebook present: **{exists(ROOT / 'Part2.ipynb')}**")
    lines.append(f"- AI log template present: **{exists(ROOT / 'AI_LOG_TEMPLATE.md')}**")
    lines.append("")

    lines.append("## Part 1")
    lines.append(f"- Task1 one-max runs summary: `{RESULTS / 'part1' / 'task1_onemax'}`")
    lines.append(f"- Task3 tuning stage1 summary present: **{exists(RESULTS / 'part1' / 'task3_tuning_stage1' / 'stage1_summary.csv')}**")
    lines.append(f"- Task3 tuning stage2 summary present: **{exists(RESULTS / 'part1' / 'task3_tuning_stage2' / 'stage2_summary.csv')}**")
    lines.append(f"- Task3 main (10 runs/condition) summary present: **{exists(part1_task3)}**")
    lines.append(f"- Task4 deceptive summary present: **{exists(part1_task4)}**")
    lines.append(f"- Task4 deceptive vs baseline comparison present: **{exists(RESULTS / 'part1' / 'task4_deceptive_vs_soft15max.csv')}**")
    lines.append("")

    lines.append("## Part 2")
    lines.append(f"- Task5 encoding comparison summary present: **{exists(RESULTS / 'part2' / 'task5_encoding_comparison' / 'encoding_comparison_summary.csv')}**")
    lines.append(f"- Task7 summary present: **{exists(part2_task7)}**")
    lines.append(f"- Task8 primitive trend summary present: **{exists(part2_task8)}**")
    lines.append("")

    if part1_task3.exists():
        df = pd.read_csv(part1_task3)
        lines.append("## Part1 Key Metrics")
        for _, r in df.iterrows():
            lines.append(
                f"- `{r['condition']}`: best_of_run_mean={r['best_of_run_mean']:.3f}, "
                f"ideal_found_fraction={r.get('ideal_found_fraction', float('nan')):.3f}"
            )
        lines.append("")

    if part1_task4.exists():
        df = pd.read_csv(part1_task4)
        lines.append("## Task4 Deceptive Metrics")
        for _, r in df.iterrows():
            lines.append(
                f"- `{r['condition']}`: mean={r['best_of_run_mean']:.3f}, "
                f"ideal_found_fraction={r['ideal_found_fraction']:.3f}, "
                f"local_optimum={r['deceptive_local_optimum']:.1f}, global_optimum={r['global_optimum']:.1f}"
            )
        lines.append("")

    if part2_task7.exists():
        df = pd.read_csv(part2_task7)
        lines.append("## Part2 Task7 Checks")
        runs_ok = (df["n_runs"] >= 10).all()
        lines.append(f"- 10 runs per experiment satisfied: **{runs_ok}**")
        lines.append(f"- Number of experiment conditions: **{len(df)}**")
        if "execute_call_reduction_ratio" in df.columns:
            lines.append(
                f"- Mean execute-call reduction (caching): **{100.0 * df['execute_call_reduction_ratio'].mean():.1f}%**"
            )
        lines.append("")

    out = RESULTS / "requirement_coverage.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()


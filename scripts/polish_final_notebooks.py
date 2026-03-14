from __future__ import annotations

from pathlib import Path
from typing import Iterable

import nbformat


ROOT = Path(__file__).resolve().parents[1]


def find_targets() -> list[Path]:
    """Collect root notebooks and mirrored submission copies."""
    targets: list[Path] = []

    for fn in ("Part1.ipynb", "Part2.ipynb"):
        p = ROOT / fn
        if p.exists():
            targets.append(p)

    for d in ROOT.iterdir():
        if not d.is_dir():
            continue
        p1 = d / "Part1.ipynb"
        p2 = d / "Part2.ipynb"
        if p1.exists() and p2.exists():
            targets.extend([p1, p2])

    seen: set[str] = set()
    unique: list[Path] = []
    for p in targets:
        key = str(p.resolve())
        if key in seen:
            continue
        seen.add(key)
        unique.append(p)
    return unique


def rewrite_markdown(source: str, heading_map: dict[str, str]) -> str:
    if not source.strip():
        return source
    first = source.strip().splitlines()[0]
    return heading_map.get(first, source)


def polish_part1(nb) -> None:
    heading_map = {
        "# CE310 Part 1 - Genetic Algorithm (Final Submission Version)": (
            "# CE310 Part 1 - Genetic Algorithm (Final Submission Version)\n\n"
            "This notebook is organized in small lab-style steps: explain first, then run code, then check output."
        ),
        "## Environment Setup": (
            "## Environment Setup\n"
            "Load dependencies, locate the project root, and verify result folders are available."
        ),
        "## Code Completeness Snapshot": (
            "## Code Completeness Snapshot\n"
            "Display core source snippets so implementation coverage is easy to inspect."
        ),
        "## Task 1 Step 1 - Population Initialization Test": (
            "## Task 1 Step 1 - Population Initialization Test\n"
            "Start by validating initialization behavior: shape, value range, and sample individuals."
        ),
        "## Task 1 Step 4 - Clone, Crossover, Mutation Unit Tests": (
            "## Task 1 Step 4 - Clone, Crossover, Mutation Unit Tests\n"
            "Run operator-level checks before integrating the full GA loop."
        ),
        "## Task 1 Step 5 - Integrated GA Run on OneMax": (
            "## Task 1 Step 5 - Integrated GA Run on OneMax\n"
            "Combine components and run one complete trial to verify best/mean trend over generations."
        ),
        "## Task 3 Step 3 - Compare Key Conditions": (
            "## Task 3 Step 3 - Compare Key Conditions\n"
            "I place all conditions on one comparable axis (mean best-of-run) so encoding and objective effects are visible immediately."
        ),
        "## Task 3 Step 3b - Enhanced Visualization (if available)": (
            "## Task 3 Step 3b - Enhanced Visualization (if available)\n"
            "Load the prepared report figures; they do not change results, only improve readability of the same evidence."
        ),
        "## Task 3 Step 4 - Parameter Choice Justification": (
            "## Task 3 Step 4 - Parameter Choice Justification\n"
            "Parameter choice is based on measured outcomes (mean + std), not intuition alone; this keeps the decision reproducible."
        ),
        "## Task 4 Step 2c - Local Optimum Convergence Evidence (Quantitative)": (
            "## Task 4 Step 2c - Local Optimum Convergence Evidence (Quantitative)\n"
            "Beyond plots, I count how often runs finish near the deceptive local optimum versus the global optimum."
        ),
        "## Method Justification Against Lecture Methods": (
            "## Method Justification Against Lecture Methods\n"
            "Core methods are lecture-aligned (selection, crossover, mutation, generational loop, stack interpreter); extra engineering choices only improve runtime/logging."
        ),
        "## Part 1 Final Summary": (
            "## Part 1 Final Summary\n"
            "Summarize conclusions and map them explicitly to marking points."
        ),
    }

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            cell.source = rewrite_markdown(cell.source, heading_map)

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = cell.source

        if "R1 = PROJECT_ROOT / 'results' / 'part1'" in src and "R1.exists()" in src:
            cell.source = (
                "from pathlib import Path\n"
                "import sys\n"
                "import inspect\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "from IPython.display import Image, display\n"
                "\n"
                "ROOT = Path('.').resolve()\n"
                "PROJECT_ROOT = next((p for p in [ROOT, *ROOT.parents] if (p / 'ce310').exists()), ROOT)\n"
                "if str(PROJECT_ROOT) not in sys.path:\n"
                "    sys.path.append(str(PROJECT_ROOT))\n"
                "\n"
                "from ce310.ga import (\n"
                "    GAConfig,\n"
                "    initialize_population,\n"
                "    tournament_select_index,\n"
                "    clone,\n"
                "    one_point_crossover,\n"
                "    bit_mutate,\n"
                "    run_ga,\n"
                ")\n"
                "from ce310.part1_problems import (\n"
                "    fitness_one_max,\n"
                "    decode_4bit_positional,\n"
                "    decode_15bit_nonpositional,\n"
                "    fitness_15max,\n"
                "    fitness_soft15max,\n"
                "    fitness_soft15trap_integer,\n"
                ")\n"
                "\n"
                "R1 = PROJECT_ROOT / 'results' / 'part1'\n"
                "FIG = PROJECT_ROOT / 'figures'\n"
                "print('PROJECT_ROOT =', PROJECT_ROOT)\n"
                "print('Results folder exists:', R1.exists())"
            )
        elif "best_s1 = stage1.iloc[0]" in src:
            cell.source = (
                "best_s1 = stage1.iloc[0]\n"
                "best_s2 = stage2.iloc[0]\n"
                "\n"
                "print('Stage1 best (pop, T):')\n"
                "display(best_s1[['condition','pop_size','tournament_size','best_of_run_mean','best_of_run_std']])\n"
                "\n"
                "print('Stage2 best (operator settings):')\n"
                "display(best_s2[['condition','p_clone','p_crossover','p_mutation_operator','p_bit_factor','best_of_run_mean','best_of_run_std']])"
            )


def polish_part2(nb) -> None:
    heading_map = {
        "# CE310 Part 2 - Genetic Programming (Final Submission Version)": (
            "# CE310 Part 2 - Genetic Programming (Final Submission Version)\n\n"
            "This notebook follows the same incremental pattern: explain the step, run code, inspect evidence."
        ),
        "## Environment Setup": (
            "## Environment Setup\n"
            "Load modules and detect the project root robustly across different working folders."
        ),
        "## Code Completeness Snapshot": (
            "## Code Completeness Snapshot\n"
            "Show core interpreter and fitness-construction code for completeness review."
        ),
        "## Task 7 Step 2 - Protocol Compliance Check": (
            "## Task 7 Step 2 - Protocol Compliance Check\n"
            "Confirm the hard requirement: at least 10 independent runs per condition."
        ),
        "## Task 7 Step 5b - Selection Pressure and Variability Diagnostics": (
            "## Task 7 Step 5b - Selection Pressure and Variability Diagnostics\n"
            "I report std and CV with the mean because GP variance is high; this avoids over-claiming small differences."
        ),
        "## Task 8 Step 3 - Inspect Aggregated Primitive Frequencies": (
            "## Task 8 Step 3 - Inspect Aggregated Primitive Frequencies\n"
            "Read the aggregated primitive-frequency table to connect the chart trends to concrete numeric values."
        ),
        "## Lecture-Alignment Note": (
            "## Lecture-Alignment Note\n"
            "This section maps each major design choice to Lecture 1-7 and separates algorithmic choices from implementation details."
        ),
        "## Problem2 Difficulty Explanation": (
            "## Problem2 Difficulty Explanation\n"
            "Explain why Problem2 does not reach ideal=0 under the current budget, with reproducible evidence."
        ),
    }

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            cell.source = rewrite_markdown(cell.source, heading_map)

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = cell.source

        if "R2 = PROJECT_ROOT / 'results' / 'part2'" in src and "R2.exists()" in src:
            cell.source = (
                "from pathlib import Path\n"
                "import sys\n"
                "import inspect\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "import matplotlib.pyplot as plt\n"
                "import seaborn as sns\n"
                "from IPython.display import Image, display\n"
                "\n"
                "ROOT = Path('.').resolve()\n"
                "PROJECT_ROOT = next((p for p in [ROOT, *ROOT.parents] if (p / 'ce310').exists()), ROOT)\n"
                "if str(PROJECT_ROOT) not in sys.path:\n"
                "    sys.path.append(str(PROJECT_ROOT))\n"
                "\n"
                "from ce310.gp import (\n"
                "    PRIMITIVE_NAME_BY_CODE,\n"
                "    decode_program_population,\n"
                "    execute,\n"
                "    make_gp_fitness_function,\n"
                ")\n"
                "\n"
                "R2 = PROJECT_ROOT / 'results' / 'part2'\n"
                "FIG = PROJECT_ROOT / 'figures'\n"
                "print('PROJECT_ROOT =', PROJECT_ROOT)\n"
                "print('Part2 results folder exists:', R2.exists())"
            )
        elif "assert (task7['n_runs'] >= 10).all()" in src:
            cell.source = (
                "ok = bool((task7['n_runs'] >= 10).all())\n"
                "print('All conditions have at least 10 runs:', ok)\n"
                "print('Minimum n_runs:', int(task7['n_runs'].min()))\n"
                "assert ok, 'Some conditions have fewer than 10 runs.'\n"
                "task7[['condition','n_runs']].head()"
            )
        elif "diag = task7.copy()" in src and "cv_best" in src:
            cell.source = (
                "diag = task7.copy()\n"
                "diag['cv_best'] = diag['best_of_run_std'] / diag['best_of_run_mean'].abs().replace(0, np.nan)\n"
                "diag_view = diag[['condition','problem','pop_size','tournament_size','best_of_run_mean','best_of_run_std','cv_best']]\n"
                "diag_view = diag_view.sort_values(['problem','best_of_run_mean'], ascending=[True, False])\n"
                "print('Top rows for variability diagnostics:')\n"
                "diag_view.head(12)"
            )
        elif "for _, r in task8.iterrows():" in src and "Missing:" in src:
            cell.source = (
                "for _, r in task8.iterrows():\n"
                "    raw = str(r['plot_file'])\n"
                "    p = Path(raw.replace('\\\\', '/'))\n"
                "    if not p.is_absolute():\n"
                "        p = PROJECT_ROOT / p\n"
                "    print(r['problem'], '->', p)\n"
                "    if p.exists():\n"
                "        display(Image(filename=str(p)))\n"
                "    else:\n"
                "        print('Missing:', p)"
            )


def polish(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    if path.name.lower().startswith("part1"):
        polish_part1(nb)
    else:
        polish_part2(nb)
    nbformat.write(nb, path)
    print(f"Polished: {path}")


def run(paths: Iterable[Path]) -> None:
    for p in paths:
        if p.exists():
            polish(p)
        else:
            print(f"Skip (not found): {p}")


def main() -> None:
    run(find_targets())


if __name__ == "__main__":
    main()

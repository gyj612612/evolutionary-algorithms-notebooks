from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]


def md(text: str):
    return nbf.v4.new_markdown_cell(text)


def code(text: str):
    return nbf.v4.new_code_cell(text)


def build_part1() -> nbf.NotebookNode:
    cells = []
    cells.append(
        md(
            "# CE310 Coursework Part 1 - GA\n\n"
            "This notebook follows an incremental lab-style workflow for Tasks 1-4.\n"
            "Each code cell is introduced by a short rationale and includes direct tests or output checks."
        )
    )
    cells.append(
        code(
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "\n"
            "from ce310.ga import GAConfig, run_ga, tournament_select_index, one_point_crossover, bit_mutate\n"
            "from ce310.part1_problems import (\n"
            "    fitness_one_max,\n"
            "    decode_4bit_positional,\n"
            "    decode_15bit_nonpositional,\n"
            "    fitness_15max,\n"
            "    fitness_soft15max,\n"
            ")\n"
            "\n"
            "RESULT_ROOT = Path('results/part1')\n"
            "RESULT_ROOT.exists()"
        )
    )
    cells.append(
        md(
            "## Task 1 Step A: Validate one-max and initialization assumptions\n\n"
            "Before full GA integration, verify one-max fitness on a hand-crafted population."
        )
    )
    cells.append(
        code(
            "test_pop = np.array([[1,0,1,1],[0,0,0,1],[1,1,1,1]], dtype=np.int8)\n"
            "fitness_one_max(test_pop)"
        )
    )
    cells.append(
        md(
            "## Task 1 Step B: Test selection and operators independently\n\n"
            "Check tournament selection, one-point crossover, and bit mutation in isolation."
        )
    )
    cells.append(
        code(
            "rng = np.random.default_rng(42)\n"
            "fitness = np.array([0.0, 1.0, 2.0, 3.0])\n"
            "sel_idx = tournament_select_index(fitness, tournament_size=3, rng=rng, maximize=True)\n"
            "p1 = np.array([1,1,1,1,1,1], dtype=np.int8)\n"
            "p2 = np.array([0,0,0,0,0,0], dtype=np.int8)\n"
            "child = one_point_crossover(p1, p2, rng)\n"
            "mut = bit_mutate(p1, p_bit=0.5, rng=rng)\n"
            "sel_idx, child, mut"
        )
    )
    cells.append(
        md(
            "## Task 1 Step C: Integrate a full generational GA loop on one-max\n\n"
            "Run a short trial to confirm the framework improves fitness over generations."
        )
    )
    cells.append(
        code(
            "cfg = GAConfig(\n"
            "    pop_size=80,\n"
            "    genome_length=100,\n"
            "    generations=30,\n"
            "    tournament_size=3,\n"
            "    p_clone=0.2,\n"
            "    p_crossover=0.7,\n"
            "    p_mutation_operator=0.1,\n"
            "    p_bit_mutation=1/100,\n"
            "    seed=123,\n"
            ")\n"
            "res = run_ga(cfg, fitness_one_max)\n"
            "res.history[['generation','best_fitness','mean_fitness']].head(), res.history[['generation','best_fitness','mean_fitness']].tail()"
        )
    )
    cells.append(
        code(
            "plt.figure(figsize=(7,4))\n"
            "plt.plot(res.history['generation'], res.history['best_fitness'], label='best')\n"
            "plt.plot(res.history['generation'], res.history['mean_fitness'], label='mean')\n"
            "plt.xlabel('Generation'); plt.ylabel('Fitness'); plt.title('Task1 OneMax Trial')\n"
            "plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 2 Step A: Validate genotype-to-phenotype decoding\n\n"
            "Test both required encodings: 4-bit positional and 15-bit non-positional."
        )
    )
    cells.append(
        code(
            "pop4 = np.array([[1,1,1,1, 0,0,0,0], [1,0,0,0, 1,1,0,0]], dtype=np.int8)\n"
            "dec4 = decode_4bit_positional(pop4, length_l=2)\n"
            "\n"
            "pop15 = np.array([([1]*15)+([0]*15)], dtype=np.int8)\n"
            "dec15 = decode_15bit_nonpositional(pop15, length_l=2)\n"
            "dec4, dec15"
        )
    )
    cells.append(
        md(
            "## Task 2 Step B: Validate 15-max and soft-15-max fitness functions\n\n"
            "Confirm expected output ranges and behavior on deterministic examples."
        )
    )
    cells.append(
        code(
            "f15 = fitness_15max(pop4, length_l=2, encoding='4bit')\n"
            "fsoft = fitness_soft15max(pop4, length_l=2, encoding='4bit')\n"
            "f15, fsoft"
        )
    )
    cells.append(
        md(
            "## Task 3: Parameter tuning and full experiment results\n\n"
            "Load generated experiment outputs (10 runs per main condition, 50 generations each)."
        )
    )
    cells.append(
        code(
            "tuning = pd.read_csv(RESULT_ROOT / 'task3_tuning' / 'tuning_summary.csv')\n"
            "tuning.head(10)"
        )
    )
    cells.append(
        code(
            "task3 = pd.read_csv(RESULT_ROOT / 'task3_main' / 'task3_summary.csv')\n"
            "task3"
        )
    )
    cells.append(
        code(
            "plt.figure(figsize=(9,4))\n"
            "plt.bar(task3['condition'], task3['best_of_run_mean'])\n"
            "plt.xticks(rotation=45, ha='right')\n"
            "plt.ylabel('Mean best-of-run fitness')\n"
            "plt.title('Task3 Results Across Encodings/L/Objectives')\n"
            "plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 4: Deceptive trap comparison\n\n"
            "Compare deceptive soft-15 trap performance with corresponding soft-15-max settings to show slowdown/local-optimum behavior."
        )
    )
    cells.append(
        code(
            "task4 = pd.read_csv(RESULT_ROOT / 'task4_trap' / 'task4_summary.csv')\n"
            "base_soft = task3[task3['objective']=='soft15max'][['encoding','L','best_of_run_mean','ideal_found_fraction']].rename(columns={'best_of_run_mean':'mean_soft15max','ideal_found_fraction':'ideal_frac_soft15max'})\n"
            "cmp = task4.merge(base_soft, on=['encoding','L'], how='left')\n"
            "cmp['delta_trap_minus_soft15max'] = cmp['best_of_run_mean'] - cmp['mean_soft15max']\n"
            "cmp"
        )
    )
    cells.append(
        code(
            "plt.figure(figsize=(7,4))\n"
            "labels = cmp['condition']\n"
            "x = np.arange(len(labels))\n"
            "w = 0.38\n"
            "plt.bar(x-w/2, cmp['mean_soft15max'], width=w, label='soft-15-max')\n"
            "plt.bar(x+w/2, cmp['best_of_run_mean'], width=w, label='soft-15-trap')\n"
            "plt.xticks(x, labels, rotation=35, ha='right')\n"
            "plt.ylabel('Mean best-of-run')\n"
            "plt.title('Task4: soft-15-max vs soft-15-trap')\n"
            "plt.legend(); plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Part 1 conclusions\n\n"
            "- The GA framework and all required operators are implemented and independently tested.\n"
            "- 4-bit positional encoding strongly outperforms 15-bit non-positional for strict 15-max.\n"
            "- soft-15-max provides smoother gradients and near-optimal averages, especially for 4-bit.\n"
            "- The integer-space soft-15 trap demonstrates deceptive behavior versus soft-15-max, including reduced ideal-hit rates.\n"
            "- Full logs are available under `results/part1/`."
        )
    )
    return nbf.v4.new_notebook(cells=cells)


def build_part2() -> nbf.NotebookNode:
    cells = []
    cells.append(
        md(
            "# CE310 Coursework Part 2 - GP (Stack-Based)\n\n"
            "This notebook incrementally builds from Part 1 GA to a stack-based GP system for Tasks 5-8."
        )
    )
    cells.append(
        code(
            "from pathlib import Path\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "from IPython.display import Image, display\n"
            "\n"
            "from ce310.gp import (\n"
            "    execute,\n"
            "    decode_program_population,\n"
            "    make_gp_fitness_function,\n"
            "    PRIMITIVE_NAME_BY_CODE,\n"
            ")\n"
            "\n"
            "RESULT_ROOT = Path('results/part2')\n"
            "RESULT_ROOT.exists()"
        )
    )
    cells.append(
        md(
            "## Task 5 Step A: Validate representation and decode logic\n\n"
            "Programs are fixed-length instruction sequences decoded from binary chromosomes."
        )
    )
    cells.append(
        code(
            "PRIMITIVE_NAME_BY_CODE"
        )
    )
    cells.append(
        code(
            "chrom = np.array([[1,0,1, 1,1,1, 0,0,0]], dtype=np.int8)  # [5,7,0]\n"
            "decode_program_population(chrom, program_length=3, encoding='3bit')"
        )
    )
    cells.append(
        md(
            "## Task 6 Step A: Validate provided interpreter behavior\n\n"
            "The coursework example requires `execute([5,1,2], 3) = 4`."
        )
    )
    cells.append(
        code(
            "execute(np.array([5,1,2], dtype=np.int16), 3.0)"
        )
    )
    cells.append(
        md(
            "## Task 6 Step B: Validate both fitness functions\n\n"
            "Problem1 maximizes separation between outputs at x=1 and x=-1.\n"
            "Problem2 minimizes absolute error to a fixed polynomial across 21 fitness cases."
        )
    )
    cells.append(
        code(
            "f1 = make_gp_fitness_function(program_length=30, encoding='3bit', problem='problem1')\n"
            "f2 = make_gp_fitness_function(program_length=30, encoding='3bit', problem='problem2')\n"
            "dummy = np.random.default_rng(1).integers(0,2,size=(4,90),dtype=np.int8)\n"
            "fit1, meta1 = f1(dummy)\n"
            "fit2, meta2 = f2(dummy)\n"
            "meta1, meta2, fit1[:3], fit2[:3]"
        )
    )
    cells.append(
        md(
            "## Task 5 result snapshot: encoding comparison\n\n"
            "Load recorded results for 3-bit and 7-bit encodings."
        )
    )
    cells.append(
        code(
            "enc = pd.read_csv(RESULT_ROOT / 'task5_encoding_comparison' / 'encoding_comparison_summary.csv')\n"
            "enc"
        )
    )
    cells.append(
        md(
            "## Task 7: 10-run experiments, 50 generations, no early stopping\n\n"
            "Inspect full experiment matrix by population size and tournament size."
        )
    )
    cells.append(
        code(
            "task7 = pd.read_csv(RESULT_ROOT / 'task7_experiments' / 'task7_summary.csv')\n"
            "task7"
        )
    )
    cells.append(
        code(
            "p1 = task7[task7['problem']=='problem1'].pivot(index='pop_size', columns='tournament_size', values='best_of_run_mean')\n"
            "p2 = task7[task7['problem']=='problem2'].pivot(index='pop_size', columns='tournament_size', values='best_of_run_mean')\n"
            "p1, p2"
        )
    )
    cells.append(
        code(
            "fig, axes = plt.subplots(1,2, figsize=(11,4), sharex=True)\n"
            "for ax, problem, df in [(axes[0],'problem1',p1),(axes[1],'problem2',p2)]:\n"
            "    for t in df.columns:\n"
            "        ax.plot(df.index, df[t], marker='o', label=f'T={t}')\n"
            "    ax.set_title(problem)\n"
            "    ax.set_xlabel('Population size')\n"
            "    ax.set_ylabel('Mean best-of-run fitness')\n"
            "    ax.grid(alpha=0.3)\n"
            "    ax.legend()\n"
            "plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 7 computational effort\n\n"
            "Use stored per-run execute-call counters to compare cost across configurations."
        )
    )
    cells.append(
        code(
            "import glob\n"
            "rows = []\n"
            "for path in glob.glob('results/part2/task7_experiments/*/runs_summary.csv'):\n"
            "    df = pd.read_csv(path)\n"
            "    cond = Path(path).parent.name\n"
            "    rows.append({'condition': cond, 'mean_total_execute_calls': df.get('total_execute_calls', pd.Series([np.nan])).mean()})\n"
            "cost = pd.DataFrame(rows).sort_values('mean_total_execute_calls', ascending=False)\n"
            "cost.head(10)"
        )
    )
    cells.append(
        md(
            "## Task 8: primitive frequency evolution\n\n"
            "Show primitive frequency trends for selected best configurations per problem."
        )
    )
    cells.append(
        code(
            "task8 = pd.read_csv(RESULT_ROOT / 'task8_primitives' / 'task8_selected_conditions.csv')\n"
            "task8"
        )
    )
    cells.append(
        code(
            "for _, r in task8.iterrows():\n"
            "    p = Path(r['plot_file'])\n"
            "    if p.exists():\n"
            "        print(r['problem'], '->', p)\n"
            "        display(Image(filename=str(p)))\n"
            "    else:\n"
            "        print('Missing plot:', p)"
        )
    )
    cells.append(
        md(
            "## Part 2 conclusions\n\n"
            "- GA framework from Part 1 was reused with binary representation and independent mutation operator.\n"
            "- The provided stack interpreter was integrated exactly and tested with coursework reference example.\n"
            "- Task7 protocol is satisfied: 10 runs per condition, 50 generations, per-generation and cross-run statistics logged.\n"
            "- Larger populations generally improve fitness on both problems but increase computational cost.\n"
            "- Primitive frequencies shift away from uniform initialization, with trends depending on problem and selection pressure.\n"
            "- Full traceability is available under `results/part2/`."
        )
    )
    return nbf.v4.new_notebook(cells=cells)


def main() -> None:
    part1 = build_part1()
    part2 = build_part2()
    nbf.write(part1, ROOT / "Part1.ipynb")
    nbf.write(part2, ROOT / "Part2.ipynb")
    print("Generated Part1.ipynb and Part2.ipynb")


if __name__ == "__main__":
    main()

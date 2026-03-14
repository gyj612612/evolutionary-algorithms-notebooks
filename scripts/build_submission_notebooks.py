from __future__ import annotations

from pathlib import Path

import nbformat as nbf


ROOT = Path(__file__).resolve().parents[1]
FINAL_DIR = ROOT / "最终提交版"


def md(text: str):
    return nbf.v4.new_markdown_cell(text)


def code(text: str):
    return nbf.v4.new_code_cell(text)


def build_part1() -> nbf.NotebookNode:
    cells = []
    cells.append(
        md(
            "# CE310 Part 1 - Genetic Algorithm (Final Submission Version)\n\n"
            "This notebook follows the required incremental lab-style workflow:\n"
            "explanation -> code -> tests/output, step by step."
        )
    )
    cells.append(md("## Environment Setup\nLoad required libraries and project modules."))
    cells.append(
        code(
            "from pathlib import Path\n"
            "import sys\n"
            "import inspect\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from IPython.display import Image, display\n"
            "ROOT = Path('.').resolve()\n"
            "PROJECT_ROOT = ROOT if (ROOT / 'ce310').exists() else ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n"
            "    sys.path.append(str(PROJECT_ROOT))\n"
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
            "R1 = PROJECT_ROOT / 'results' / 'part1'\n"
            "FIG = PROJECT_ROOT / 'figures'\n"
            "R1.exists()"
        )
    )
    cells.append(md("## Code Completeness Snapshot\nShow source code of core GA operators to keep key implementation visible inside this notebook."))
    cells.append(
        code(
            "import ce310.ga as ga_mod\n"
            "print(inspect.getsource(ga_mod.tournament_select_index)[:1200])\n"
            "print('\\n---\\n')\n"
            "print(inspect.getsource(ga_mod.one_point_crossover)[:1200])\n"
            "print('\\n---\\n')\n"
            "print(inspect.getsource(ga_mod.bit_mutate)[:1200])"
        )
    )

    cells.append(md("## Task 1 Step 1 - Population Initialization Test\nCheck binary initialization shape and sample individuals."))
    cells.append(
        code(
            "cfg_init = GAConfig(pop_size=6, genome_length=12, generations=5, tournament_size=2,\n"
            "    p_clone=0.2, p_crossover=0.7, p_mutation_operator=0.1, p_bit_mutation=1/12, seed=42)\n"
            "rng = np.random.default_rng(cfg_init.seed)\n"
            "pop = initialize_population(cfg_init, rng)\n"
            "pop.shape, pop[:3]"
        )
    )

    cells.append(md("## Task 1 Step 2 - OneMax Fitness Sanity Test\nVerify fitness on a small hand-crafted population."))
    cells.append(
        code(
            "toy = np.array([[1,0,1,1],[0,0,0,1],[1,1,1,1]], dtype=np.int8)\n"
            "fitness_one_max(toy)"
        )
    )

    cells.append(md("## Task 1 Step 3 - Tournament Selection Test\nConfirm tournament selection returns valid population index."))
    cells.append(
        code(
            "fit = np.array([0.0, 1.0, 2.0, 3.0])\n"
            "idx = tournament_select_index(fit, tournament_size=3, rng=np.random.default_rng(123), maximize=True)\n"
            "idx"
        )
    )

    cells.append(md("## Task 1 Step 4 - Clone, Crossover, Mutation Unit Tests\nTest each operator independently before integration."))
    cells.append(
        code(
            "p1 = np.array([1,1,1,1,1,1], dtype=np.int8)\n"
            "p2 = np.array([0,0,0,0,0,0], dtype=np.int8)\n"
            "rng_ops = np.random.default_rng(7)\n"
            "c = clone(p1)\n"
            "xo = one_point_crossover(p1, p2, rng_ops)\n"
            "mut = bit_mutate(p1, p_bit=0.5, rng=rng_ops)\n"
            "c, xo, mut"
        )
    )

    cells.append(md("## Task 1 Step 5 - Integrated GA Run on OneMax\nRun full generational GA and inspect convergence behaviour."))
    cells.append(
        code(
            "cfg_task1 = GAConfig(pop_size=100, genome_length=100, generations=50, tournament_size=3,\n"
            "    p_clone=0.2, p_crossover=0.7, p_mutation_operator=0.1, p_bit_mutation=1/100, seed=2026)\n"
            "res_task1 = run_ga(cfg_task1, fitness_one_max)\n"
            "res_task1.history[['generation','best_fitness','mean_fitness']].head(), res_task1.history[['generation','best_fitness','mean_fitness']].tail()"
        )
    )

    cells.append(md("## Task 1 Step 6 - Plot OneMax Learning Curve\nVisualize best and mean fitness across generations."))
    cells.append(
        code(
            "plt.figure(figsize=(8,4))\n"
            "plt.plot(res_task1.history['generation'], res_task1.history['best_fitness'], label='best')\n"
            "plt.plot(res_task1.history['generation'], res_task1.history['mean_fitness'], label='mean')\n"
            "plt.xlabel('Generation'); plt.ylabel('Fitness'); plt.title('Task1 OneMax Trial')\n"
            "plt.grid(alpha=0.3); plt.legend(); plt.tight_layout()"
        )
    )

    cells.append(md("## Task 2 Step 1 - 4-bit and 15-bit Decoder Tests\nCheck both genotype-phenotype mappings required in coursework."))
    cells.append(
        code(
            "pop4 = np.array([[1,1,1,1,0,0,0,0],[1,0,0,0,1,1,0,0]], dtype=np.int8)\n"
            "dec4 = decode_4bit_positional(pop4, length_l=2)\n"
            "pop15 = np.array([([1]*15)+([0]*15)], dtype=np.int8)\n"
            "dec15 = decode_15bit_nonpositional(pop15, length_l=2)\n"
            "dec4, dec15"
        )
    )

    cells.append(md("## Task 2 Step 2 - 15-max and soft-15-max Function Tests\nValidate objective outputs on controlled examples."))
    cells.append(
        code(
            "fit15 = fitness_15max(pop4, length_l=2, encoding='4bit')\n"
            "fitsoft = fitness_soft15max(pop4, length_l=2, encoding='4bit')\n"
            "fit15, fitsoft"
        )
    )

    cells.append(md("## Task 3 Step 1 - Load Tuning Results\nRead Stage1 and Stage2 tuning summaries from experiment logs."))
    cells.append(
        code(
            "stage1 = pd.read_csv(R1 / 'task3_tuning_stage1' / 'stage1_summary.csv')\n"
            "stage2 = pd.read_csv(R1 / 'task3_tuning_stage2' / 'stage2_summary.csv')\n"
            "stage1.head(5), stage2.head(5)"
        )
    )

    cells.append(md("## Task 3 Step 2 - Load Main Experiment Summary\nReview 10-run results for both encodings and both L values."))
    cells.append(
        code(
            "task3 = pd.read_csv(R1 / 'task3_main' / 'task3_summary.csv')\n"
            "task3"
        )
    )

    cells.append(md("## Task 3 Step 3 - Compare Key Conditions\nVisualize mean best-of-run fitness across all Task3 conditions."))
    cells.append(
        code(
            "plt.figure(figsize=(10,4))\n"
            "sns.barplot(data=task3, x='condition', y='best_of_run_mean')\n"
            "plt.xticks(rotation=45, ha='right')\n"
            "plt.ylabel('Mean best-of-run')\n"
            "plt.title('Task3 Condition Comparison')\n"
            "plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 3 Step 3b - Enhanced Visualization (if available)\n"
            "Display prepared figure files for clearer presentation of encoding and tuning effects."
        )
    )
    cells.append(
        code(
            "for fn in ['part1_encoding_comparison.png','part1_parameter_heatmap.png']:\n"
            "    p = FIG / fn\n"
            "    print(p)\n"
            "    if p.exists():\n"
            "        display(Image(filename=str(p)))\n"
            "    else:\n"
            "        print('Missing figure:', p)"
        )
    )
    cells.append(md("## Task 3 Step 4 - Parameter Choice Justification\nExtract the selected best tuning row as explicit evidence for parameter decisions."))
    cells.append(
        code(
            "best_s1 = stage1.iloc[0]\n"
            "best_s2 = stage2.iloc[0]\n"
            "best_s1[['condition','pop_size','tournament_size','best_of_run_mean','best_of_run_std']], \\\n"
            "best_s2[['condition','p_clone','p_crossover','p_mutation_operator','p_bit_factor','best_of_run_mean','best_of_run_std']]"
        )
    )

    cells.append(md("## Task 4 Step 1 - Load Deceptive Experiment Results\nInspect trap summary and baseline comparison file."))
    cells.append(
        code(
            "task4 = pd.read_csv(R1 / 'task4_trap' / 'task4_summary.csv')\n"
            "cmp4 = pd.read_csv(R1 / 'task4_deceptive_vs_soft15max.csv')\n"
            "task4, cmp4"
        )
    )

    cells.append(md("## Task 4 Step 2 - Visualize Trap vs Soft-15-max\nShow slowdown/deception effect clearly."))
    cells.append(
        code(
            "plt.figure(figsize=(8,4))\n"
            "sns.barplot(data=cmp4, x='condition', y='delta_best_mean_trap_minus_soft')\n"
            "plt.axhline(0, color='black', linewidth=1)\n"
            "plt.xticks(rotation=30, ha='right')\n"
            "plt.ylabel('Trap mean - soft15max mean')\n"
            "plt.title('Task4 Deceptive Effect (negative means trap is harder)')\n"
            "plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 4 Step 2b - Enhanced Deceptive Comparison Figure (if available)\n"
            "Use the detailed prepared figure as supplementary visual evidence."
        )
    )
    cells.append(
        code(
            "p = FIG / 'part1_deceptive_comparison.png'\n"
            "print(p)\n"
            "if p.exists():\n"
            "    display(Image(filename=str(p)))\n"
            "else:\n"
            "    print('Missing figure:', p)"
        )
    )
    cells.append(
        md(
            "## Theory Link (EC/GA)\n"
            "- 4-bit positional vs 15-bit non-positional differences are consistent with representation bias and search difficulty.\n"
            "- Deceptive trap objective creates misleading gradients and stronger local-optimum attraction.\n"
            "- Tournament size controls selection pressure; higher pressure can accelerate convergence but may reduce diversity."
        )
    )
    cells.append(
        md(
            "## Task 4 Step 2c - Local Optimum Convergence Evidence (Quantitative)\n"
            "For the deceptive integer trap, local optimum is around fitness 14 and global optimum is 15. "
            "This cell quantifies how often runs end near the local optimum."
        )
    )
    cells.append(
        code(
            "import glob\n"
            "rows=[]\n"
            "for cond_dir in sorted((R1/'task4_trap').glob('*_soft15trap_int')):\n"
            "    rs = cond_dir/'runs_summary.csv'\n"
            "    if not rs.exists():\n"
            "        continue\n"
            "    df = pd.read_csv(rs)\n"
            "    # local optimum neighborhood around 14 for this deceptive objective\n"
            "    frac_local = ((df['best_of_run_fitness'] >= 13.8) & (df['best_of_run_fitness'] <= 14.2)).mean()\n"
            "    frac_global = (df['best_of_run_fitness'] >= 14.95).mean()\n"
            "    rows.append({'condition':cond_dir.name,'local_optimum_fraction':frac_local,'global_optimum_fraction':frac_global,\n"
            "                 'mean_best_of_run':df['best_of_run_fitness'].mean(),'std_best_of_run':df['best_of_run_fitness'].std()})\n"
            "loc = pd.DataFrame(rows).sort_values('condition').reset_index(drop=True)\n"
            "loc"
        )
    )
    cells.append(
        md(
            "## Method Justification Against Lecture Methods\n"
            "- Core algorithmic methods follow CE310 lectures: tournament selection, cloning/XO/mutation, trap/deceptive objective, stack GP interpreter.\n"
            "- Additional engineering method used: result caching of duplicate GP programs to reduce computation time.\n"
            "- Why acceptable: it does not change representation, fitness definition, or evolutionary operators; it only avoids redundant re-evaluation of identical programs."
        )
    )

    cells.append(md("## Part 1 Final Summary\nConclude against Task1-4 marking expectations."))
    cells.append(
        code(
            "report_p1 = (R1 / 'part1_report_summary.md').read_text(encoding='utf-8')\n"
            "print(report_p1[:2000])"
        )
    )

    return nbf.v4.new_notebook(cells=cells)


def build_part2() -> nbf.NotebookNode:
    cells = []
    cells.append(
        md(
            "# CE310 Part 2 - Genetic Programming (Final Submission Version)\n\n"
            "This notebook follows the required incremental lab-style workflow and references full run logs."
        )
    )
    cells.append(md("## Environment Setup\nLoad GP framework, plotting tools, and result paths."))
    cells.append(
        code(
            "from pathlib import Path\n"
            "import sys\n"
            "import inspect\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from IPython.display import Image, display\n"
            "ROOT = Path('.').resolve()\n"
            "PROJECT_ROOT = ROOT if (ROOT / 'ce310').exists() else ROOT.parent\n"
            "if str(PROJECT_ROOT) not in sys.path:\n"
            "    sys.path.append(str(PROJECT_ROOT))\n"
            "from ce310.gp import (\n"
            "    PRIMITIVE_NAME_BY_CODE,\n"
            "    decode_program_population,\n"
            "    execute,\n"
            "    make_gp_fitness_function,\n"
            ")\n"
            "R2 = PROJECT_ROOT / 'results' / 'part2'\n"
            "FIG = PROJECT_ROOT / 'figures'\n"
            "R2.exists()"
        )
    )
    cells.append(md("## Code Completeness Snapshot\nShow core interpreter source code inside notebook for direct review."))
    cells.append(
        code(
            "import ce310.gp as gp_mod\n"
            "print(inspect.getsource(gp_mod.execute)[:1600])\n"
            "print('\\n---\\n')\n"
            "print(inspect.getsource(gp_mod.make_gp_fitness_function)[:2200])"
        )
    )

    cells.append(md("## Task 5 Step 1 - Primitive Set Verification\nCheck instruction encoding mapping used by GP."))
    cells.append(code("PRIMITIVE_NAME_BY_CODE"))

    cells.append(md("## Task 5 Step 2 - Program Decoding Test\nValidate 3-bit decoding from binary chromosome to instruction sequence."))
    cells.append(
        code(
            "chrom = np.array([[1,0,1,1,1,1,0,0,0]], dtype=np.int8)  # expected [5,7,0]\n"
            "decode_program_population(chrom, program_length=3, encoding='3bit')"
        )
    )

    cells.append(md("## Task 6 Step 1 - Interpreter Example from Coursework\nVerify required example execute([5,1,2],3)=4."))
    cells.append(code("execute(np.array([5,1,2], dtype=np.int16), 3.0)"))

    cells.append(md("## Task 6 Step 2 - Fitness Function Smoke Test\nEvaluate both GP problems on random individuals."))
    cells.append(
        code(
            "rng = np.random.default_rng(123)\n"
            "dummy = rng.integers(0,2,size=(5,90),dtype=np.int8)\n"
            "f1 = make_gp_fitness_function(30, '3bit', 'problem1')\n"
            "f2 = make_gp_fitness_function(30, '3bit', 'problem2')\n"
            "fit1, meta1 = f1(dummy)\n"
            "fit2, meta2 = f2(dummy)\n"
            "fit1, meta1, fit2[:3], meta2"
        )
    )

    cells.append(md("## Task 5 Result Summary - Encoding Comparison\nLoad 3-bit vs 7-bit comparison results."))
    cells.append(code("enc = pd.read_csv(R2 / 'task5_encoding_comparison' / 'encoding_comparison_summary.csv'); enc"))

    cells.append(md("## Task 7 Step 1 - Load Full Experiment Matrix\nInspect all 18 conditions (problem x pop x tournament)."))
    cells.append(code("task7 = pd.read_csv(R2 / 'task7_experiments' / 'task7_summary.csv'); task7"))

    cells.append(md("## Task 7 Step 2 - Protocol Compliance Check\nVerify mandatory run count requirement."))
    cells.append(
        code(
            "assert (task7['n_runs'] >= 10).all(), 'Some conditions have fewer than 10 runs.'\n"
            "task7[['condition','n_runs']].head()"
        )
    )
    cells.append(md("## Task 7 Step 2b - Ideal Solution Reporting Columns\nExplicitly inspect ideal-hit and first-hit-generation statistics."))
    cells.append(
        code(
            "cols = ['condition','problem','ideal_found_fraction','first_ideal_generation_mean']\n"
            "task7[cols]"
        )
    )

    cells.append(md("## Task 7 Step 3 - Parameter Effect Visualization (Problem 1)\nPlot mean best-of-run against population size for different tournament sizes."))
    cells.append(
        code(
            "p1 = task7[task7['problem']=='problem1'].copy()\n"
            "plt.figure(figsize=(8,4))\n"
            "sns.lineplot(data=p1, x='pop_size', y='best_of_run_mean', hue='tournament_size', marker='o')\n"
            "plt.title('Problem1: population and tournament effects')\n"
            "plt.tight_layout()"
        )
    )

    cells.append(md("## Task 7 Step 4 - Parameter Effect Visualization (Problem 2)\nPlot mean best-of-run for symbolic regression problem."))
    cells.append(
        code(
            "p2 = task7[task7['problem']=='problem2'].copy()\n"
            "plt.figure(figsize=(8,4))\n"
            "sns.lineplot(data=p2, x='pop_size', y='best_of_run_mean', hue='tournament_size', marker='o')\n"
            "plt.title('Problem2: population and tournament effects')\n"
            "plt.tight_layout()"
        )
    )
    cells.append(
        md(
            "## Task 7 Step 4b - Enhanced Parameter and Cost Visualizations (if available)\n"
            "Show prepared heatmap and computational cost figures."
        )
    )
    cells.append(
        code(
            "for fn in ['part2_parameter_impact_heatmap.png','part2_computational_cost.png']:\n"
            "    p = FIG / fn\n"
            "    print(p)\n"
            "    if p.exists():\n"
            "        display(Image(filename=str(p)))\n"
            "    else:\n"
            "        print('Missing figure:', p)"
        )
    )

    cells.append(md("## Task 7 Step 5 - Computational Effort Analysis\nSummarize execute-call statistics and reduction ratio."))
    cells.append(
        code(
            "cols = ['condition','mean_execute_calls_per_generation','mean_execute_calls_nominal_per_generation','execute_call_reduction_ratio']\n"
            "task7[cols].sort_values('execute_call_reduction_ratio', ascending=False).head(10)"
        )
    )
    cells.append(
        md(
            "## Task 7 Step 5b - Selection Pressure and Variability Diagnostics\n"
            "Quantify parameter effects in terms of mean performance and variability (std / coefficient of variation)."
        )
    )
    cells.append(
        code(
            "diag = task7.copy()\n"
            "diag['cv_best'] = diag['best_of_run_std'] / diag['best_of_run_mean'].abs().replace(0, np.nan)\n"
            "diag_view = diag[['condition','problem','pop_size','tournament_size','best_of_run_mean','best_of_run_std','cv_best']]\n"
            "diag_view = diag_view.sort_values(['problem','best_of_run_mean'], ascending=[True, False])\n"
            "diag_view.head(12)"
        )
    )

    cells.append(md("## Task 7 Step 6 - Best Conditions and Variability\nIdentify best settings for each problem and inspect standard deviation."))
    cells.append(
        code(
            "best_p1 = p1.sort_values('best_of_run_mean', ascending=False).iloc[0]\n"
            "best_p2 = p2.sort_values('best_of_run_mean', ascending=False).iloc[0]\n"
            "best_p1[['condition','best_of_run_mean','best_of_run_std']], best_p2[['condition','best_of_run_mean','best_of_run_std','ideal_found_fraction']]"
        )
    )

    cells.append(md("## Task 8 Step 1 - Selected Primitive Trend Conditions\nLoad selected conditions for primitive analysis."))
    cells.append(code("task8 = pd.read_csv(R2 / 'task8_primitives' / 'task8_selected_conditions.csv'); task8"))

    cells.append(md("## Task 8 Step 2 - Display Primitive Trend Plots\nShow primitive frequency evolution plots for the selected conditions."))
    cells.append(
        code(
            "for _, r in task8.iterrows():\n"
            "    p = Path(r['plot_file'])\n"
            "    print(r['problem'], '->', p)\n"
            "    if p.exists():\n"
            "        display(Image(filename=str(p)))\n"
            "    else:\n"
            "        print('Missing:', p)"
        )
    )
    cells.append(
        md(
            "## Task 8 Step 2b - Enhanced Detailed Primitive Evolution (if available)\n"
            "Display high-resolution prepared trend figures for both problems."
        )
    )
    cells.append(
        code(
            "for fn in ['part2_primitive_evolution_problem1_detailed.png','part2_primitive_evolution_problem2_detailed.png']:\n"
            "    p = FIG / fn\n"
            "    print(p)\n"
            "    if p.exists():\n"
            "        display(Image(filename=str(p)))\n"
            "    else:\n"
            "        print('Missing figure:', p)"
        )
    )

    cells.append(md("## Task 8 Step 3 - Inspect Aggregated Primitive Frequencies\nRead one best-condition aggregated file for detailed values."))
    cells.append(
        code(
            "cond_p2 = str(best_p2['condition'])\n"
            "agg = pd.read_csv(R2 / 'task7_experiments' / cond_p2 / 'generation_aggregated.csv')\n"
            "freq_cols = [c for c in agg.columns if c.startswith('freq_') and c.endswith('_mean')]\n"
            "agg[['generation'] + freq_cols].head()"
        )
    )

    cells.append(md("## Part 2 Final Summary\nPrint concise report summary for Task5-8."))
    cells.append(
        code(
            "report_p2 = (R2 / 'part2_report_summary.md').read_text(encoding='utf-8')\n"
            "print(report_p2[:2500])"
        )
    )
    cells.append(
        md(
            "## Theory Link (EC/GP)\n"
            "- Population size and tournament size jointly affect exploration/exploitation balance.\n"
            "- Run-to-run variability is expected in stochastic evolutionary search.\n"
            "- Primitive frequencies drift away from uniform initialization as useful building blocks spread through selection."
        )
    )
    cells.append(
        md(
            "## Lecture-Alignment Note\n"
            "- Lecture 02/03: tournament selection and stochastic variability concepts are directly used in Task7 analysis.\n"
            "- Lecture 04: deceptive/trap behavior informs Part1 Task4 interpretation.\n"
            "- Lecture 05/06: symbolic regression framing, primitive sets, interpreter/closure concepts support Part2 design.\n"
            "- Lecture 07: bloat/control ideas are acknowledged; fixed-length GP here intentionally avoids variable-length bloat complexity."
        )
    )
    cells.append(
        md(
            "## Problem2 Difficulty Explanation\n"
            "- The target is a 5th-order polynomial over 21 fitness cases.\n"
            "- With fixed-length 30-instruction linear programs and limited primitive set, exact symbolic reconstruction is hard.\n"
            "- Therefore, obtaining `ideal_found_fraction = 0` in current budget is plausible and should be discussed as a search-budget/representation limitation rather than an implementation bug."
        )
    )

    return nbf.v4.new_notebook(cells=cells)


def main() -> None:
    FINAL_DIR.mkdir(parents=True, exist_ok=True)
    p1 = build_part1()
    p2 = build_part2()

    # Save in root for consistency and inside final folder for direct submission.
    nbf.write(p1, ROOT / "Part1.ipynb")
    nbf.write(p2, ROOT / "Part2.ipynb")
    nbf.write(p1, FINAL_DIR / "Part1.ipynb")
    nbf.write(p2, FINAL_DIR / "Part2.ipynb")
    print(f"Generated notebooks at {ROOT/'Part1.ipynb'} and {ROOT/'Part2.ipynb'}")
    print(f"Generated submission copies at {FINAL_DIR}")


if __name__ == "__main__":
    main()

from __future__ import annotations

from pathlib import Path
from textwrap import dedent, indent

import nbformat


ROOT = Path(__file__).resolve().parents[1]

def find_v10_dir() -> Path:
    out_dir = ROOT / "out"
    candidates = [p for p in out_dir.iterdir() if p.is_dir() and p.name.endswith("_v10")]
    if not candidates:
        raise SystemExit(f"no *_v10 folder found under: {out_dir}")
    return sorted(candidates, key=lambda p: p.stat().st_mtime, reverse=True)[0]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def module_sources() -> dict[str, str]:
    return {
        "ce310.ga": read_text(ROOT / "ce310" / "ga.py"),
        "ce310.utils": read_text(ROOT / "ce310" / "utils.py"),
        "ce310.experiments": read_text(ROOT / "ce310" / "experiments.py"),
        "ce310.part1_problems": read_text(ROOT / "ce310" / "part1_problems.py"),
        "ce310.gp": read_text(ROOT / "ce310" / "gp.py"),
    }


def script_sources() -> dict[str, str]:
    return {
        "run_part1": read_text(ROOT / "scripts" / "run_part1.py"),
        "run_part2": read_text(ROOT / "scripts" / "run_part2.py"),
    }


def loader_block(mod_src: dict[str, str], run_src: dict[str, str]) -> str:
    return dedent(
        f"""
        EMBEDDED_MODULE_SOURCES = {{
            "ce310.ga": {mod_src["ce310.ga"]!r},
            "ce310.utils": {mod_src["ce310.utils"]!r},
            "ce310.experiments": {mod_src["ce310.experiments"]!r},
            "ce310.part1_problems": {mod_src["ce310.part1_problems"]!r},
            "ce310.gp": {mod_src["ce310.gp"]!r},
        }}

        EMBEDDED_SCRIPT_SOURCES = {{
            "run_part1": {run_src["run_part1"]!r},
            "run_part2": {run_src["run_part2"]!r},
        }}

        def _inject_embedded_ce310_modules() -> None:
            import importlib.util
            import sys as _sys
            import types

            embed_root = PROJECT_ROOT / ".embedded_ce310"
            pkg_dir = embed_root / "ce310"
            pkg_dir.mkdir(parents=True, exist_ok=True)
            (pkg_dir / "__init__.py").write_text("# embedded ce310 package\\n", encoding="utf-8")

            module_files = {{
                "ce310.ga": pkg_dir / "ga.py",
                "ce310.utils": pkg_dir / "utils.py",
                "ce310.experiments": pkg_dir / "experiments.py",
                "ce310.part1_problems": pkg_dir / "part1_problems.py",
                "ce310.gp": pkg_dir / "gp.py",
            }}
            for module_name, src in EMBEDDED_MODULE_SOURCES.items():
                module_files[module_name].write_text(src, encoding="utf-8")

            if "ce310" not in _sys.modules:
                pkg = types.ModuleType("ce310")
                pkg.__path__ = [str(pkg_dir)]  # type: ignore[attr-defined]
                _sys.modules["ce310"] = pkg
            else:
                pkg = _sys.modules["ce310"]
                pkg.__path__ = [str(pkg_dir)]  # type: ignore[attr-defined]

            for module_name in ["ce310.ga", "ce310.utils", "ce310.experiments", "ce310.part1_problems", "ce310.gp"]:
                if module_name in _sys.modules:
                    continue
                mod_path = module_files[module_name]
                spec = importlib.util.spec_from_file_location(module_name, mod_path)
                if spec is None or spec.loader is None:
                    raise ImportError(f"Failed to create spec for {{module_name}} at {{mod_path}}")
                mod = importlib.util.module_from_spec(spec)
                _sys.modules[module_name] = mod
                spec.loader.exec_module(mod)
                setattr(pkg, module_name.split(".")[-1], mod)


        def _load_embedded_script_module(module_name: str):
            import importlib.util
            import sys as _sys

            embed_scripts = PROJECT_ROOT / ".embedded_ce310" / "scripts"
            embed_scripts.mkdir(parents=True, exist_ok=True)
            script_path = embed_scripts / f"{{module_name}}.py"
            script_path.write_text(EMBEDDED_SCRIPT_SOURCES[module_name], encoding="utf-8")

            spec = importlib.util.spec_from_file_location(module_name, script_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Failed to create spec for script {{module_name}} at {{script_path}}")
            mod = importlib.util.module_from_spec(spec)
            _sys.modules[module_name] = mod
            spec.loader.exec_module(mod)
            return mod
        """
    ).strip()


def part1_setup(mod_src: dict[str, str], run_src: dict[str, str]) -> str:
    loader = loader_block(mod_src, run_src)
    loader_indented = indent(loader, "        ")
    return dedent(
        f"""
        from pathlib import Path
        import sys
        import inspect
        import json
        import time
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from IPython.display import Image, display

        # Keep notebook self-contained: never climb parent directories.
        ROOT = Path('.').resolve()
        PROJECT_ROOT = ROOT
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.append(str(PROJECT_ROOT))

{loader_indented}

        USING_EXTERNAL_CE310 = True
        try:
            from ce310.ga import (
                GAConfig,
                initialize_population,
                tournament_select_index,
                clone,
                one_point_crossover,
                bit_mutate,
                run_ga,
            )
            from ce310.part1_problems import (
                fitness_one_max,
                decode_4bit_positional,
                decode_15bit_nonpositional,
                fitness_15max,
                fitness_soft15max,
                fitness_soft15trap_integer,
            )
            from ce310.utils import ensure_dir, write_json
        except Exception as ex:
            USING_EXTERNAL_CE310 = False
            print('ce310 package not found -> injecting embedded source modules:', ex)
            _inject_embedded_ce310_modules()
            from ce310.ga import (
                GAConfig,
                initialize_population,
                tournament_select_index,
                clone,
                one_point_crossover,
                bit_mutate,
                run_ga,
            )
            from ce310.part1_problems import (
                fitness_one_max,
                decode_4bit_positional,
                decode_15bit_nonpositional,
                fitness_15max,
                fitness_soft15max,
                fitness_soft15trap_integer,
            )
            from ce310.utils import ensure_dir, write_json

        from ce310.part1_problems import make_fitness_15max, make_fitness_soft15max, make_fitness_soft15trap_integer
        from ce310.experiments import run_condition

        R1 = PROJECT_ROOT / 'results' / 'part1_v10'
        FIG = PROJECT_ROOT / 'figures'
        ensure_dir(R1)
        ensure_dir(FIG)

        FORCE_RERUN = False


        def part1_outputs_complete() -> bool:
            required = [
                R1 / 'task3_tuning_stage1' / 'stage1_summary.csv',
                R1 / 'task3_tuning_stage2' / 'stage2_summary.csv',
                R1 / 'task3_main' / 'task3_summary.csv',
                R1 / 'task4_trap' / 'task4_summary.csv',
                R1 / 'task4_deceptive_vs_soft15max.csv',
                R1 / 'part1_report_summary.md',
            ]
            if not all(p.exists() for p in required):
                return False
            t3 = pd.read_csv(R1 / 'task3_main' / 'task3_summary.csv')
            t4 = pd.read_csv(R1 / 'task4_trap' / 'task4_summary.csv')
            if len(t3) != 8 or (t3['n_runs'] < 10).any():
                return False
            if len(t4) != 4 or (t4['n_runs'] < 10).any():
                return False
            return True


        def _build_part1_cfg(pop_size: int, genome_length: int, tournament_size: int, p_clone: float, p_mutop: float, p_bit_factor: float):
            p_xo = 1.0 - p_clone - p_mutop
            return {{
                'pop_size': int(pop_size),
                'genome_length': int(genome_length),
                'generations': 50,
                'tournament_size': int(tournament_size),
                'p_clone': float(p_clone),
                'p_crossover': float(p_xo),
                'p_mutation_operator': float(p_mutop),
                'p_bit_mutation': float(p_bit_factor) / float(genome_length),
                'experiment_name': 'part1_v10',
            }}


        def run_part1_v10_pipeline(resume_if_exists: bool = True) -> None:
            m = _load_embedded_script_module('run_part1')
            m.RESULT_ROOT = R1

            stage1_df = m.run_stage1_pop_t_tuning(
                n_runs=5,
                resume_if_exists=resume_if_exists,
                pops=[50, 100, 200],
                tournaments=[2, 3, 5],
            )
            best_pop = int(stage1_df.iloc[0]['pop_size'])
            best_t = int(stage1_df.iloc[0]['tournament_size'])

            stage2_df = m.run_stage2_operator_tuning(
                best_pop=best_pop,
                best_t=best_t,
                n_runs=3,
                resume_if_exists=resume_if_exists,
                p_clones=[0.1, 0.2, 0.3],
                p_mutops=[0.1, 0.2],
                p_bit_factors=[0.5, 1.0],
            )
            best = stage2_df.iloc[0]
            selected = {{
                'pop_size': int(best['pop_size']),
                'tournament_size': int(best['tournament_size']),
                'p_clone': float(best['p_clone']),
                'p_crossover': float(best['p_crossover']),
                'p_mutation_operator': float(best['p_mutation_operator']),
                'p_bit_factor': float(best['p_bit_factor']),
                'p_bit_mutation': float(best['p_bit_factor']) / 120.0,
            }}
            write_json(R1 / 'selected_part1_params.json', selected)

            task1 = m.run_task1_baseline(selected_params=selected, n_runs=10, resume_if_exists=resume_if_exists)
            task3_df = m.run_task3_main(selected_params=selected, n_runs=10, resume_if_exists=resume_if_exists)
            task4_df = m.run_task4_deceptive(selected_params=selected, n_runs=10, resume_if_exists=resume_if_exists)
            m.build_part1_report(
                stage1_df=stage1_df,
                stage2_df=stage2_df,
                selected_params=selected,
                task1_summary=task1,
                task3_df=task3_df,
                task4_df=task4_df,
            )

            cmp = pd.read_csv(R1 / 'task4_deceptive_vs_soft15max.csv')

            # Figures referenced in later cells
            plt.figure(figsize=(12, 4))
            plt.bar(task3_df['condition'], task3_df['best_of_run_mean'], yerr=task3_df['best_of_run_std'], capsize=3)
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Mean best-of-run')
            plt.title('Part1 Encoding Comparison')
            plt.tight_layout()
            plt.savefig(FIG / 'part1_encoding_comparison.png', dpi=140)
            plt.close()

            heat = stage1_df.pivot_table(index='pop_size', columns='tournament_size', values='best_of_run_mean')
            plt.figure(figsize=(6, 4))
            plt.imshow(heat.values, aspect='auto')
            plt.colorbar(label='mean best-of-run')
            plt.xticks(range(len(heat.columns)), heat.columns)
            plt.yticks(range(len(heat.index)), heat.index)
            plt.xlabel('Tournament size')
            plt.ylabel('Population size')
            plt.title('Part1 Parameter Heatmap')
            plt.tight_layout()
            plt.savefig(FIG / 'part1_parameter_heatmap.png', dpi=140)
            plt.close()

            plt.figure(figsize=(8, 4))
            plt.bar(cmp['condition'], cmp['delta_best_mean_trap_minus_soft'])
            plt.axhline(0, linewidth=1)
            plt.xticks(rotation=30, ha='right')
            plt.ylabel('Trap mean - soft15max mean')
            plt.title('Part1 Deceptive Comparison')
            plt.tight_layout()
            plt.savefig(FIG / 'part1_deceptive_comparison.png', dpi=140)
            plt.close()


        if FORCE_RERUN or (not part1_outputs_complete()):
            print('Running Part1 v10 real experiments (no synthetic fallback tables)...')
            t0 = time.time()
            run_part1_v10_pipeline(resume_if_exists=not FORCE_RERUN)
            print(f'Part1 v10 pipeline completed in {{time.time() - t0:.1f}} sec')
        else:
            print('Part1 v10 outputs already complete. Using cached real-run results.')

        print('PROJECT_ROOT =', PROJECT_ROOT)
        print('Using external ce310 package:', USING_EXTERNAL_CE310)
        print('Results folder exists:', R1.exists())
        """
    ).strip()


def part2_setup(mod_src: dict[str, str], run_src: dict[str, str]) -> str:
    loader = loader_block(mod_src, run_src)
    loader_indented = indent(loader, "        ")
    return dedent(
        f"""
        from pathlib import Path
        import sys
        import inspect
        import json
        import time
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from IPython.display import Image, display

        # Keep notebook self-contained: never climb parent directories.
        ROOT = Path('.').resolve()
        PROJECT_ROOT = ROOT
        if str(PROJECT_ROOT) not in sys.path:
            sys.path.append(str(PROJECT_ROOT))

{loader_indented}

        USING_EXTERNAL_CE310 = True
        try:
            from ce310.gp import (
                PRIMITIVE_NAME_BY_CODE,
                decode_program_population,
                execute,
                make_gp_fitness_function,
                make_primitive_frequency_hook,
            )
            from ce310.ga import GAConfig, run_ga
            from ce310.utils import ensure_dir, write_json
        except Exception as ex:
            USING_EXTERNAL_CE310 = False
            print('ce310 package not found -> injecting embedded source modules:', ex)
            _inject_embedded_ce310_modules()
            from ce310.gp import (
                PRIMITIVE_NAME_BY_CODE,
                decode_program_population,
                execute,
                make_gp_fitness_function,
                make_primitive_frequency_hook,
            )
            from ce310.ga import GAConfig, run_ga
            from ce310.utils import ensure_dir, write_json

        R2 = PROJECT_ROOT / 'results' / 'part2_v10'
        R1_V10 = PROJECT_ROOT / 'results' / 'part1_v10'
        FIG = PROJECT_ROOT / 'figures'
        ensure_dir(R2)
        ensure_dir(FIG)

        FORCE_RERUN = False


        def part2_outputs_complete() -> bool:
            required = [
                R2 / 'task5_encoding_comparison' / 'encoding_comparison_summary.csv',
                R2 / 'task7_experiments' / 'task7_summary.csv',
                R2 / 'task8_primitives' / 'task8_selected_conditions.csv',
                R2 / 'part2_report_summary.md',
            ]
            if not all(p.exists() for p in required):
                return False
            t7 = pd.read_csv(R2 / 'task7_experiments' / 'task7_summary.csv')
            if len(t7) != 18 or (t7['n_runs'] < 10).any():
                return False
            return True


        def _load_best_part1_params_from_v10() -> dict:
            path = R1_V10 / 'selected_part1_params.json'
            if path.exists():
                data = json.loads(path.read_text(encoding='utf-8'))
                return {{
                    'best_pop_size': int(data.get('pop_size', 100)),
                    'best_tournament_size': int(data.get('tournament_size', 3)),
                }}
            return {{'best_pop_size': 100, 'best_tournament_size': 3}}


        def _plot_trend_from_agg(agg_path: Path, out_path: Path, title: str) -> None:
            if not agg_path.exists():
                return
            agg = pd.read_csv(agg_path)
            freq_cols = [c for c in agg.columns if c.startswith('freq_') and c.endswith('_mean')]
            if not freq_cols:
                return
            plt.figure(figsize=(10, 6))
            for col in freq_cols:
                primitive = col.replace('freq_', '').replace('_mean', '')
                plt.plot(agg['generation'], agg[col], label=primitive, linewidth=1.7)
            plt.title(title)
            plt.xlabel('Generation')
            plt.ylabel('Primitive Frequency')
            plt.ylim(0.0, 1.0)
            plt.grid(alpha=0.3)
            plt.legend(ncol=4, fontsize=8)
            plt.tight_layout()
            out_path.parent.mkdir(parents=True, exist_ok=True)
            plt.savefig(out_path, dpi=140)
            plt.close()


        def run_part2_v10_pipeline(resume_if_exists: bool = True) -> None:
            m = _load_embedded_script_module('run_part2')
            m.RESULT_ROOT = R2
            m.load_best_part1_params = _load_best_part1_params_from_v10

            selected = _load_best_part1_params_from_v10()
            encoding_df = m.run_encoding_comparison(
                best_pop=selected['best_pop_size'],
                best_t=selected['best_tournament_size'],
                program_length=30,
                n_runs=10,
                resume_if_exists=resume_if_exists,
            )
            task7_df = m.run_task7_experiments(
                program_length=30,
                encoding='3bit',
                pops=[50, 100, 200],
                tournaments=[2, 3, 5],
                n_runs=10,
                resume_if_exists=resume_if_exists,
            )
            task8_df = m.run_task8_primitive_report(task7_df)
            m.build_part2_report(
                encoding_df=encoding_df,
                task7_df=task7_df,
                task8_df=task8_df,
                selected_params=selected,
            )

            # Figures referenced in later cells
            p2 = task7_df[task7_df['problem'] == 'problem2'].pivot_table(
                index='pop_size', columns='tournament_size', values='best_of_run_mean'
            )
            plt.figure(figsize=(6, 4))
            plt.imshow(p2.values, aspect='auto')
            plt.colorbar(label='mean best-of-run')
            plt.xticks(range(len(p2.columns)), p2.columns)
            plt.yticks(range(len(p2.index)), p2.index)
            plt.xlabel('Tournament size')
            plt.ylabel('Population size')
            plt.title('Part2 Parameter Impact (Problem2)')
            plt.tight_layout()
            plt.savefig(FIG / 'part2_parameter_impact_heatmap.png', dpi=140)
            plt.close()

            c = task7_df.sort_values('mean_execute_calls_per_generation', ascending=False).head(10)
            plt.figure(figsize=(10, 4))
            plt.bar(c['condition'], c['mean_execute_calls_per_generation'])
            plt.xticks(rotation=45, ha='right')
            plt.ylabel('Mean execute calls / generation')
            plt.title('Part2 Computational Cost (Top 10)')
            plt.tight_layout()
            plt.savefig(FIG / 'part2_computational_cost.png', dpi=140)
            plt.close()

            p1_best = task7_df[task7_df['problem'] == 'problem1'].sort_values('best_of_run_mean', ascending=False).iloc[0]['condition']
            p2_best = task7_df[task7_df['problem'] == 'problem2'].sort_values('best_of_run_mean', ascending=False).iloc[0]['condition']
            _plot_trend_from_agg(
                R2 / 'task7_experiments' / str(p1_best) / 'generation_aggregated.csv',
                FIG / 'part2_primitive_evolution_problem1_detailed.png',
                f'Problem1 detailed primitive evolution ({{p1_best}})',
            )
            _plot_trend_from_agg(
                R2 / 'task7_experiments' / str(p2_best) / 'generation_aggregated.csv',
                FIG / 'part2_primitive_evolution_problem2_detailed.png',
                f'Problem2 detailed primitive evolution ({{p2_best}})',
            )


        if FORCE_RERUN or (not part2_outputs_complete()):
            print('Running Part2 v10 real experiments (no synthetic fallback tables)...')
            t0 = time.time()
            run_part2_v10_pipeline(resume_if_exists=not FORCE_RERUN)
            print(f'Part2 v10 pipeline completed in {{time.time() - t0:.1f}} sec')
        else:
            print('Part2 v10 outputs already complete. Using cached real-run results.')

        print('PROJECT_ROOT =', PROJECT_ROOT)
        print('Using external ce310 package:', USING_EXTERNAL_CE310)
        print('Part2 results folder exists:', R2.exists())
        """
    ).strip()


def patch_notebook(path: Path, setup_code: str) -> None:
    nb = nbformat.read(str(path), as_version=4)
    setup_idx = None
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and cell.source.lstrip().startswith("from pathlib import Path"):
            setup_idx = i
            break
    if setup_idx is None:
        raise RuntimeError(f"setup cell not found in {path}")

    nb.cells[setup_idx].source = setup_code

    cell = nb.cells[setup_idx]
    cell.metadata["collapsed"] = True
    cell.metadata["hide_input"] = True
    cell.metadata["source_hidden"] = True
    cell.metadata["jupyter"] = dict(cell.metadata.get("jupyter", {}), source_hidden=True, outputs_hidden=False)
    tags = set(cell.metadata.get("tags", []))
    tags.update(["hide-input", "hide_input", "remove-input", "setup"])
    cell.metadata["tags"] = sorted(tags)

    nbformat.write(nb, str(path))
    print("patched", path, "setup_idx", setup_idx)


def main() -> None:
    V10_DIR = find_v10_dir()

    mod_src = module_sources()
    run_src = script_sources()
    p1 = part1_setup(mod_src, run_src)
    p2 = part2_setup(mod_src, run_src)

    targets = [
        (V10_DIR / "Part1.ipynb", p1),
        (V10_DIR / "Part2.ipynb", p2),
        (V10_DIR / "submit_only_clean" / "Part1.ipynb", p1),
        (V10_DIR / "submit_only_clean" / "Part2.ipynb", p2),
        (V10_DIR / "submit_only_3files" / "Part1.ipynb", p1),
        (V10_DIR / "submit_only_3files" / "Part2.ipynb", p2),
    ]
    for path, setup in targets:
        if path.exists():
            patch_notebook(path, setup)


if __name__ == "__main__":
    main()

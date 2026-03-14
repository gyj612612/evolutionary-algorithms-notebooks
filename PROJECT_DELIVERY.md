# CE310 Coursework Delivery (Auto-Generated Workflow)

## Key Deliverables

- `Part1.ipynb`: Incremental GA notebook for Tasks 1-4.
- `Part2.ipynb`: Incremental GP notebook for Tasks 5-8.
- `results/part1/`: Full run logs, per-generation stats, plots, summaries.
- `results/part2/`: Full run logs, per-generation stats, primitive-frequency trends, summaries.

## How to Reproduce

1. Validate all components:
   - `python scripts/validate_framework.py`
2. Run Part 1 experiments:
   - `python scripts/run_part1.py`
   - Fast iteration:
     - `python scripts/run_part1.py --quick`
   - Full recompute:
     - `python scripts/run_part1.py --no-resume`
3. Run Part 2 experiments:
   - `python scripts/run_part2.py`
   - Fast iteration:
     - `python scripts/run_part2.py --quick`
   - Full recompute:
     - `python scripts/run_part2.py --no-resume`
   - Custom experiment scale:
     - `python scripts/run_part2.py --runs-task7 10 --runs-encoding 5 --pops 50,100,200 --tournaments 2,3,5`
4. Generate notebooks:
   - `python scripts/build_notebooks.py`
5. Generate requirement coverage matrix:
   - `python scripts/generate_requirement_coverage.py`
6. Or run everything:
   - `python scripts/run_all.py`

## Runtime Notes

- Part 1 is relatively fast.
- Part 2 is heavier due repeated GP interpreter execution:
  - Task 7 uses 10 runs per condition and 50 generations.
  - Problem 2 evaluates 21 fitness cases per individual.
- `run_condition()` supports resume by reusing existing outputs, so interrupted runs continue without rerunning completed conditions.
- Resume safety: if requested run count differs from stored results, that condition is recomputed automatically.
- Part2 fitness evaluation is optimized with:
  - vectorized multi-case program execution (`execute_many`)
  - unique-program caching per generation
  - logging of nominal vs actual execute calls and reduction ratio

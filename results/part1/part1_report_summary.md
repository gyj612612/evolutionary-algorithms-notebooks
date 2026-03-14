# CE310 Part 1 Auto Summary

## Selected Parameters
- `pop_size=300`, `tournament_size=2`, `p_clone=0.100`, `p_xo=0.800`, `p_mutop=0.100`, `p_bit=0.01250`

## Task 1 (OneMax)
- Condition: `onemax_L100`
- Mean best-of-run: **99.900**
- Std best-of-run: **0.316**
- Ideal-found fraction: **0.900**

## Task 3 Tuning
- Stage1 best (`pop`, `T`): (300, 2) with mean best-of-run **26.600**
- Stage2 best operators: `p_clone=0.100`, `p_xo=0.800`, `p_mutop=0.100`, `p_bit_factor=1.500` with mean best-of-run **28.667**

## Task 3 Main Experiments
- File: `results/part1/task3_main/task3_summary.csv`
- `15bit_L10_15max`: mean best-of-run=0.300, std=0.483, ideal-found=0.000
- `15bit_L30_15max`: mean best-of-run=0.600, std=0.699, ideal-found=0.000
- `4bit_L10_15max`: mean best-of-run=10.000, std=0.000, ideal-found=1.000
- `4bit_L30_15max`: mean best-of-run=28.300, std=1.059, ideal-found=0.100
- `15bit_L10_soft15max`: mean best-of-run=14.490, std=0.129, ideal-found=0.000
- `15bit_L30_soft15max`: mean best-of-run=11.727, std=0.180, ideal-found=0.000
- `4bit_L10_soft15max`: mean best-of-run=15.000, std=0.000, ideal-found=1.000
- `4bit_L30_soft15max`: mean best-of-run=14.743, std=0.063, ideal-found=0.000

## Task 4 Deceptive Problem (Soft-15 Trap Integer)
- File: `results/part1/task4_trap/task4_summary.csv`
- Comparison file: `results/part1/task4_deceptive_vs_soft15max.csv`
- `15bit_L10_soft15trap_int`: trap mean=13.370, soft15max mean=14.490, delta=-1.120, trap ideal-found=0.000, soft ideal-found=0.000
- `15bit_L30_soft15trap_int`: trap mean=10.757, soft15max mean=11.727, delta=-0.970, trap ideal-found=0.000, soft ideal-found=0.000
- `4bit_L10_soft15trap_int`: trap mean=14.860, soft15max mean=15.000, delta=-0.140, trap ideal-found=0.100, soft ideal-found=1.000
- `4bit_L30_soft15trap_int`: trap mean=14.370, soft15max mean=14.743, delta=-0.373, trap ideal-found=0.000, soft ideal-found=0.000

## Reproducibility
- All run histories, configs, and aggregated stats are under `results/part1/`.
- Every condition stores per-generation best/mean/std plus run-level summaries.
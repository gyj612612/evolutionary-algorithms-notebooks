# CE310 Part 1 Auto Summary

## Selected Parameters
- `pop_size=200`, `tournament_size=2`, `p_clone=0.100`, `p_xo=0.800`, `p_mutop=0.100`, `p_bit=0.00417`

## Task 1 (OneMax)
- Condition: `onemax_L100`
- Mean best-of-run: **97.900**
- Std best-of-run: **1.370**
- Ideal-found fraction: **0.200**

## Task 3 Tuning
- Stage1 best (`pop`, `T`): (200, 2) with mean best-of-run **25.000**
- Stage2 best operators: `p_clone=0.100`, `p_xo=0.800`, `p_mutop=0.100`, `p_bit_factor=0.500` with mean best-of-run **26.333**

## Task 3 Main Experiments
- File: `results/part1/task3_main/task3_summary.csv`
- `15bit_L10_15max`: mean best-of-run=0.300, std=0.483, ideal-found=0.000
- `15bit_L30_15max`: mean best-of-run=0.400, std=0.699, ideal-found=0.000
- `4bit_L10_15max`: mean best-of-run=9.900, std=0.316, ideal-found=0.900
- `4bit_L30_15max`: mean best-of-run=24.800, std=2.300, ideal-found=0.000
- `15bit_L10_soft15max`: mean best-of-run=13.960, std=0.212, ideal-found=0.000
- `15bit_L30_soft15max`: mean best-of-run=11.457, std=0.130, ideal-found=0.000
- `4bit_L10_soft15max`: mean best-of-run=15.000, std=0.000, ideal-found=1.000
- `4bit_L30_soft15max`: mean best-of-run=14.483, std=0.164, ideal-found=0.000

## Task 4 Deceptive Problem (Soft-15 Trap Integer)
- File: `results/part1/task4_trap/task4_summary.csv`
- Comparison file: `results/part1/task4_deceptive_vs_soft15max.csv`
- `15bit_L10_soft15trap_int`: trap mean=12.960, soft15max mean=13.960, delta=-1.000, trap ideal-found=0.000, soft ideal-found=0.000
- `15bit_L30_soft15trap_int`: trap mean=10.433, soft15max mean=11.457, delta=-1.023, trap ideal-found=0.000, soft ideal-found=0.000
- `4bit_L10_soft15trap_int`: trap mean=14.760, soft15max mean=15.000, delta=-0.240, trap ideal-found=0.000, soft ideal-found=1.000
- `4bit_L30_soft15trap_int`: trap mean=14.180, soft15max mean=14.483, delta=-0.303, trap ideal-found=0.000, soft ideal-found=0.000

## Reproducibility
- All run histories, configs, and aggregated stats are under `results/part1/`.
- Every condition stores per-generation best/mean/std plus run-level summaries.
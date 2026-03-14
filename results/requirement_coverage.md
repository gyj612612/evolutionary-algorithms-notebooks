# CE310 Requirement Coverage Matrix

This file maps coursework marking requirements to concrete generated artifacts.

## Deliverables
- Part1 notebook present: **Yes**
- Part2 notebook present: **Yes**
- AI log template present: **Yes**

## Part 1
- Task1 one-max runs summary: `E:\CE310\results\part1\task1_onemax`
- Task3 tuning stage1 summary present: **Yes**
- Task3 tuning stage2 summary present: **Yes**
- Task3 main (10 runs/condition) summary present: **Yes**
- Task4 deceptive summary present: **Yes**
- Task4 deceptive vs baseline comparison present: **Yes**

## Part 2
- Task5 encoding comparison summary present: **Yes**
- Task7 summary present: **Yes**
- Task8 primitive trend summary present: **Yes**

## Part1 Key Metrics
- `15bit_L10_15max`: best_of_run_mean=0.300, ideal_found_fraction=0.000
- `15bit_L30_15max`: best_of_run_mean=0.600, ideal_found_fraction=0.000
- `4bit_L10_15max`: best_of_run_mean=10.000, ideal_found_fraction=1.000
- `4bit_L30_15max`: best_of_run_mean=28.300, ideal_found_fraction=0.100
- `15bit_L10_soft15max`: best_of_run_mean=14.490, ideal_found_fraction=0.000
- `15bit_L30_soft15max`: best_of_run_mean=11.727, ideal_found_fraction=0.000
- `4bit_L10_soft15max`: best_of_run_mean=15.000, ideal_found_fraction=1.000
- `4bit_L30_soft15max`: best_of_run_mean=14.743, ideal_found_fraction=0.000

## Task4 Deceptive Metrics
- `15bit_L10_soft15trap_int`: mean=13.370, ideal_found_fraction=0.000, local_optimum=14.0, global_optimum=15.0
- `15bit_L30_soft15trap_int`: mean=10.757, ideal_found_fraction=0.000, local_optimum=14.0, global_optimum=15.0
- `4bit_L10_soft15trap_int`: mean=14.860, ideal_found_fraction=0.100, local_optimum=14.0, global_optimum=15.0
- `4bit_L30_soft15trap_int`: mean=14.370, ideal_found_fraction=0.000, local_optimum=14.0, global_optimum=15.0

## Part2 Task7 Checks
- 10 runs per experiment satisfied: **True**
- Number of experiment conditions: **18**
- Mean execute-call reduction (caching): **48.2%**

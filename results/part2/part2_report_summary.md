# CE310 Part 2 Auto Summary

## Selected GA Baseline from Part 1
- pop_size=300
- tournament_size=2

## Task 5 Encoding Comparison
- `3bit_problem1`: mean best-of-run=32.000, std=11.576
- `7bit_problem1`: mean best-of-run=42.400, std=15.060
- `3bit_problem2`: mean best-of-run=-70.369, std=14.567
- `7bit_problem2`: mean best-of-run=-64.795, std=30.703

## Task 7 Experiments
- Summary file: `results/part2/task7_experiments/task7_summary.csv`
- `problem1_3bit_pop50_t2`: mean best-of-run=14.200, std=9.682, avg_execute_calls/gen=60.7, nominal_execute_calls/gen=100.0, call_reduction=39.3%
- `problem1_3bit_pop50_t3`: mean best-of-run=13.400, std=3.893, avg_execute_calls/gen=45.1, nominal_execute_calls/gen=100.0, call_reduction=54.9%
- `problem1_3bit_pop50_t5`: mean best-of-run=12.400, std=6.915, avg_execute_calls/gen=40.4, nominal_execute_calls/gen=100.0, call_reduction=59.6%
- `problem1_3bit_pop100_t2`: mean best-of-run=14.200, std=6.893, avg_execute_calls/gen=145.2, nominal_execute_calls/gen=200.0, call_reduction=27.4%
- `problem1_3bit_pop100_t3`: mean best-of-run=19.400, std=16.249, avg_execute_calls/gen=102.8, nominal_execute_calls/gen=200.0, call_reduction=48.6%
- `problem1_3bit_pop100_t5`: mean best-of-run=16.200, std=7.627, avg_execute_calls/gen=79.9, nominal_execute_calls/gen=200.0, call_reduction=60.0%
- `problem1_3bit_pop200_t2`: mean best-of-run=23.000, std=9.487, avg_execute_calls/gen=295.7, nominal_execute_calls/gen=400.0, call_reduction=26.1%
- `problem1_3bit_pop200_t3`: mean best-of-run=34.400, std=21.762, avg_execute_calls/gen=195.5, nominal_execute_calls/gen=400.0, call_reduction=51.1%
- `problem1_3bit_pop200_t5`: mean best-of-run=35.800, std=17.345, avg_execute_calls/gen=107.7, nominal_execute_calls/gen=400.0, call_reduction=73.1%
- `problem2_3bit_pop50_t2`: mean best-of-run=-122.934, std=19.534, ideal_found_fraction=0.000, avg_execute_calls/gen=819.5, nominal_execute_calls/gen=1050.0, call_reduction=21.9%
- `problem2_3bit_pop50_t3`: mean best-of-run=-114.382, std=28.448, ideal_found_fraction=0.000, avg_execute_calls/gen=583.0, nominal_execute_calls/gen=1050.0, call_reduction=44.5%
- `problem2_3bit_pop50_t5`: mean best-of-run=-106.925, std=18.754, ideal_found_fraction=0.000, avg_execute_calls/gen=440.7, nominal_execute_calls/gen=1050.0, call_reduction=58.0%
- `problem2_3bit_pop100_t2`: mean best-of-run=-82.560, std=28.652, ideal_found_fraction=0.000, avg_execute_calls/gen=1408.2, nominal_execute_calls/gen=2100.0, call_reduction=32.9%
- `problem2_3bit_pop100_t3`: mean best-of-run=-81.221, std=32.802, ideal_found_fraction=0.000, avg_execute_calls/gen=1018.3, nominal_execute_calls/gen=2100.0, call_reduction=51.5%
- `problem2_3bit_pop100_t5`: mean best-of-run=-84.664, std=11.824, ideal_found_fraction=0.000, avg_execute_calls/gen=768.0, nominal_execute_calls/gen=2100.0, call_reduction=63.4%
- `problem2_3bit_pop200_t2`: mean best-of-run=-72.034, std=20.269, ideal_found_fraction=0.000, avg_execute_calls/gen=3015.5, nominal_execute_calls/gen=4200.0, call_reduction=28.2%
- `problem2_3bit_pop200_t3`: mean best-of-run=-53.485, std=24.744, ideal_found_fraction=0.000, avg_execute_calls/gen=1578.1, nominal_execute_calls/gen=4200.0, call_reduction=62.4%
- `problem2_3bit_pop200_t5`: mean best-of-run=-67.281, std=26.959, ideal_found_fraction=0.000, avg_execute_calls/gen=1487.0, nominal_execute_calls/gen=4200.0, call_reduction=64.6%

## Task 8 Primitive Trends
- `problem1` best condition `problem1_3bit_pop200_t5` -> `results\part2\task8_primitives\problem1_primitive_trends.png`
- `problem2` best condition `problem2_3bit_pop200_t3` -> `results\part2\task8_primitives\problem2_primitive_trends.png`

## Reproducibility
- All run histories, configs, and aggregated stats are in `results/part2/`.
- Each condition records per-generation fitness stats and primitive frequencies.
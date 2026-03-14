from __future__ import annotations

import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ce310.ga import GAConfig, bit_mutate, one_point_crossover, run_ga, tournament_select_index
from ce310.gp import (
    decode_program_population,
    execute,
    execute_many,
    make_gp_fitness_function,
    polynomial_target,
    primitive_frequency_table,
)
from ce310.part1_problems import (
    decode_15bit_nonpositional,
    decode_4bit_positional,
    fitness_15max,
    fitness_15trap,
    fitness_soft15trap_integer,
    fitness_one_max,
    fitness_soft15max,
)


def test_part1_components() -> None:
    rng = np.random.default_rng(123)

    # OneMax
    pop = np.array([[1, 0, 1, 1], [0, 0, 0, 1]], dtype=np.int8)
    fit = fitness_one_max(pop)
    assert np.allclose(fit, np.array([3.0, 1.0]))

    # 4-bit decoding
    pop4 = np.array(
        [
            [1, 1, 1, 1, 0, 0, 0, 0],  # 15,0
            [1, 0, 0, 0, 1, 1, 0, 0],  # 1,3
        ],
        dtype=np.int8,
    )
    dec4 = decode_4bit_positional(pop4, length_l=2)
    assert dec4.tolist() == [[15, 0], [1, 3]]

    # 15-bit decoding
    pop15 = np.array([([1] * 15) + ([0] * 15)], dtype=np.int8)
    dec15 = decode_15bit_nonpositional(pop15, length_l=2)
    assert dec15.tolist() == [[15, 0]]

    # 15-max, soft-15-max and trap
    fit_15 = fitness_15max(pop4, length_l=2, encoding="4bit")
    fit_soft = fitness_soft15max(pop4, length_l=2, encoding="4bit")
    fit_trap = fitness_15trap(pop4, length_l=2, encoding="4bit")
    fit_soft_trap_int = fitness_soft15trap_integer(pop4, length_l=2, encoding="4bit")
    assert fit_15.tolist() == [1.0, 0.0]
    assert np.allclose(fit_soft, np.array([7.5, 2.0]))
    assert fit_trap.shape == (2,)
    assert fit_soft_trap_int.shape == (2,)

    # Tournament selection
    f = np.array([0.0, 1.0, 2.0, 3.0])
    idx = tournament_select_index(f, tournament_size=3, rng=rng, maximize=True)
    assert 0 <= idx < 4

    # Crossover and mutation
    p1 = np.array([1, 1, 1, 1], dtype=np.int8)
    p2 = np.array([0, 0, 0, 0], dtype=np.int8)
    child = one_point_crossover(p1, p2, rng)
    assert child.shape == p1.shape
    mut = bit_mutate(p1, p_bit=1.0, rng=rng)
    assert mut.tolist() == [0, 0, 0, 0]

    # Full GA run smoke test
    cfg = GAConfig(
        pop_size=20,
        genome_length=16,
        generations=5,
        tournament_size=3,
        p_clone=0.2,
        p_crossover=0.7,
        p_mutation_operator=0.1,
        p_bit_mutation=1 / 16,
        seed=7,
        maximize=True,
        experiment_name="smoke_part1",
    )
    result = run_ga(cfg, fitness_one_max)
    assert len(result.history) == 6
    assert "best_fitness" in result.history.columns


def test_part2_components() -> None:
    # Interpreter example from coursework: [5,1,2], x=3 -> 4
    assert execute(np.array([5, 1, 2], dtype=np.int16), 3.0) == 4.0
    many = execute_many(np.array([5, 1, 2], dtype=np.int16), np.array([3.0, 4.0]))
    assert many.tolist() == [4.0, 5.0]

    # Decode program
    pop = np.array([[1, 0, 1, 1, 1, 1]], dtype=np.int8)  # [5,7]
    prog = decode_program_population(pop, program_length=2, encoding="3bit")
    assert prog.tolist() == [[5, 7]]

    # Fitness functions
    f1 = make_gp_fitness_function(program_length=3, encoding="3bit", problem="problem1")
    fit1, meta1 = f1(np.array([[1, 5, 2, 1, 5, 2, 0, 0, 0]], dtype=np.int8))
    assert fit1.shape == (1,)
    assert meta1["fitness_cases"] == 2
    assert meta1["execute_calls"] <= meta1["execute_calls_nominal"]

    f2 = make_gp_fitness_function(program_length=3, encoding="3bit", problem="problem2")
    fit2, meta2 = f2(np.array([[1, 5, 2, 1, 5, 2, 0, 0, 0]], dtype=np.int8))
    assert fit2.shape == (1,)
    assert meta2["fitness_cases"] == 21
    assert meta2["execute_calls"] <= meta2["execute_calls_nominal"]

    # Primitive frequencies
    freq = primitive_frequency_table(np.array([[0, 1, 2, 3, 4, 5, 6, 7]], dtype=np.int16))
    assert np.isclose(sum(freq.values()), 1.0)

    # Target polynomial sanity
    y0 = polynomial_target(0.0)
    assert np.isclose(y0, 1.0)


if __name__ == "__main__":
    test_part1_components()
    test_part2_components()
    print("All validation tests passed.")

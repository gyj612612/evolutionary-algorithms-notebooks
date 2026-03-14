from __future__ import annotations

from typing import Dict, Literal, Tuple

import numpy as np


GPEncoding = Literal["3bit", "7bit"]
GPProblem = Literal["problem1", "problem2"]

PRIMITIVE_NAME_BY_CODE = {
    0: "NOP",
    1: "X",
    2: "+",
    3: "-",
    4: "*",
    5: "1",
    6: "-1",
    7: "0",
}


def execute(program: np.ndarray, x: float) -> float:
    stack = []

    def pop() -> float:
        if not stack:
            return 0.0
        return float(stack.pop())

    for instr in program:
        if instr == 0:  # NOP
            pass
        elif instr == 1:  # X
            stack.append(float(x))
        elif instr == 2:  # +
            stack.append(pop() + pop())
        elif instr == 3:  # -
            stack.append(pop() - pop())
        elif instr == 4:  # *
            stack.append(pop() * pop())
        elif instr == 5:  # 1
            stack.append(1.0)
        elif instr == 6:  # -1
            stack.append(-1.0)
        else:  # 0
            stack.append(0.0)

    return pop()


def execute_many(program: np.ndarray, x_values: np.ndarray) -> np.ndarray:
    x_values = np.asarray(x_values, dtype=float)
    stack = []

    def pop() -> np.ndarray:
        if not stack:
            return np.zeros_like(x_values, dtype=float)
        return stack.pop()

    for instr in program:
        if instr == 0:  # NOP
            pass
        elif instr == 1:  # X
            stack.append(x_values.copy())
        elif instr == 2:  # +
            stack.append(pop() + pop())
        elif instr == 3:  # -
            stack.append(pop() - pop())
        elif instr == 4:  # *
            stack.append(pop() * pop())
        elif instr == 5:  # 1
            stack.append(np.ones_like(x_values, dtype=float))
        elif instr == 6:  # -1
            stack.append(-np.ones_like(x_values, dtype=float))
        else:  # 0
            stack.append(np.zeros_like(x_values, dtype=float))

    return pop()


def decode_3bit_positional(population: np.ndarray, program_length: int) -> np.ndarray:
    expected_bits = 3 * program_length
    if population.shape[1] != expected_bits:
        raise ValueError(f"Expected chromosome length {expected_bits}, got {population.shape[1]}")
    blocks = population.reshape(population.shape[0], program_length, 3)
    weights = np.array([1, 2, 4], dtype=np.int16)
    return (blocks * weights).sum(axis=2).astype(np.int16)


def decode_7bit_nonpositional(population: np.ndarray, program_length: int) -> np.ndarray:
    expected_bits = 7 * program_length
    if population.shape[1] != expected_bits:
        raise ValueError(f"Expected chromosome length {expected_bits}, got {population.shape[1]}")
    blocks = population.reshape(population.shape[0], program_length, 7)
    return blocks.sum(axis=2).astype(np.int16)


def decode_program_population(
    population: np.ndarray, program_length: int, encoding: GPEncoding
) -> np.ndarray:
    if encoding == "3bit":
        return decode_3bit_positional(population, program_length)
    if encoding == "7bit":
        return decode_7bit_nonpositional(population, program_length)
    raise ValueError(f"Unknown encoding: {encoding}")


def polynomial_target(x: float) -> float:
    return 2 * (x**5) + 4 * (x**4) + 6 * (x**3) + 8 * (x**2) + 10 * x + 1


def fitness_problem1_single(program: np.ndarray) -> float:
    out = execute_many(program, np.array([-1.0, 1.0]))
    return float(out[1] - out[0])


def fitness_problem2_single(
    program: np.ndarray, x_values: np.ndarray, target_values: np.ndarray | None = None
) -> float:
    if target_values is None:
        target_values = np.array([polynomial_target(float(x)) for x in x_values], dtype=float)
    y_hat = execute_many(program, x_values)
    err = np.abs(y_hat - target_values).sum()
    return float(-err)


def _evaluate_unique_programs(
    programs: np.ndarray,
    problem: GPProblem,
    x_values_problem2: np.ndarray,
    target_values_problem2: np.ndarray,
) -> Tuple[np.ndarray, int]:
    unique_programs, inverse = np.unique(programs, axis=0, return_inverse=True)
    unique_fit = np.empty(unique_programs.shape[0], dtype=float)

    if problem == "problem1":
        x_small = np.array([-1.0, 1.0], dtype=float)
        for i in range(unique_programs.shape[0]):
            y = execute_many(unique_programs[i], x_small)
            unique_fit[i] = float(y[1] - y[0])
    elif problem == "problem2":
        for i in range(unique_programs.shape[0]):
            y_hat = execute_many(unique_programs[i], x_values_problem2)
            unique_fit[i] = float(-np.abs(y_hat - target_values_problem2).sum())
    else:
        raise ValueError(f"Unknown GP problem: {problem}")

    return unique_fit[inverse], int(unique_programs.shape[0])


def make_gp_fitness_function(
    program_length: int, encoding: GPEncoding, problem: GPProblem
):
    x_values = np.linspace(-1.0, 1.0, 21)
    y_targets = np.array([polynomial_target(float(x)) for x in x_values], dtype=float)
    n_cases = 2 if problem == "problem1" else len(x_values)

    def fitness(population: np.ndarray) -> Tuple[np.ndarray, Dict[str, float]]:
        programs = decode_program_population(population, program_length, encoding)
        fit, unique_count = _evaluate_unique_programs(
            programs=programs,
            problem=problem,
            x_values_problem2=x_values,
            target_values_problem2=y_targets,
        )
        nominal_calls = float(population.shape[0] * n_cases)
        actual_calls = float(unique_count * n_cases)
        return fit, {
            "execute_calls": actual_calls,
            "execute_calls_nominal": nominal_calls,
            "fitness_cases": float(n_cases),
            "unique_programs": float(unique_count),
            "duplicate_ratio": float(1.0 - (unique_count / population.shape[0])),
        }

    return fitness


def primitive_frequency_table(programs: np.ndarray) -> Dict[str, float]:
    counts = np.bincount(programs.ravel(), minlength=8).astype(float)
    total = counts.sum()
    if total <= 0:
        total = 1.0
    return {
        f"freq_{PRIMITIVE_NAME_BY_CODE[i]}": float(counts[i] / total)
        for i in range(8)
    }


def make_primitive_frequency_hook(program_length: int, encoding: GPEncoding):
    def hook(_generation: int, population: np.ndarray, _fitness: np.ndarray):
        programs = decode_program_population(population, program_length, encoding)
        return primitive_frequency_table(programs)

    return hook


def best_program_from_population(
    population: np.ndarray,
    fitness: np.ndarray,
    program_length: int,
    encoding: GPEncoding,
    maximize: bool = True,
) -> np.ndarray:
    if maximize:
        idx = int(np.argmax(fitness))
    else:
        idx = int(np.argmin(fitness))
    programs = decode_program_population(population, program_length, encoding)
    return programs[idx].copy()

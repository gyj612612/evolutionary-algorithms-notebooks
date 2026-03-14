from __future__ import annotations

from typing import Literal

import numpy as np


Encoding = Literal["4bit", "15bit"]


def fitness_one_max(population: np.ndarray) -> np.ndarray:
    return population.sum(axis=1).astype(float)


def decode_4bit_positional(population: np.ndarray, length_l: int) -> np.ndarray:
    expected_bits = 4 * length_l
    if population.shape[1] != expected_bits:
        raise ValueError(f"Expected chromosome length {expected_bits}, got {population.shape[1]}")
    blocks = population.reshape(population.shape[0], length_l, 4)
    weights = np.array([1, 2, 4, 8], dtype=np.int16)
    return (blocks * weights).sum(axis=2).astype(np.int16)


def decode_15bit_nonpositional(population: np.ndarray, length_l: int) -> np.ndarray:
    expected_bits = 15 * length_l
    if population.shape[1] != expected_bits:
        raise ValueError(f"Expected chromosome length {expected_bits}, got {population.shape[1]}")
    blocks = population.reshape(population.shape[0], length_l, 15)
    return blocks.sum(axis=2).astype(np.int16)


def decode_population(population: np.ndarray, length_l: int, encoding: Encoding) -> np.ndarray:
    if encoding == "4bit":
        return decode_4bit_positional(population, length_l)
    if encoding == "15bit":
        return decode_15bit_nonpositional(population, length_l)
    raise ValueError(f"Unknown encoding: {encoding}")


def fitness_15max(population: np.ndarray, length_l: int, encoding: Encoding) -> np.ndarray:
    phenotype = decode_population(population, length_l, encoding)
    return (phenotype == 15).sum(axis=1).astype(float)


def fitness_soft15max(population: np.ndarray, length_l: int, encoding: Encoding) -> np.ndarray:
    phenotype = decode_population(population, length_l, encoding)
    return phenotype.mean(axis=1).astype(float)


def fitness_15trap(population: np.ndarray, length_l: int, encoding: Encoding) -> np.ndarray:
    block_size = 4 if encoding == "4bit" else 15
    expected_bits = length_l * block_size
    if population.shape[1] != expected_bits:
        raise ValueError(f"Expected chromosome length {expected_bits}, got {population.shape[1]}")

    blocks = population.reshape(population.shape[0], length_l, block_size)
    unitation = blocks.sum(axis=2).astype(float)
    trap_values = np.where(unitation == block_size, block_size, (block_size - 1) - unitation)
    # Normalize each block to keep range comparable with 15-max: [0, L]
    normalized = trap_values / block_size
    return normalized.sum(axis=1).astype(float)


def fitness_soft15trap_integer(population: np.ndarray, length_l: int, encoding: Encoding) -> np.ndarray:
    """
    Deceptive trap in integer space (corresponding to soft-15-max style scale).
    Per decoded integer I in [0,15]:
      - global optimum at I=15 -> score 15
      - deceptive local optimum at I=0 -> score 14
      - misleading slope away from the global optimum for I<15 via score 14-I
    Returns the mean block score in [0, 15].
    """
    phenotype = decode_population(population, length_l, encoding)
    block_scores = np.where(phenotype == 15, 15, 14 - phenotype)
    return block_scores.mean(axis=1).astype(float)


def make_fitness_15max(length_l: int, encoding: Encoding):
    return lambda population: fitness_15max(population, length_l, encoding)


def make_fitness_soft15max(length_l: int, encoding: Encoding):
    return lambda population: fitness_soft15max(population, length_l, encoding)


def make_fitness_15trap(length_l: int, encoding: Encoding):
    return lambda population: fitness_15trap(population, length_l, encoding)


def make_fitness_soft15trap_integer(length_l: int, encoding: Encoding):
    return lambda population: fitness_soft15trap_integer(population, length_l, encoding)

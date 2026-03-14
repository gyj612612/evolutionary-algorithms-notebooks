from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, Optional, Tuple

import numpy as np
import pandas as pd


FitnessFn = Callable[[np.ndarray], Any]
GenerationHook = Callable[[int, np.ndarray, np.ndarray], Dict[str, float]]


@dataclass
class GAConfig:
    pop_size: int
    genome_length: int
    generations: int = 50
    tournament_size: int = 3
    p_clone: float = 0.2
    p_crossover: float = 0.7
    p_mutation_operator: float = 0.1
    p_bit_mutation: float = 0.01
    seed: Optional[int] = None
    maximize: bool = True
    experiment_name: str = "ga_experiment"

    def validate(self) -> None:
        if self.pop_size <= 1:
            raise ValueError("pop_size must be > 1")
        if self.genome_length <= 1:
            raise ValueError("genome_length must be > 1")
        if self.generations < 1:
            raise ValueError("generations must be >= 1")
        if self.tournament_size < 2:
            raise ValueError("tournament_size must be >= 2")
        if self.tournament_size > self.pop_size:
            raise ValueError("tournament_size cannot exceed pop_size")
        probs = [self.p_clone, self.p_crossover, self.p_mutation_operator]
        if any(p < 0 for p in probs):
            raise ValueError("operator probabilities must be >= 0")
        if not np.isclose(sum(probs), 1.0):
            raise ValueError("p_clone + p_crossover + p_mutation_operator must sum to 1")
        if not (0.0 <= self.p_bit_mutation <= 1.0):
            raise ValueError("p_bit_mutation must be in [0, 1]")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GARunResult:
    config: Dict[str, Any]
    history: pd.DataFrame
    best_genome: np.ndarray
    best_fitness: float
    final_population: np.ndarray
    metadata: Dict[str, Any]


def initialize_population(cfg: GAConfig, rng: np.random.Generator) -> np.ndarray:
    return rng.integers(0, 2, size=(cfg.pop_size, cfg.genome_length), dtype=np.int8)


def tournament_select_index(
    fitness: np.ndarray,
    tournament_size: int,
    rng: np.random.Generator,
    maximize: bool = True,
) -> int:
    contenders = rng.integers(0, fitness.shape[0], size=tournament_size)
    contender_fitness = fitness[contenders]
    if maximize:
        return int(contenders[np.argmax(contender_fitness)])
    return int(contenders[np.argmin(contender_fitness)])


def clone(parent: np.ndarray) -> np.ndarray:
    return parent.copy()


def one_point_crossover(
    parent_a: np.ndarray, parent_b: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    if parent_a.shape != parent_b.shape:
        raise ValueError("parent shapes must match")
    cut = int(rng.integers(1, parent_a.shape[0]))
    child = np.empty_like(parent_a)
    child[:cut] = parent_a[:cut]
    child[cut:] = parent_b[cut:]
    return child


def bit_mutate(individual: np.ndarray, p_bit: float, rng: np.random.Generator) -> np.ndarray:
    mask = rng.random(individual.shape[0]) < p_bit
    mutated = individual.copy()
    mutated[mask] = 1 - mutated[mask]
    return mutated


def _call_fitness(fitness_fn: FitnessFn, population: np.ndarray) -> Tuple[np.ndarray, Dict[str, Any]]:
    out = fitness_fn(population)
    if isinstance(out, tuple) and len(out) == 2:
        fitness, meta = out
    else:
        fitness, meta = out, {}
    fitness = np.asarray(fitness, dtype=float)
    if fitness.shape != (population.shape[0],):
        raise ValueError("fitness function must return one scalar per individual")
    return fitness, dict(meta)


def _build_generation_row(
    generation: int,
    fitness: np.ndarray,
    maximize: bool,
    extra: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if maximize:
        best_idx = int(np.argmax(fitness))
    else:
        best_idx = int(np.argmin(fitness))
    row: Dict[str, Any] = {
        "generation": generation,
        "best_fitness": float(fitness[best_idx]),
        "mean_fitness": float(np.mean(fitness)),
        "std_fitness": float(np.std(fitness)),
        "best_index": best_idx,
    }
    if extra:
        row.update(extra)
    return row


def run_ga(
    cfg: GAConfig,
    fitness_fn: FitnessFn,
    generation_hook: Optional[GenerationHook] = None,
) -> GARunResult:
    cfg.validate()
    rng = np.random.default_rng(cfg.seed)
    population = initialize_population(cfg, rng)

    history_rows = []
    metadata: Dict[str, Any] = {"fitness_meta_per_generation": []}

    fitness, fitness_meta = _call_fitness(fitness_fn, population)
    hook_meta = generation_hook(0, population, fitness) if generation_hook else {}
    history_rows.append(_build_generation_row(0, fitness, cfg.maximize, {**fitness_meta, **hook_meta}))
    metadata["fitness_meta_per_generation"].append(fitness_meta)

    for gen in range(1, cfg.generations + 1):
        next_population = np.empty_like(population)
        for i in range(cfg.pop_size):
            r = rng.random()
            if r < cfg.p_clone:
                p = tournament_select_index(fitness, cfg.tournament_size, rng, cfg.maximize)
                child = clone(population[p])
            elif r < cfg.p_clone + cfg.p_crossover:
                p1 = tournament_select_index(fitness, cfg.tournament_size, rng, cfg.maximize)
                p2 = tournament_select_index(fitness, cfg.tournament_size, rng, cfg.maximize)
                child = one_point_crossover(population[p1], population[p2], rng)
            else:
                p = tournament_select_index(fitness, cfg.tournament_size, rng, cfg.maximize)
                child = bit_mutate(population[p], cfg.p_bit_mutation, rng)
            next_population[i] = child

        population = next_population
        fitness, fitness_meta = _call_fitness(fitness_fn, population)
        hook_meta = generation_hook(gen, population, fitness) if generation_hook else {}
        history_rows.append(_build_generation_row(gen, fitness, cfg.maximize, {**fitness_meta, **hook_meta}))
        metadata["fitness_meta_per_generation"].append(fitness_meta)

    history = pd.DataFrame(history_rows)
    if cfg.maximize:
        best_idx = int(np.argmax(fitness))
    else:
        best_idx = int(np.argmin(fitness))

    result = GARunResult(
        config=cfg.to_dict(),
        history=history,
        best_genome=population[best_idx].copy(),
        best_fitness=float(fitness[best_idx]),
        final_population=population.copy(),
        metadata=metadata,
    )
    return result


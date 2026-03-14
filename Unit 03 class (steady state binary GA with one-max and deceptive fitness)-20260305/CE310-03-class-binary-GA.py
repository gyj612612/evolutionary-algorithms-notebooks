from random import randint
from random import sample
from random import random

# Initialize Global Parameters
iterations = 500
N = 20          # Genome length
M = 50          # Population size
crossover_prob = 0.5
mutation_rate = 1 / N

def fitness_function(genome):
    return sum(genome) # Fitness is simply the count of 1s.
    
def random_individual(N):
    return [randint(0, 1) for _ in range(N)]

def random_population(M, N):
    return [random_individual(N) for _ in range(M)]

def eval_fitness(population, fitness_func):
    return [fitness_func(ind) for ind in population]

def tournament():
    i, j = sample(range(M), 2)
    return i if fitnesses[i] >= fitnesses[j] else j

def negative_tournament():
    i, j = sample(range(M), 2)
    # Returns the index of the weaker individual to be replaced
    return i if fitnesses[i] <= fitnesses[j] else j

def mutate():
    idx = tournament()
    parent = population[idx]
    # Create offspring by flipping bits
    offspring = [(1 - bit) if random() < mutation_rate else bit for bit in parent]
    return offspring

def crossover():
    idx1 = tournament()
    idx2 = tournament()
    parent1, parent2 = population[idx1], population[idx2]
    
    # One-point crossover
    point = randint(1, N - 1)
    offspring = parent1[:point] + parent2[point:]
    return offspring
    
population = random_population(M, N)
fitnesses = eval_fitness(population, fitness_function)

# Track the best individual
best_idx = fitnesses.index(max(fitnesses))
best_genome = population[best_idx][:]
best_fit = fitnesses[best_idx]

for i in range(iterations):
    if random() < crossover_prob:
        offspring = crossover()
    else:
        offspring = mutate()
        
    f = fitness_function(offspring)
    
    k = negative_tournament()
    population[k] = offspring
    fitnesses[k] = f
    
    if f > best_fit:
        best_fit = f
        best_genome = offspring[:]
        print(best_fit, best_genome)

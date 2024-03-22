from itertools import compress
import random
import time
import matplotlib.pyplot as plt
import numpy as np
from data import *


def initial_population(individual_size, population_size):
    return [[random.choice([True, False]) for _ in range(individual_size)] for _ in range(population_size)]


def fitness(items, knapsack_max_capacity, individual):
    total_weight = sum(compress(items['Weight'], individual))
    if total_weight > knapsack_max_capacity:
        return 0
    return sum(compress(items['Value'], individual))


def population_best(items, knapsack_max_capacity, population):
    best_individual = None
    best_individual_fitness = -1
    for individual in population:
        individual_fitness = fitness(items, knapsack_max_capacity, individual)
        if individual_fitness > best_individual_fitness:
            best_individual = individual
            best_individual_fitness = individual_fitness
    return best_individual, best_individual_fitness


# selekcja
def get_parents():
    parents = []
    sum_fitness = sum([fitness(items, knapsack_max_capacity, c) for c in population])
    for i in range(n_selection):
        possibilities = [fitness(items, knapsack_max_capacity, value)/sum_fitness for value in population]
        random_num = random.random()
        temp = 0
        for value in possibilities:
            temp += value
            if (temp >= random_num):
                parents.append(population[possibilities.index(value)])
                break

    return parents


# crossover
def create_children(parents):
    split_parents = np.array_split(parents, 2)
    first_part = split_parents[0]
    second_part = split_parents[1]
    children = []
    for i in range(len(first_part)):
        first_parent = np.array_split(first_part[i], 2)
        second_parent = np.array_split(second_part[i], 2)
        child_A = np.concatenate((first_parent[0], second_parent[1])).tolist()
        child_B = np.concatenate((first_parent[1], second_parent[0])).tolist()
        children.append(child_A)
        children.append(child_B)
    return children


# mutacja
def mutation(children):
    for idx, child in enumerate(children):
        mutate_index = random.randint(0, len(child) - 1)
        new_val = not child[mutate_index]
        child[mutate_index] = new_val
        children[idx] = child


def find_best():
    better_array = np.array([fitness(items, knapsack_max_capacity, specimen) for specimen in population])
    res = []
    for _ in range(n_elite):
        best_index = better_array.argmax()
        res.append(population[best_index])
        better_array = better_array.tolist()
        better_array.remove(better_array[best_index])
        better_array = np.array(better_array)

    return res


items, knapsack_max_capacity = get_big()
print(items)

population_size = 100
generations = 200
n_selection = 50
n_elite = 1

start_time = time.time()
best_solution = None
best_fitness = 0
population_history = []
best_history = []
population = initial_population(len(items), population_size)


for _ in range(generations):
    population_history.append(population)
    # TODO: implement genetic algorithm
    best = find_best()
    parents = get_parents()
    children = create_children(parents)
    mutation(children)
    population = children

    for elite in best:
        population.append(elite)



    best_individual, best_individual_fitness = population_best(items, knapsack_max_capacity, population)
    if best_individual_fitness > best_fitness:
        best_solution = best_individual
        best_fitness = best_individual_fitness
    best_history.append(best_fitness)

end_time = time.time()
total_time = end_time - start_time
print('Best solution:', list(compress(items['Name'], best_solution)))
print('Best solution value:', best_fitness)
print('Time: ', total_time)

# plot generations
x = []
y = []
top_best = 5
for i, population in enumerate(population_history):
    plotted_individuals = min(len(population), top_best)
    x.extend([i] * plotted_individuals)
    population_fitnesses = [fitness(items, knapsack_max_capacity, individual) for individual in population]
    population_fitnesses.sort(reverse=True)
    y.extend(population_fitnesses[:plotted_individuals])
plt.scatter(x, y, marker='.')
plt.plot(best_history, 'r')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()

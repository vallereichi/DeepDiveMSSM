import numpy as np
import random
import time
from collections.abc import Callable
from typing import Union, Optional
import objective_functions as objective_functions
from objective_functions import evaluate_objective_function

# define parameters
NP = 10                # population size
F = 0.8                 # Mutation scaling factor
Cr = 0.8                # Crossover rate

# convergence restrictions
conv_threshold = 1e-3
MAX_ITER = 10000

# defining the parameter space
ranges = [[-100, 100], [-100,100]]
objective_function:Callable[[np.array], float] = objective_functions.gaussian



"""
function declarations
"""
def initialize_population(NP:int, ranges:list) -> list[np.array]:
    """
    creating the initial population by randomly selecting the chosen number of points from the given parameter space

    parameters: 
        NP:     population size
        ranges: list of ranges for every dimension of the parameter space

    returns:    
        list of points in the parameter space composing the first generation
    """
    population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]   
    while len(np.unique(population, axis=0)) != len(population):          
        population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]  

    #print(f"Population initialized with {len(population)} points in the {len(ranges)}-dimensional space.") 
    return population


def update(population:list[np.array], mutation:Callable[[list[np.array], np.array, float], np.array], crossover:Callable[[np.array, np.array, float], np.array]):
    """
    perform one iteration of the selected differential evolution

    parameters:
        population: list of the current generation of points in the parameter space
        mutation:   the mutation scheme function (e.g. "1")
        crossover:  the crossover function (e.g. binary)

    returns:
        population: list of the next generation of points in the parameter space
        improvement: over the last generation. Needed for determining convergance
    """
    target = random.choice(population)
    target_id = np.where([np.array_equal(target, indiv) for indiv in population])[0][0]                                        # TODO add more target options

    donor = mutation(population, target, F)
    trial = crossover(target, donor, Cr)
    improvement = selection(population, target,target_id, trial)


    #print("Improvement:", improvement)
    return population, improvement

# Mutation
def mutate_rand_one(population:list[np.array], target:np.array, F:float) -> np.array:
        """
        perform the mutation step according to the "rand/one" scheme

        parameters:
            population: list of the current generation of points in the parameter space
            target:     target_vector from the current generation
            F:          Mutation scale factor

        returns:
            donor_vector 
        """
        a, b, c = np.array(random.sample(population, 3))
        while any(np.array_equal(x, target) for x in [a, b, c]):
            a, b, c = np.array(random.sample(population, 3))

        donor = a + F * (b - c)
        return donor


# Crossover
def crossover_bin(target:np.array, donor:np.array, Cr:float) -> np.array:
        """
        performing the binary crossover

        parameters:
            target: target_vector
            donor:  donor_vector
            Cr:     Crossover rate

        returns:
            trial_vector
        """
       
        trial = np.zeros_like(target)
        for k in range(len(target)):
            if random.random() <= Cr:
                trial[k] = donor[k]
            else:
                trial[k] = target[k]

        rand_dim = random.randint(0, len(target) - 1)
        trial[rand_dim] = donor[rand_dim]

        return trial


# Selection
def selection(population:list[np.array], target:np.array, target_id:int, trial:np.array) -> float:
        """
        Final selection for the next generation. Choosing the vector with the best likelihood in a greedy fashion from the target_vector and the trial_vector

        parameters:
            population: list of the current generation of points in the parameter space
            target:     target_vector
            target_id:  index of the target_vector in the current population
            trial:      trial_vector

        returns:
            improvement over the last generation. Needed for determining convergance
        """
        
        target_lh = evaluate_objective_function(objective_function, target)
        trial_lh = evaluate_objective_function(objective_function, trial)

        if trial_lh > target_lh:
            if not any(np.array_equal(trial, indiv) for indiv in population):
                population[target_id] = trial
    
        improvement = max(trial_lh-target_lh, 0)
        
        #print("\nTarget likelihood:", target_lh)
        #print("Trial likelihood:", trial_lh)
        
        return improvement






"""
main entry point
"""
def main():

    start = time.time()
    population = initialize_population(NP, ranges)
    population_list = [population]
    improvement = 0

    print("\n ------------------- \nstart differential evolution:")
    while len(population_list) < MAX_ITER:
        population, improvement = update(population, mutate_rand_one, crossover_bin)
        population_list.append(population)
        print("population: ", len(population_list))

        if 0 < improvement < conv_threshold:
            break

    end = time.time()       
    print("total time: ", end-start)
    # print("\nFinal population:")
    # for point in population:
    #    print(point)




if __name__ == "__main__":
    main()
import numpy as np
import random
import time
import likelihoods
from likelihoods import comb_likelihood, eval_likelihood

# define parameters
NP = 10000
F = 0.8
Cr = 0.8

conv_threshold = 1e-3
MAX_ITER = 10000

ranges = [[20, 60], [30, 90]]
likelihood_list = [(likelihoods.gaussian, [50, 20]), (likelihoods.gaussian, [70, 10])]


"""
function declarations
"""
def initialize_population(NP:int, ranges:list) -> list[np.array]:
    population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]   
    while len(np.unique(population, axis=0)) != len(population):          
        population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]  

    #print(f"Population initialized with {len(population)} points in the {len(ranges)}-dimensional space.") 
    return population


def update(population:list[np.array], mutation, crossover):
    target = random.choice(population)
    target_id = np.where([np.array_equal(target, indiv) for indiv in population])[0][0]                                        # TODO add more target options

    donor = mutation(population, target, F)
    trial = crossover(target, donor, Cr)
    improvement = selection(population, target,target_id, trial)


    #print("Improvement:", improvement)
    return population, improvement

# Mutation
def mutate_rand_one(population:list[np.array], target:np.array, F:float) -> np.array:
        a, b, c = np.array(random.sample(population, 3))
        while any(np.array_equal(x, target) for x in [a, b, c]):
            a, b, c = np.array(random.sample(population, 3))

        donor = a + F * (b - c)
        return donor


# Crossover
def crossover_bin(target:np.array, donor:np.array, Cr:float) -> np.array:
       
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
        
        target_lh = comb_likelihood([eval_likelihood(lh[0], lh[1], target[i]) for i, lh in enumerate(likelihood_list)])
        trial_lh = comb_likelihood([eval_likelihood(lh[0], lh[1], trial[i]) for i, lh in enumerate(likelihood_list)])

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
    # print("\nFinal population:")
    # for point in population:
    #    print(point)
    print("total time: ", end-start)




if __name__ == "__main__":
    main()
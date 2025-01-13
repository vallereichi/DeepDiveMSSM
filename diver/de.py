import numpy as np
import random
import likelihoods
from likelihoods import comb_likelihood, eval_likelihood

# define parameters
NP = 100
F = 0.8
Cr = 0.8

conv_threshold = 1e-3
MAX_ITER = 10000

ranges = [[20, 60], [30, 90]]
likelihood_list = [(likelihoods.gaussian, [50, 20]), (likelihoods.gaussian, [70, 10])]

# initialize population
population_list = []
population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]   
while len(np.unique(population, axis=0)) != len(population):          
    population = [[random.uniform(ranges[i][0], ranges[i][1]) for i in range(len(ranges))] for _ in range(NP)]   
population_list.append(population)



print("\nInitial population:")
print(np.unique(population, axis=0))


print("\n ------------------- \nstart differential evolution:")

while len(population_list) < MAX_ITER:

    # perform mutation in the rand/1 scheme
    target = random.choice(population)
    target_id = np.where([np.array_equal(target, indiv) for indiv in population])[0][0]

    a, b, c = np.array(random.sample(population, 3))
    while any(np.array_equal(x, target) for x in [a, b, c]):
        a, b, c = np.array(random.sample(population, 3))

    donor = a + F * (b - c)

    print("\nTarget:", target)
    print("Donor:", donor)


    # perform binary crossover
    trial = np.zeros_like(target)
    for k in range(len(target)):
        if random.random() <= Cr:
            trial[k] = donor[k]
        else:
            trial[k] = target[k]

    rand_dim = random.randint(0, len(target) - 1)
    trial[rand_dim] = donor[rand_dim]

    print("Trial:", trial)



    # selection
    target_lh = comb_likelihood([eval_likelihood(lh[0], lh[1], target[i]) for i, lh in enumerate(likelihood_list)])
    trial_lh = comb_likelihood([eval_likelihood(lh[0], lh[1], trial[i]) for i, lh in enumerate(likelihood_list)])

    if trial_lh > target_lh:
        if not any(np.array_equal(trial, indiv) for indiv in population):
            population[target_id] = trial

    population_list.append(population)

    improvement = max(trial_lh-target_lh, 0)

    print("\nTarget likelihood:", target_lh)
    print("Trial likelihood:", trial_lh)
    print("Improvement:", improvement)

    print("\nnumber of populations: ", len(population_list))
    print("-------------------")

    if 0 < improvement < conv_threshold:
        break

print("\nFinal population:")
for point in population:
    print(point)
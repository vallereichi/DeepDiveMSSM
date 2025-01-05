import numpy as np
import random
import likelihoods




# Initialization
def initialize(parameter_space:list[tuple], NP:int) -> list[np.array]:
    """
    initialize the first generation of target vectors. The initialization randomly selects points from the parameter space and creates NP population points.

    parameters:
        parameter_space: list of tuples containing the ranges in all the dimensions of the parameter space
        NP:              size of population

    returns:    
        population of points in the parameter space
    """
    population = []
    for _ in range(NP):
        point = []
        for dim in parameter_space:
            point.append(random.uniform(dim[0], dim[1]))
        population.append(np.array(point))
    return population



# Mutation
def mutation(population:list[np.array], F:float, parameter_space:list[tuple]) -> list[np.array]:
    """
    Mutate the population using the DE/rand/1 mutation strategy.

    parameters:
        population:      list of points in the parameter space
        F:               mutation factor
        parameter_space: list of tuples containing the ranges in all the dimensions of the parameter space
    
    returns:
        mutated population
    """
    NP = len(population)
    mutated_population = []
    for i in range(NP):
        a, b, c = random.sample(population, 3)
        x = population[i]
        v = a + F*(b - c)
        
        # Ensure that the mutated vector is within the parameter space  TODO: create more implementations
        for j in range(len(v)):
            v[j] = max(min(v[j], parameter_space[j][1]), parameter_space[j][0])        


        mutated_population.append(v)
    return mutated_population


# Crossover
def crossover(population:list[np.array], mutated_population:list[np.array], CR:float) -> list[np.array]:
    """
    Perform the crossover operation between the population and the mutated population.

    parameters:
        population:          list of points in the parameter space
        mutated_population:  list of points in the parameter space
        CR:                  crossover rate
    
    returns:
        crossovered population
    """
    NP = len(population)
    crossovered_population = []
    for i in range(NP):
        x = population[i]
        v = mutated_population[i]
        u = np.zeros_like(x)
        for j in range(len(x)):
            if random.random() < CR:
                u[j] = v[j]
            else:
                u[j] = x[j]
        crossovered_population.append(u)

    l = random.randint(0, len(x)-1)
    crossovered_population[l] = population[l]

    return crossovered_population


# Selection
def selection(population:list[np.array], crossovered_population:list[np.array], lh:list[tuple]) -> list[np.array]:
    """
    Select the best population between the original population and the crossovered population.

    parameters:
        population:          list of points in the parameter space
        crossovered_population:  list of points in the parameter space
        lh:                      list of likelihood functions for each dimension of the parameter space. tuple(lh_name, mu, sigma)
    
    returns:
        selected population
    """
    NP = len(population)
    lh_funcs = [getattr(likelihoods, lh[i][0]) for i in range(len(lh))]
    mus = [lh[i][1] for i in range(len(lh))]
    sigmas = [lh[i][2] for i in range(len(lh))]


    selected_population = []
    for i in range(NP):
        x = population[i]
        u = crossovered_population[i]

        likelihood = lambda x: sum([lh_funcs[j](x[j], mus[j], sigmas[j]) for j in range(len(x))])
        if likelihood(u) > likelihood(x):
            selected_population.append(u)
        else:
            selected_population.append(x)
    return selected_population


# calculate average combined log likelihood of population
def average_combined_log_likelihood(population:list[np.array], lh:list[tuple]) -> float:
    """
    Calculate the average combined log likelihood of the population.

    parameters:
        population: list of points in the parameter space
        lh:         list of likelihood functions for each dimension of the parameter space. tuple(lh_name, mu, sigma)
    
    returns:
        average combined log likelihood of the population
    """
    NP = len(population)
    lh_funcs = [getattr(likelihoods, lh[i][0]) for i in range(len(lh))]
    mus = [lh[i][1] for i in range(len(lh))]
    sigmas = [lh[i][2] for i in range(len(lh))]

    likelihoods_tmp = [sum([lh_funcs[j](x[j], mus[j], sigmas[j]) for j in range(len(x))]) for x in population]
    return np.mean(likelihoods_tmp)

def best_likelihood_point(population:list[np.array], lh:list[tuple]) -> float:
    """
    Get the best point in the parameter space based on the likelihoods.

    parameters:
        lh: list of likelihoods for each point in the parameter space. tuple(lh_name, mu, sigma)
    
    returns: float
    """
    lh_funcs = [getattr(likelihoods, lh[i][0]) for i in range(len(lh))]
    mus = [lh[i][1] for i in range(len(lh))]
    sigmas = [lh[i][2] for i in range(len(lh))]

    likelihoods_tmp = [sum([lh_funcs[j](x[j], mus[j], sigmas[j]) for j in range(len(x))]) for x in population]
    return population[np.argmax(likelihoods_tmp)]





# Main DE function for rand/1/bin
def rand_one_bin(parameter_space:list[tuple], NP:int, F:float, CR:float, lh:list[tuple], convergence_thresh:float = 1e-3, max_generations:int = 10000) -> list[np.array]:
    """
    Perform the Differential Evolution algorithm.

    parameters:
        parameter_space: list of tuples containing the ranges in all the dimensions of the parameter space
        NP:              size of population
        F:               mutation factor
        CR:              crossover rate
        lh:              list of likelihood functions for each dimension of the parameter space. tuple(lh_name, mu, sigma)
        convergence_thresh: threshold for convergence
        max_generations: maximum number of generations

    returns:
        best point in the parameter space
    """
    diff = 1
    count = 0
    generations = []
    population = initialize(parameter_space, NP)
    generations.append(population)

    while diff > convergence_thresh and count < max_generations:
        mutated_population = mutation(population, F, parameter_space)
        crossovered_population = crossover(population, mutated_population, CR)
        population = selection(population, crossovered_population, lh)

        generations.append(population)
        diff = abs(average_combined_log_likelihood(population, lh) - average_combined_log_likelihood(generations[-2], lh))
        count += 1
    return generations


# advanced mutation and crossover strategies
def genearalized_mutation(population:list[np.array],x_1:tuple, F:list[float], Q:float, lambda_:float, lh:list[tuple]) -> list[np.array]:
    """
    Perform the generalized mutation operation.

    parameters:
        population: list of points in the parameter space
        x_1: point in the parameter space. tuple(nü.array, idx)
        F: list of mutation factors
        Q: number of difference vectors
        lambda_: mutation rate
        lh: list of likelihood functions for each dimension of the parameter space. tuple(lh_name, mu, sigma)
    
    returns:
        mutated population
    """
    x_best = best_likelihood_point(population, lh)
    random_sample = random.sample(population, 2*Q)
    for i in range(2*Q):
        if np.array_equal(random_sample[i], x_1[0]) == True:
            random_sample = random.sample(population, 2*Q)
            break

    b = random_sample[:Q]
    c = random_sample[Q:]
    Sum = sum([F[j]*(b[j] - c[j]) for j in range(Q-1)])

    v = lambda_*x_best + (1-lambda_)*x_1[0] + Sum
    mutated_population = population.copy()
    mutated_population[x_1[1]] = v

    return mutated_population
    





# Testing
def test():
    # example data
    parameter_space = [(2, 43), (0, 99)]
    NP = 10
    F = 0.8
    Cr = 0.8

    lh_list = [
        ("gaussian", 10, 30),
        ("gaussian", 50, 20)
    ]

    population = initialize(parameter_space, NP)
    mutated_population = genearalized_mutation(population, (population[0], 0), [0.8, 0.9], 3, 0.5, lh_list)
    crossovered_population = crossover(population, mutated_population, Cr)
    selected_population = selection(population, crossovered_population, lh_list)


    print("\nParameter Space:")
    print(parameter_space)
    print("\nPopulation:")
    for i in population:
        print(i)

    print("\nMutated Population:")
    for i in mutated_population:
        print(i)

    print("\nCrossovered Population:")
    for i in crossovered_population:
        print(i)

    print("\nSelected Population:")
    for i in selected_population:
        print(i)




if __name__ == "__main__":
    test()

    generations = rand_one_bin([(2, 43), (0, 99)], 10, 0.8, 0.8, [("gaussian", 10, 30), ("gaussian", 50, 20)], 1e-3, 10000)
    print(len(generations))



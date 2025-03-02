import time
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from de import *

def main():
    print("running Differential Evolution")
    times = []
    processes = range(10,1000)

    for NP in tqdm(processes):

        start_time = time.time()
        population = initialize_population(NP, ranges)
        population_list = [population]
        improvement = 0

        while len(population_list) < MAX_ITER:
            population, improvement = update(population, mutate_rand_one, crossover_bin)
            population_list.append(population)

            if 0 < improvement < conv_threshold:
                break

        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        

    print(len(times))
    
    plt.scatter(processes, times, marker='.', color='coral', alpha=0.5, label="rand/1/bin")
    plt.xlabel("NP")
    plt.ylabel("time in s")
    plt.legend()
    plt.savefig("test_results.png", dpi=1000)

    with open("test_data.csv", 'w') as file:
        for t in times:
            file.write(str(t))
    



if __name__ == "__main__":
    main()

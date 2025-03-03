import time
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from de import *

def main():

    ranges = [
        [20, 60],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
        [30, 90],
    ]

    fig1 = plt.figure(figsize=(5,5))
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel("NP")
    ax1.set_ylabel("time in s")
    
    fig2 = plt.figure(figsize=(5,5))
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel("NP")
    ax2.set_ylabel("time in s")

    for i in range(0,90,10):
        test_ranges = ranges[:100-i]
        print("running Differential Evolution with ", str(len(test_ranges)), " parameters")
        times_total = []
        times_update = []
        processes = range(10,1000)

        for NP in tqdm(processes):

            start_time = time.time()
            population = initialize_population(NP, test_ranges)
            population_list = [population]
            improvement = 0

            mean_time_update = []

            while len(population_list) < MAX_ITER:
                start = time.time()
                population, improvement = update(population, mutate_rand_one, crossover_bin)
                end = time.time()
                mean_time_update.append(end-start)
                population_list.append(population)

                if 0 < improvement < conv_threshold:
                    break
                
                
            end_time = time.time()
            elapsed_time_total = end_time - start_time
            elapsed_time_update = np.mean(mean_time_update)
            times_total.append(elapsed_time_total)
            times_update.append(elapsed_time_update)
        
        ax1.scatter(processes, times_total, marker='.', alpha=0.5, label=f"{len(test_ranges)} parameters")
        ax2.scatter(processes, times_update, marker='.', alpha=0.5, label=f"{len(test_ranges)} parameters")

    ax1.legend()
    fig1.tight_layout()
    fig1.savefig("total_time.png", dpi=1000)

    ax2.legend()
    fig2.tight_layout()
    fig2.savefig("update_time.png", dpi=1000)

    



if __name__ == "__main__":
    main()

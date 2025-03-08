import time, os
from tqdm import tqdm
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from de import *



def main():

    ranges = [[0,100]]
    start_population_size = 10
    end_population_size = 500
    step_size = 10

    if not os.path.isfile("test_results"):
        test_results = {}
        file = open('test_results', 'ab')
        pickle.dump(test_results, file)
        file.close()
    else:
        file = open("test_results", 'rb')
        test_results = pickle.load(file)
        start_population_size = max([int(i.split()[0]) for i in test_results.keys()]) + step_size

    for i in range(start_population_size,end_population_size,step_size):
        test_ranges = ranges*i
        print("running Differential Evolution with ", str(len(test_ranges)), " parameters")
        times_total = []
        times_update = []
        n_steps = []
        processes = range(10,1000)

        for NP in tqdm(processes):

            start_time_total = time.time()
            population = initialize_population(NP, test_ranges)
            population_list = [population]
            improvement = 0

            mean_time_update = []

            while len(population_list) < MAX_ITER:
                start_time_update = time.time()
                population, improvement = update(population, mutate_rand_one, crossover_bin)
                end_time_update = time.time()
                mean_time_update.append(end_time_update-start_time_update)
                population_list.append(population)

                if 0 < improvement < conv_threshold:
                    break
                
                
            end_time_total = time.time()
            elapsed_time_total = end_time_total - start_time_total
            elapsed_time_update = np.mean(mean_time_update)
            times_total.append(elapsed_time_total)
            times_update.append(elapsed_time_update)
            n_steps.append(len(population_list))

        
        file = open("test_results", 'rb')
        test_results = pickle.load(file)
        file.close()

        test_results[f"{len(test_ranges)} parameters"] = {
                "times total": times_total,
                "times update": times_update,
                "iterations": n_steps,
            }
        
        file = open("test_results", 'wb')
        pickle.dump(test_results, file)
        file.close()
        
        

    
    



if __name__ == "__main__":
    main()

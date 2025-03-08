import time
from tqdm import tqdm
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

from de import *

def save_to_file(df:dict, file_path:str) -> None:
    file = open(file_path, 'ab')
    pickle.dump(df, file)
    file.close()

def main():

    ranges = [[0,100]]
     

    for i in range(10,500,10):
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

        
        test_results = {
            f"{len(test_ranges)} parameters": {
                "times total": times_total,
                "times update": times_update,
                "iterations": n_steps,
            }
        }
        save_to_file(test_results, "test_results")

    
    



if __name__ == "__main__":
    main()

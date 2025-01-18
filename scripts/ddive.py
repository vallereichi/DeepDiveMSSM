
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import util
from scan_info import scan_info

"""
define defaults for testing 
"""
path_to_runs = "../runs"
path_to_diver_scan = "../runs/MSSM_diver/samples/DIVER.hdf5"
path_to_random_scan = "../runs/MSSM_random/samples/RANDOM.hdf5"

COLORS = ['coral', 'darkcyan', 'orchid', 'darkseagreen', 'goldenrod']

observable_list = ["h0_1", "h0_2"]






"""
function declarations
"""
def search_observable(scan:pd.DataFrame, search:str) -> str:
    """
    Find a search string in a pandas dataframe and return the key of the column.

    parameters:
        scan: pandas dataframe
        search: string to search for

    returns:
        key of the column as string
    """
    key = ''
    for string in scan_list[0][1].keys():
        if re.search(f'{search}(?!.*_isvalid)', string) is not None:
            key = string
            print("Key found: ", key)
            break

    if key == '':
        raise ValueError(f"no key found for '{search}'")
    
    return key


def get_dimension(observable_key:str) -> str:
    """
    determine the unit of the observable

    parameters:
        observable_key: key of the observable

    returns:
        string with the unit of the observable
    """
    dim = ''
    if re.search('Pole_Mass', observable_key) is not None:
        dim = "mass [GeV]"

    return dim



# create plots
def scatter_2d(scan_list:list[tuple], observable_list:list[str]) -> None:
    """
    create a 2D scatter plot of two observables

    parameters:
        scan_list: list of scans
        observable_list: list of observables to plot. length must be even

    returns:
        None
    """
    keys = [search_observable(scan_list[0], observable) for observable in observable_list]
    dimensions = [get_dimension(key) for key in keys]

    # start 2D scatter plot
    for scan in scan_list:
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.scatter(scan[1][keys[0]], scan[1][keys[1]], c=scan[1]['plr'], cmap='viridis', s=10)
        ax.set_xlabel(f"{observable_list[0]} {dimensions[0]}")
        ax.set_ylabel(f"{observable_list[1]} {dimensions[1]}")
        ax.set_title(scan[0])

        fig.tight_layout()
        #plt.show()
        fig.savefig(f"../plots/2D_scatter_plot_{observable_list[0]}_{observable_list[1]}_{scan[0]}.png")

        # TODO: add better colomap
        # TODO: maybe create Observable class to handle the keys and dimensions
        # TODO: add capability to handle more than two observables

    return


def plot_plr(scan_list:list[tuple], observable_list:list[str]) -> None:
    """
    create a 2D scatter plot of two observables

    parameters:
        scan_list: list of scans
        observable_list: list of observables to plot. length must be even

    returns:
        None
    """
    keys = [search_observable(scan_list[0], observable) for observable in observable_list]
    dimensions = [get_dimension(key) for key in keys]

    # start profile likelihood ratio plot
    for id_obs, obs in enumerate(observable_list):
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        for id_scan, scan in enumerate(scan_list):
            ax.scatter(scan[1][keys[id_obs]], scan[1]['plr'], c=COLORS[id_scan], alpha=0.5)
        ax.set_xlabel(f"{obs} {dimensions[id_obs]}")
        ax.set_ylabel("Profile Likelihood Ratio $\\mathcal{L}$")
        

        fig.tight_layout()
        #plt.show()
        fig.savefig(f"../plots/plr_plot_{obs}.png")

        # TODO: add labels
        # TODO: pull key finding out of functions
        return
    


def hist_1d(scan_list:list[tuple], observable_list:list[str]):
    keys = [search_observable(scan_list[0], observable) for observable in observable_list]
    dimensions = [get_dimension(key) for key in keys]

    # calculate bins
    for id_obs, obs in enumerate(observable_list):
        n_bins = 20
        bin_range = abs(scan_list[0][1][keys[id_obs]].max() - scan_list[0][1][keys[id_obs]].min())
        step_size = bin_range // n_bins
        bins = np.arange(scan_list[0][1][keys[id_obs]].min(), scan_list[0][1][keys[id_obs]].max(), step_size)
        print("calculated bins: ", bin_range, step_size, bins)

        # start 1D histogram plot
        counts = [] 
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(211)
        for id_scan, scan in enumerate(scan_list):
            count, _, _ = ax.hist(scan[1][keys[id_obs]], bins=bins, alpha=0.5, color=COLORS[id_scan+1])
            counts.append(count)
        ax.set_ylabel("Counts")



        fig.tight_layout()
        #plt.show()
        fig.savefig(f"../plots/hist_plot_{obs}.png")



# Entry point
if __name__ == "__main__":

    scan_list = util.load_hdf5_file(path_to_runs)
    scatter_2d(scan_list, observable_list)
    plot_plr(scan_list, observable_list)
    hist_1d(scan_list, observable_list)
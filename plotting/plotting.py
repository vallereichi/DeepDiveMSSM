import re 
import h5py
import argparse
import numpy as np
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt

"""
handle command line options
"""
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', nargs='+', required=True, help="choose at least one input file with file format '*.hdf5'. When more than one file is provided comparison plots are created. Therefore it is no longer possible to plot multiple observables in the same figure.")
parser.add_argument('-s', '--search', nargs='*', required=True, help="select a list of observables which you intend to plot. If only this option is selected, the script will by default plot every observable ageinst the profile likelihood ratio")
parser.add_argument('-l', '--labels', nargs='*', help="provide labels for the legend or titles. If this option is set it must be of same length as 'search'")
parser.add_argument('-c', '--compare', action='store_true', help="create comparison plots for different scans. More than one input file must be provided")
parser.add_argument('-i', '--individual', action='store_true', help="if this option is set, all desired observables will be plotted individually")
parser.add_argument('--hist', action='store_true', help="if this option is set, all observables are plotted as histograms")

args = parser.parse_args()

#sanity checks
if args.labels is not None:
    if len(args.search) != len(args.labels):
        raise ValueError("'--search' opion and '--labels' option must be of same length")

if args.compare == True and len(args.file) < 2:
    raise ValueError("in order to create comparison plots you must provide more than one input file")


"""
loading input files
"""
@dataclass
class Scan:
    name: str
    data: pd.DataFrame
    plr: list
    num_points: int

@dataclass
class Observable:
    label: str
    key: str
    dimension: str

scans = []
for file in args.file:
    dataset = h5py.File(file, 'r')['MSSM']
    scan_data = {}
    for key in dataset.keys():
        scan_data[key] = dataset[key][:]

    scan_data = pd.DataFrame(scan_data)
    scan_data = scan_data[scan_data['LogLike_isvalid'] == 1]
    plr = np.exp(scan_data['LogLike'] - scan_data['LogLike'].max())

    name = str(file.split("/")[-1].strip('.hdf5'))
    scans.append(Scan(name, scan_data, plr, len(scan_data['LogLike'])))

observables = []
for id, item in enumerate(args.search):
    if args.labels is not None:
        label = args.labels[id]
    else:
        label = item
    key = ''

    for str in dataset.keys():
        if re.search(f'{item}(?!_isvalid)', str) is not None:
            key = str
            break
    
    if key == '':
        raise ValueError(f"{item} not found in keys")
    
    dimension = ""
    if re.search('Pole_Mass', key) is not None:
        dimension = "mass [GeV]"
    
    observables.append(Observable(label, key, dimension))



"""
creating the plots
"""
def plot_plr(scans: list[Scan], observables: list[Observable]) -> None:
    """
    creates one figure for all observables specified as command line options as scatter plots
    against the profile likelihood ratio.
    with this function no comparison plots for two different scans can be made.

        scans: list of'Scan' objects that contains the output data from a gambit scan.
        observables: list of 'Observable' objects that are intended for the plot

    returns:
        None. The plot is instead saved as a pdf
    """
    for scan in scans:
        fig = plt.figure()

        ax = fig.add_subplot(111)

        dim = []

        for obs in observables:
            dim.append(obs.dimension)
            ax.scatter(scan.data[obs.key], scan.plr, marker='.', alpha=0.5, label=obs.label)

        if dim.count(dim[0]) != len(observables):
            raise ValueError("if you want to plot different observables in one scatter plot, all the dimesnions must be the same")

        ax.set_xlabel(dim[0])
        ax.set_ylabel("Profile Likelihood Ratio")

        ax.minorticks_on()
        ax.legend(frameon=False, draggable=True)
        ax.set_title(scan.name)

        fig.tight_layout()

        plt.show()
    
    return
    

def plot_plr_comparison(scans:list[Scan], observables:list[Observable]) -> None:
    """
    creates comparison plots for the different provided scans.
    All Observables are plotted in different figures.

        scans: list of'Scan' objects that contains the output data from a gambit scan.
        observables: list of 'Observable' objects that are intended for the plot

    returns:
        None. The plot is instead saved as a pdf
     """
    for obs in observables:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for scan in scans:
            ax.scatter(scan.data[obs.key], scan.plr, marker='.', alpha=0.5, label=scan.name)
        
        ax.set_xlabel(f'{obs.label} {obs.dimension}')
        ax.set_ylabel("Profile Likelihood Ratio")
        
        ax.legend(frameon=False, draggable=True)
        ax.minorticks_on()

        plt.show()




"""
conditionals
"""
if args.hist == False and args.individual == False and args.compare == False:
    plot_plr(scans, observables)

if args.hist == False and args.compare == True:
    plot_plr_comparison(scans, observables)





    
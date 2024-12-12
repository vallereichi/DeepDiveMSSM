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
parser.add_argument('-m', '--mode', choices=['compare'], help="choose how to display the plots. The option compare will create plots with data from all scans on one axis")
parser.add_argument('-t', '--type', choices=['plr', 'hist'], help="choose a plot type")


args = parser.parse_args()

#sanity checks
if args.labels is not None:
    if len(args.search) != len(args.labels):
        raise ValueError("'--search' opion and '--labels' option must be of same length")


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

    for string in dataset.keys():
        if re.search(f'{item}(?!_isvalid)', string) is not None:
            key = string
            break
    
    if key == '':
        raise ValueError(f"{item} not found in keys")
    
    dimension = ""
    if re.search('Pole_Mass', key) is not None:
        dimension = "mass [GeV]"
    
    observables.append(Observable(label, key, dimension))


"""
helper function
"""
def create_grid(len:int) -> tuple[int]:
    """
    specifies the grid when plotting multiple axis in one figure

        len: length of either the 'scans' or 'observables' depending on the  type of plot

    reuturns:
        (nrows, ncols) number of rows and colums in one figure based on the number of plots
    """
    ncols = int(np.ceil(np.sqrt(len)))
    nrows = int(np.ceil(len / ncols))

    return (nrows, ncols)

def create_figure(scans:list[Scan], observables:list[Observable], mode:str, plot_type:str) -> tuple:
    """
    this helper function creates the figure in different configurations specified by the mode

        scans: list of'Scan' objects that contains the output data from a gambit scan.
        observables: list of 'Observable' objects that are intended for the plot        
        mode: options are 'scan' or 'obs' depending on what should be placed as subplots. Default is None. In this case a new figure is created for every plot
        
    returns:
        None. But the figure and axis objects are created
    """
    num_axes = len(scans) + len(observables)
    figs = []
    axs = []

    if plot_type == "plr":
        ylabel = "Profile Likelihood Ratio"
    if plot_type == "hist":
        ylabel = "counts"


    if mode == "default":

        for scan in scans:
            for obs in observables:
                fig, _ = plt.subplots()
                ax = fig.add_subplot(111)

                ax.set_xlabel(f'{obs.label} {obs.dimension}')
                ax.set_ylabel(ylabel)
                ax.set_title(scan.name)
                ax.minorticks_on()

                figs.append(fig)
                axs.append(ax)

    if mode == "compare":

        for obs in observables:
            fig, _ = plt.subplots()
            ax = fig.add_subplot(111)
            
            ax.set_xlabel(obs.dimension)
            ax.set_ylabel(ylabel)
            ax.legend([scan.name for scan in scans])
            ax.minorticks_on()

            figs.append(fig)
            axs.append(ax)
                
    return (figs, axs)

        
                




"""
creating the plots
"""
#def plot_plr(scans: list[Scan], observables: list[Observable]) -> None:
#    """
#    creates one figure for all observables specified as command line options as scatter plots
#    against the profile likelihood ratio.
#    with this function no comparison plots for two different scans can be made.
#
#        scans: list of'Scan' objects that contains the output data from a gambit scan.
#        observables: list of 'Observable' objects that are intended for the plot
#
#    returns:
#        None. The plot is instead saved as a pdf
#    """
#    for scan in scans:
#        fig = plt.figure()
#
#        ax = fig.add_subplot(111)
#
#        dim = []
#
#        for obs in observables:
#            dim.append(obs.dimension)
#            ax.scatter(scan.data[obs.key], scan.plr, marker='.', alpha=0.5, label=obs.label)
#
#        if dim.count(dim[0]) != len(observables):
#            raise ValueError("if you want to plot different observables in one scatter plot, all the dimesnions must be the same")
#
#        ax.set_xlabel(dim[0])
#        ax.set_ylabel("Profile Likelihood Ratio")
#
#        ax.minorticks_on()
#        ax.legend(frameon=False, draggable=True)
#        ax.set_title(scan.name)
#
#        fig.tight_layout()
#
#        plt.show()
#    
#    return
#   
#
#def plot_plr_comparison(scans:list[Scan], observables:list[Observable]) -> None:
#    """
#    creates comparison plots for the different provided scans.
#    All Observables are plotted in different figures.
#
#        scans: list of'Scan' objects that contains the output data from a gambit scan.
#        observables: list of 'Observable' objects that are intended for the plot
#
#    returns:
#        None. The plot is instead saved as a pdf
#     """
#    for obs in observables:
#        fig = plt.figure()
#        ax = fig.add_subplot(111)
#
#        for scan in scans:
#            ax.scatter(scan.data[obs.key], scan.plr, marker='.', alpha=0.5, label=scan.name)
#        
#        ax.set_xlabel(f'{obs.label} {obs.dimension}')
#        ax.set_ylabel("Profile Likelihood Ratio")
#        
#        ax.legend(frameon=False, draggable=True)
#        ax.minorticks_on()
#
#        plt.show()




"""
conditionals
"""
if args.mode is None:
    figs, axs = create_figure(scans, observables, 'default', args.type)

    axs[0].scatter(scans[0].data[observables[0].key], scans[0].plr, marker='.', alpha=0.5)
    

    plt.show()




    
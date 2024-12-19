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
    figs = []
    axs = []


    if plot_type == "plr":
        ylabel = "Profile Likelihood Ratio"
        def set_data(ax, xdata, ydata, norm):
            ax.scatter(xdata, ydata, marker='.', alpha=0.5)
            return
    if plot_type == "hist":
        ylabel = "counts"
        def set_data(ax, xdata, ydata, norm):
            ax.hist(xdata, bins=20, alpha=0.5, density=norm)
            return


    if mode == "default":

        normalize = False

        for scan in scans:
            for obs in observables:
                fig, ax = plt.subplots()
        
                set_data(ax, scan.data[obs.key], scan.plr, normalize)

                ax.set_xlabel(f'{obs.label} {obs.dimension}')
                ax.set_ylabel(ylabel)
                ax.set_title(scan.name)
                ax.minorticks_on()

                fig.tight_layout()

                figs.append(fig)
                axs.append(axs)

                

    if mode == "compare":

        normalize = True

        for obs in observables:
            fig, ax = plt.subplots()

            for scan in scans:
                set_data(ax, scan.data[obs.key], scan.plr, normalize)
            
            ax.set_xlabel(f'{obs.label} {obs.dimension}')
            ax.set_ylabel(ylabel)
            ax.legend([scan.name for scan in scans])
            ax.minorticks_on()

            
            fig.tight_layout()

            figs.append(figs)
            axs.append(ax)
            
                
    return  (figs, axs)                   




"""
conditionals
"""
if args.mode is None:
    mode = 'default'
if args.mode == 'compare':
    mode = 'compare'


figs, axs = create_figure(scans, observables, mode, args.type)

   



plt.show()
    
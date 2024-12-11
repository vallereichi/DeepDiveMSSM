import numpy as np
import matplotlib.pyplot as plt
import argparse
import re
import h5py
import pandas as pd


# handle command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file",required=True, help="file containing the output data of a scan. file format *.hdf5")
parser.add_argument("-p", "--parameter",nargs='*', help="if a parameter is provided it will get plotted against its profile likelihood ratio calculated from the scan data")
parser.add_argument("--hist", action="store_true", help="plot histogramm")
parser.add_argument("--bit", nargs="*", choices=["PrecisionBit"])
arguments = parser.parse_args()



#print waht the user wants to plot
print(f"Creating plot for {arguments.parameter}")


# find user input string in parameter list
dataset = h5py.File(arguments.file, 'r')['MSSM']
datadict = {}
parameters = []
for key in dataset.keys():
    datadict[key] = dataset[key][:]

    for param in arguments.parameter:
        if re.search(f'{param}(?!.*_isvalid)(?!.*Pole_Mixing)', key) is not None: 
            parameters.append((param, key))
            print("Key: ", key)
    
if len(parameters) == 0:
    raise ValueError(f"scan data does not contain any matching key for '{arguments.parameter}'")
            
scan = pd.DataFrame(data=datadict)
scan = scan[scan['LogLike_isvalid'] == 1]
prof_like = np.exp(scan['LogLike'] - scan['LogLike'].max())

"""
function declarations
"""
def find_parameter(parameter_name):
    for key in dataset.keys():
        keys = []
        if re.search(f'{parameter_name}(?!.*_isvalid)', key) is not None:
            keys.append(key)
            print("Key: ", key)
        
    return keys

def plot_prof_lh():

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)

    for param in parameters:
        ax.scatter(x=scan[param[1]], y=prof_like, marker='.', alpha=0.5, label=f"{param[0]}")

    ax.set_xlabel("mass [GeV]")
    ax.set_ylabel("Profile Likelihood Ratio")

    ax.minorticks_on()
    ax.legend()

    plt.show()

    
def plot_hist():
    

    fig = plt.figure()
    if len(parameters) < 3:
        ncols = len(parameters)
    else:
        ncols = 3
    
    nrows = int(np.ceil(len(parameters)/ncols))

    for id, param in enumerate(parameters):
        ax = fig.add_subplot(nrows, ncols, id + 1)
        maximum = scan[param[1]][prof_like.idxmax()]
        
        ax.hist(scan[param[1]], bins=20, alpha=0.5, label=f"{param[0]} max: {round(maximum, 2)}")

        ax.set_xlabel("mass [GeV]")
        ax.set_ylabel("counts")
        ax.minorticks_on()

        ax.legend()

    fig.tight_layout()

    plt.show()

def plot_bits():
    bit_keys = []
    for bit in arguments.bit:
        for key in dataset.keys():
            if re.search(f'{bit}(?!.*_isvalid)', key) is not None:
                bit_keys.append(key)
                print("Key: ", key)

    

    fig = plt.figure()
    if len(parameters) < 3:
        ncols = len(parameters)
    else:
        ncols = 3
    
    nrows = int(np.ceil(len(parameters)/ncols))

    for id, param in enumerate(parameters):
        ax = fig.add_subplot(nrows, ncols, id)
        



    pass


"""
Call plot functions
"""
if arguments.hist:
    plot_hist()
else:
    plot_prof_lh()

import re
import h5py
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
handle command line options
"""
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", nargs='+', required=True)
parser.add_argument("-p", "--parameters", nargs='*')
parser.add_argument("--hist", action='store_true')
parser.add_argument("-b", "--bits", nargs='*', choices=["PrecisionBit"])

args = parser.parse_args()

print("obtaining scan data from: ")
for file in args.file:
    print(file)


"""
load scan data
"""
scans = {}

for file in args.file:
    dataset = h5py.File(file, 'r')['MSSM']
    datadict = {}
    for key in dataset.keys():
        datadict[key] = dataset[key][:]

    scan = pd.DataFrame(data=datadict)
    scan = scan[scan['LogLike_isvalid'] == 1]
    scan['PLR'] = np.exp(scan['LogLike'] - scan['LogLike'].max())
    
    scans[file] = scan

"""
finding parameters
"""
def find_observable(parameter_name:str) -> str:
    obs = ""
    for key in scans[args.file[0]].keys():
        if re.search(f'{parameter_name}(?!.*_isvalid)', key) is not None:
            obs = key
            break
    if obs == "":
        raise ValueError(f"no matching key found for '{parameter_name}'")
    
    print(f"Key found for {parameter_name}: \n{obs}")
    return obs


"""
parameter class
"""
class Parameter():
        
    def __init__(self, name, label:str = None):
        self.name = name
        if label == None:
            self.label = self.name
        else:
            self.label = label

        self.key = find_observable(self.name)
        self.dimension = ""
        self.max = [scans[file][self.key][scans[file]['PLR'].idxmax()] for file in args.file]

    def determine_dimension(self):
        if re.search(r'Pole_Mass', self.key) is not None:
            self.dimension = "mass [GeV]"    
        return self.dimension





"""
plotting
"""
#creating the figure
fig = plt.figure()


#plotting parameters from command line options
if len(args.parameters) != 0 and len(args.file) == 1:

    print(f"creating plots for {args.parameters}")
    parameters = [Parameter(parameter) for parameter in args.parameters]
    
    if args.hist:
        if len(parameters) < 3:
            ncols = len(parameters)
        else:
            ncols = 3
        nrows = int(np.ceil(len(parameters)/ncols))

        for id, par in enumerate(parameters):
            ax = fig.add_subplot(nrows, ncols, id + 1)
            ax.hist(scans[args.file[0]][par.key], bins=20, alpha=0.5, label=f"max PLR: {round(par.max[0], 2)}")

            ax.set_title(par.label)
            ax.set_xlabel(par.determine_dimension())
            ax.set_ylabel("count")

            ax.minorticks_on()
            ax.legend(frameon=False, draggable=True)

        fig.tight_layout()
        plt.show()
    
    
    else:
        ax = fig.add_subplot(111)



        xlabel = []
        legend = []


        for par in parameters:
            ax.scatter(scans[args.file[0]][par.key], scans[args.file[0]]['PLR'], marker='.', alpha=0.5, label=par.label)
            xlabel.append(par.determine_dimension())

        if xlabel.count(xlabel[0]) != len(parameters):
            raise ValueError("All parameters must have the same dimension")
        ax.set_xlabel(xlabel[0])
        ax.set_ylabel("Profile Likelihood Ratio")

        ax.legend()
        ax.minorticks_on()

        fig.tight_layout()
        plt.show()
    

if len(args.parameters) == 1 and len(args.file) > 1:

    print(f"creating plots for {args.parameters}")
    parameters = [Parameter(parameter) for parameter in args.parameters]

    if args.hist:

        ax = fig.add_subplot(111)
        for scan in args.file:
            ax.hist(scans[scan][parameters[0].key], bins=20, density=True, alpha=0.5, label=scan)

        ax.set_xlabel(parameters[0].determine_dimension())
        ax.set_ylabel("counts")

        ax.minorticks_on()
        ax.legend(frameon= False, draggable=True)

        fig.tight_layout()
        plt.show()
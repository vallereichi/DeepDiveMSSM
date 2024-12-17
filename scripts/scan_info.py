#!/opt/homebrew/Caskroom/miniconda/base/envs/gambitenv/bin/python

#Author: Valentin Reichenspurner

import h5py
import argparse
import numpy as np
from dataclasses import dataclass


"""
handling command line options
"""
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', required=True, nargs='+', help="filepaths to the scan data")

args = parser.parse_args()




"""
load files
"""
@dataclass
class Scan:
    name: str
    data: str
    length: int
    num_points: int
    num_valid_points: int

scans = []
for file in args.file:
    hdf5 = h5py.File(file, 'r')['MSSM']
    data = {}
    
    for key in hdf5.keys():
        data[key] = hdf5[key][:]

    name = str(file.split("/")[-1].strip('.hdf5'))
    length = len(hdf5.keys())
    num_points = len(data['LogLike'])
    num_valid_points = list(data['LogLike_isvalid']).count(1)

    scans.append(Scan(name, data, length, num_points, num_valid_points))


for scan in scans:
    print("#############################################################")
    print("Scan: ", scan.name, "\n")
    print("Keys: ", scan.length, "\n")
    print("Number of points: ", scan.num_points, "\n")
    print("Valid logs: ", scan.num_valid_points, "\n")
    



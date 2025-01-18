import os
import h5py
import pandas as pd
import numpy as np
from pathlib import Path

def load_hdf5_file(path:str) -> list:
    """
    load a hdf5 file and return a list of pandas dataframes with a name associated to the file.
    Each dataframe only contains valid points and a column with the profile likelihood ratio is added.

    parameters:
        path: pass a path to a hdf5 file or a directory containing hdf5 files

    returns:
        list of tuples with the name of the scan and the pandas dataframe
    """

    if os.path.isdir(path):
        scans = []
        hdf5_paths = [p for p in Path(path).rglob('*.hdf5')]
        for file in hdf5_paths:
            scans.append(load_hdf5_file(file)[0])
        return scans

    # load hdf5 files
    hdf5 = h5py.File(path, 'r')
    group_key = [key for key in list(hdf5.keys()) if key != 'metadata'][0]
    dataset = hdf5[group_key]

    # create pandas dataframe
    dataframe = {}
    for key in dataset.keys():
        dataframe[key] = dataset[key][:]
    scan = pd.DataFrame(dataframe)
    scan_name = os.path.splitext(os.path.basename(path))[0]
    print("File loaded: ", scan_name, "; ", path)

    # choose only valid points
    scan = scan[ scan['LogLike_isvalid'] == 1 ]

    # calculate profile likelihood ratio
    scan['plr'] = np.exp(scan['LogLike'] - scan['LogLike'].max())

    return [(scan_name, scan)]
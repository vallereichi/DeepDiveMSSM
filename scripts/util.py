import os
import h5py
import pandas as pd
import numpy as np
from pathlib import Path

"""
declare classes
"""


class Scan(pd.DataFrame):
    def __init__(self, name:str, data:dict):
        super().__init__(data)
        self.name = name
        
class Observable:
    def __init__(self, search_key:str, key:str, unit:str, label:str = None):
        self.search_key = search_key
        self.key = key
        self.unit = unit

        if label is None:
            self.label = search_key

    def __repr__(self):
        return f"Observable: {self.search_key} -> {self.key} ({self.unit})"

"""
declare helper functions
"""
def load_hdf5_file(path:str) -> list[Scan]:
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
    df = pd.DataFrame(dataframe)
    scan_name = os.path.splitext(os.path.basename(path))[0]
    print("File loaded: ", scan_name, "; ", path)

    # choose only valid points
    df = df[ df['LogLike_isvalid'] == 1 ]

    # calculate profile likelihood ratio
    df['plr'] = np.exp(df['LogLike'] - df['LogLike'].max())

    # create scan object
    scan = Scan(scan_name, df)

    return [scan]

def load_csv_file(path:str) -> list[Scan]:
    df = pd.read_csv(path)
    scan_name = os.path.splitext(os.path.basename(path))[0]
    print("File loaded: ", scan_name, "; ", path)
    scan = Scan(scan_name, df)

    return [scan]
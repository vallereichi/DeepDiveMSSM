import re
import os
import h5py
import pandas as pd
import numpy as np
from classes import Scan, Observable

"""
load files
"""
def load_hdf5(path:str) -> tuple[str, pd.DataFrame]:
    data ={}

    with h5py.File(path, 'r') as hdf5:
        for group in hdf5.keys():
            if group != "metadata":
                for key in hdf5[group].keys():
                    data[key] = hdf5[group][key][:]

    data = pd.DataFrame(data)
    name = os.path.splitext(os.path.basename(path))[0]

    print("file loaded: ", path)

    return name, data


def create_Scan_object(name:str, data:pd.DataFrame) -> Scan:
    num_keys = data.shape[1]
    num_points = data.shape[0]

    valid_logs = data[data['LogLike_isvalid'] == 1]
    num_valid_points = valid_logs.shape[0]

    plr = np.exp(valid_logs['LogLike'] - valid_logs['LogLike'].max())

    return Scan(name, valid_logs, plr, num_keys, num_points, num_valid_points)




def create_Observable_object(search_key:str, label:str , key_list:list) -> Observable:
    key = ''
    for string in key_list:
        if re.search(f'{search_key}(?!.*_isvalid)', string) is not None:
            key = string
            print("found key: ", key)
            break
    
    if key == '':
        raise ValueError(f"no key found for '{search_key}'")
    
    dimension = ""
    if re.search('Pole_Mass', key) is not None:
        dimension = "mass [GeV]"

    return Observable(search_key, label, key, dimension)




def print_scan_info(scan:Scan) -> None:
    print(f"\n\n++++++++    {scan.name} SCAN    ++++++++\n")
    print("     Keys: ", scan.num_keys)
    print("     Points: ", scan.num_points)
    print("     valid Points: ", scan.num_valid_points)
    print("\n\n")



def test():
    scan, scan_data = load_hdf5("runs/MSSM_diver/samples/DIVER.hdf5")
    scan = create_Scan_object(scan, scan_data)
    print_scan_info(scan)


if __name__ == '__main__':
    test()
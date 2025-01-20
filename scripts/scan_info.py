import pandas as pd
import argparse
import os
from util import Scan, load_hdf5_file

def scan_info(scan:Scan) -> None:
    """
    print out information about a scan

    parameters:
        scan: tuple with the name of the scan and the corresponding pandas dataframe

    returns:
        None
    """
    print(f"\n\n++++++++    {scan.name} SCAN    ++++++++\n")
    print("    number of keys:          ", len(scan.keys()))
    print("    number of valid points:  ", scan.shape[0])
    print("\n\n")





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Print out information about a scan.')
    parser.add_argument('-p', '--path', type=str, nargs='*', help='path(s) to the hdf5 file(s) or directory containing hdf5 files')
    args = parser.parse_args()

    if args.path is not None:
        print("Loading scans from the specified path(s).")
        scan_list = []

        for path in args.path:
            if not os.path.exists(path):
                raise ValueError(f"Path {path} does not exist.")
            
            if os.path.isdir(path):
                scan_list = load_hdf5_file(path)
            else:
                scan_list.append(load_hdf5_file(path)[0])
        
    else:
        print("No path specified. Loading all scans from the runs directory.")
        scan_list = load_hdf5_file("../runs")

    for scan in scan_list:
        scan_info(scan)
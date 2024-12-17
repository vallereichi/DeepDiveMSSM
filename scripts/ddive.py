#!/opt/homebrew/Caskroom/miniconda/base/envs/gambitenv/bin/python

import os
import re
import util
import plots
import argparse
from pathlib import Path


"""
command line options
"""
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', nargs='+', required=True, help="select one or more filepaths")
parser.add_argument('-i', '--info', action='store_true', help="print general info about the selected input files")
parser.add_argument('-o', '--observable', help="if provided this observable will be searched for and then gets plotted")
parser.add_argument('-l', '--label', help="specify a label for the provided observable other than its plain text value")
parser.add_argument('-m', '--mode', choices=['plr', 'hist'], help="choose how to plot the data")

args = parser.parse_args()
""""""

# load data
scans = []

for path in args.path:
    if os.path.isdir(path):
        # gambit output file structure: scan/samples/*.hdf5
        files = [p for p in Path(path).rglob('*.hdf5')]
        for file in files:
            scan_name, scan_data = util.load_hdf5(file)
            scans.append(util.create_Scan_object(scan_name, scan_data))


    else:
        scan_name, scan_data = util.load_hdf5(path)
        scans.append(util.create_Scan_object(scan_name, scan_data))


# load observable
if args.label is None:
    label = args.observable
else:
    label = args.label

observable = util.create_Observable_object(args.observable, label, scans[0].data.columns)


# info print 
if args.info:
    for scan in scans:
        util.print_scan_info(scan)

    if args.observable is None:
        quit()


# plot observable
if args.mode == 'plr' or args.mode == None:
    plots.plot_plr(scans, observable)



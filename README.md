# DeepDive MSSM scanning

this repository contains all the code I build for my bachelor thesis.
the different folders either provide some example code for visualizing various concepts,
or are build as tools to simplify the scan analysis.

The prospect of my thesis is to compare different scanning algorithms for MSSM models using the [GAMBIT](https://gambitbsm.org) framework.

## diver

My own implementation of the differential evolution algorithm. At the current state only the rand/1/bin algorithm is implemented, but I am planning to also include other variants such as rand-to-best, a generic mutation scheme and self adaptive variants. Once all of them are in place it will be great to also have some comparison between the algorithms and to create some insightful plots

## scripts

Everything in this folder handles different ouput formats from various MSSM scans. Since I am  at the moment only dealing with GAMBIT scans, I have only yet implemented support for the hdf5 file format and the GAMBIT specififc output files. The different scripts can be run as standalone scripts or from the main file "ddive.py". 

supported options:

- get general information about a scan
- create profile likeklihiood plots for the different MSSM parameters
- create histogram plots for the different MMSM parameters
- every plot can be performed as a camparison plot, when two scans are provided

## runs

This folder contains some ready to use output files from different MSSM scans

## yaml-files

Here are the input yaml files used to create the output found in the rus folder. These yaml files are written in the special input format for running GAMBIT scans.
In order to run them GAMBIT must be installed or alternatively run through a docker image.

# DeepDive MSSM scanning

this repository contains all the code I build for my bachelor thesis.
the different folders either provide some example code for visualizing various concepts,
or are build as tools to simplify the scan analysis.

The prospect of my thesis is to compare different scanning algorithms for MSSM models using the [GAMBIT](https://gambitbsm.org) framework.

### folder structure

    .
    ├── README.md
    ├── diver
    │   └── de.py
    ├── plotting
    │   ├── plotting.py
    │   └── readme.md
    └── yaml-files
        ├── MSSM.yaml
        ├── diver_mssm.yaml
        └── random_mssm.yaml

## diver

simple implementation of the Differential Evolution algorithm.

## plotting

plotting scripts for visualizing the output of a scan.

## yaml-files

input yaml files used for the scans.

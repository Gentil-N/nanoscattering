# Nanoscattering

## Setting Up Environment

***Not Tested with Windows OS***

Assuming ```virtualenv``` is installed with ```python3``` on the current system and a terminal is opened in the project root folder, run the following command:
```shell
sh ./setup.sh
```

**About DTU Clusters**

Before the previous command, this should must be run:
```shell
module load python3
```
otherwise ```python2.7``` is used with an old version of ```virtualenv```.

As a reminder, login is done through:
```shell
ssh dtu_account_name@login1.hpc.dtu.dk
```
where ```dtu_account_name``` is a personal DTU ID. Then, enter the corresponding password.

## Global Instructions

On a basic computer, the following command must be run (from the project root directory) before launching any python script in order to activate the virtual environment containing all required libraries:
```shell
source ./venv/bin/activate
```
To deactivate the virtual environment, simply run:
```shell
deactivate
```

**About DTU Clusters**

Each script has a specific launcher located into the ```dtu-hpc``` folder. For example, assuming a ```fake.py``` script being written into ```src```, a ```task_fake.sh``` file is created (see https://www.hpc.dtu.dk/?page_id=1416 for job's configuration) as well as ```launch_fake.sh``` file. The purpose of this last one is to erase the previous log files and execute the task file.

## Scripts

### main.py

All different techniques are shown in this _test_ script.

### computesurface.py

A theoretical surface _f(wavelength, particle's size) = scattering cross section_ is computed from a ```ply``` mesh with the triangle technique. For better performance, this script should be run on the cluster.

### findradius.py

A list of spectrum (exported from nanoparticles data) are compared to a theoretical surface previously computed in order to find the respective radius.

### select.py

Spectrum exporter. Should be run under a renderable environment (not on a cluster).
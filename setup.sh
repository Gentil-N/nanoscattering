#!/bin/bash
echo "------- Setting Up Environment... -------"
virtualenv venv
source ./venv/bin/activate
pip install numpy matplotlib scipy plyfile pycollada
deactivate
echo "------- Installation Successful! -------"
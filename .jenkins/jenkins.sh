#!/bin/bash -f

data_root=/project/s1053/performance/

# activate the environment
module load cray-python
module load graphviz
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt


# generate plots
python generate_plots.py $data_root

# clean up
deactivate
rm -rf venv
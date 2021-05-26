#!/bin/bash -f

data_root=/project/s1053/performance/

# activate the environment
source /project/s1053/install/venv/vcm_1.0/bin/activate
pip install gprof2dot


# generate plots
python generate_plots.py $data_root
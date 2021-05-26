#!/bin/bash -f


# initialize directories
BASE_PATH="$(dirname "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )")"
DATA_ROOT=/project/s1053/performance/
DATA_DIR=${DATA_ROOT}/fv3core_performance
PROFILE_DIR=${DATA_ROOT}/fv3core_profile/gtcuda/prof

# activate the environment
source /project/s1053/install/venv/vcm_1.0/bin/activate
pip install gprof2dot


# generate plots
${BASE_PATH}/generate_plots.py ${data_dir}

# generate pictures from dot files
dot -Tpng profile.dot -o profile.png
dot -Tpdf profile.dot -o profile.pdf
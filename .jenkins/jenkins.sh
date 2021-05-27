#!/bin/bash -f

data_root=/project/s1053/performance/

# activate the environment
root_dir=`dirname $0`
cd ${root_dir}/external/daint_venv
./install.sh ${root_dir}/venv
source ${root_dir}/venv/bin/activate
# source /project/s1053/install/venv/vcm_1.0/bin/activate
pip install gprof2dot
cd $root_dir


# generate plots
python generate_plots.py $data_root

# clean up
deactivate
rm -rf venv
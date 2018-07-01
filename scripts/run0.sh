#!/bin/bash

placenta_dir=/data/vision/polina/projects/placenta_segmentation/
python_exe=/data/vision/polina/shared_software/anaconda3-4.3.1/envs/keras/bin/python

###################

cd ${placenta_dir}

args="CUDA_VISIBLE_DEVICES=0"
nohup ${args} ${python_exe} train.py "$@" > nohup0.out 2> nohup0.err < /dev/null &

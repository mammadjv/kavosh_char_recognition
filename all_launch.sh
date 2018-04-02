#!/bin/bash

export PYTHONPATH=/home/ubuntu/caffe/python:$PYTHONPATH
source /home/ubuntu/kavosh_char_recognition/devel/setup.bash
/home/ubuntu/kavosh_char_recognition/start_cycle.sh &
roslaunch bring_up sys_bring_up.launch

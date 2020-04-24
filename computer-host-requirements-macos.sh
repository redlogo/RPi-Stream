#!/bin/bash

# install python libs
pip install numpy
pip install pillow
pip install opencv-python
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-macosx_10_14_x86_64.whl
pip install imagezmq

# install edge tpu runtime lib
curl -O https://dl.google.com/coral/edgetpu_api/edgetpu_runtime_20200331.zip
unzip edgetpu_runtime_20200331.zip
cd edgetpu_runtime
sudo bash install.sh
#!/bin/bash

# install python libs
pip install curl
pip install numpy
pip install pillow
pip install opencv-python
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-macosx_10_14_x86_64.whl
pip install imagezmq

# install edge tpu runtime lib, you will be asked for password because of the sudo command, then choose tpu frequency wisely
curl -O https://dl.google.com/coral/edgetpu_api/edgetpu_runtime_20200331.zip
unzip edgetpu_runtime_20200331.zip
cd edgetpu_runtime
sudo bash install.sh
cd ..
rm -rf edgetpu_runtime*

# get pre-trained model and labels from coral website (coco image set)
mkdir -p models_edgetpu
curl -OL https://github.com/google-coral/edgetpu/raw/master/test_data/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite
mv mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite models_edgetpu/
mkdir -p labels_edgetpu
curl -OL https://github.com/google-coral/edgetpu/raw/master/test_data/coco_labels.txt
mv coco_labels.txt labels_edgetpu/
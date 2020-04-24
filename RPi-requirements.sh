#!/bin/bash

# recommend to execute these in virtualenv
# sudo pip3 install virtualenv
# python3 -m venv rpi-stream
# source rpi-stream/bin/activate

# you might need these for opencv, credit and acknowledgement to https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi
# sudo apt-get -y install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
# sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
# sudo apt-get -y install libxvidcore-dev libx264-dev
# sudo apt-get -y install qt4-dev-tools libatlas-base-dev

# install python libs, tried and found opencv4.x does not work for RPi
pip install numpy
pip install opencv-python==3.4.6.27
pip install imagezmq
pip install imutils
pip install picamera
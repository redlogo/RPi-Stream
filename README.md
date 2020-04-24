# Raspberry Pi Stream Object Detection
## Introduction
Live camera stream from Raspberry Pi to local host, do object detection with Coral EdgeTPU on host side.

<br>A FPS 35-45 can be achieved, depending on the network condition. 
<br>Can be used as an AI-powered surveillance camera application.
## Video Tutorial
* [A preview of this project](https://www.youtube.com/watch?v=PCdNH4zSNug)
* [![Foo](meta/preview.png)](https://www.youtube.com/watch?v=PCdNH4zSNug)
## Preparation and Environment
* Raspberry Pi, [latest RPi4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) is recommended.
* A camera for RPi, such as [RPi camera module V2](https://www.raspberrypi.org/products/camera-module-v2/)
* A local computer as host, [Ubuntu](https://ubuntu.com/) system is recommended.
* [Coral EdgeTPU](https://coral.ai/products/accelerator/), USB version is tested in this repo.
* Python virtual env is recommended for both RPi and computer host sides.
  * virtualenv (python3.7) is recommended for RPi.
  * [Anaconda / Conda](https://www.anaconda.com/) (python3.7) is recommended for computer host.
## Installation
Clone this repository on both RPi and computer host sides:
```
git clone https://github.com/redlogo/RPi-Stream.git
```
Install libs needed for Raspberry Pi:
```
bash RPi-requirements.sh
```
Install libs required for local computer host with the USB EdgeTPU unplugged:
```
# choose the correct one, depending on your computer system.
bash computer-hose-requirements-linux.sh
bash computer-host-requirements-macos.sh
bash computer-host-requirements-windows.sh
```
Plug USB EdgeTPU into the host usb 3.0 port.
## Usage
Edit on RPi side, change sender_stream.py:
```
# line 20, change it to your local computer host ip
target_ip = '192.168.7.33'  
```
Firstly execute script on RPi side:
```
python3 sender_stream.py
```
Secondly execute script on local computer host side:
```
python3 receiver_stream_object_detection.py
```
To exit streaming, firstly terminate (ctrl + c) RPi side, then computer host side.
## Coding Style
General Python 3 Coding style.
## Version
1.0 - April 2020.
## Author
redlogo
## References and Acknowledgements
* [Coral EdgeTPU](https://coral.ai/)
* [Python library of imagezmq](https://github.com/jeffbass/imagezmq)
* [A brilliant project by EdjeElectronics](https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi)
## License
MIT
## Copyright
Copyright © 2020 redlogo
# RPi Stream Object Detection
Live stream a camera from Raspberry Pi to local computer host, and do object detection with Coral EdgeTPU within the local host. A FPS 35-45 can be achieved, depending on the network condition. Can be used as an AI-powered surveillance camera application.
## Preparation
You will need:
* Raspberry Pi, [latest RPi4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) is recommended.
* A camera for RPi, such as [RPi camera module V2](https://www.raspberrypi.org/products/camera-module-v2/)
* A local computer as host, [Ubuntu](https://ubuntu.com/) system is recommended.
* [Coral EdgeTPU](https://coral.ai/products/accelerator/), USB version is tested in this repo.
## Installation
Clone this repository on both RPi and computer host sides:
```
git clone https://github.com/redlogo/RPi-Stream.git
```
Install libs needed for Raspberry Pi side:
```
sudo bash RPi-requirements.sh
```
Install libs required for local computer host side (Linux):
```
sudo bash computer-host-requirements.sh
```
## Usage
Firstly execute on RPi side:
```
python3 sender_stream.py
```
Secondly execute on local computer host side:
```
python3 receiver_stream_object_detection.py
```
To exit streaming, firstly terminate RPi side, then computer host side.
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
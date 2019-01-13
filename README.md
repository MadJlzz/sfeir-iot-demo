# sfeir-iot-demo

A simple project used for demonstrating GCP IoT Core capabilities using a RaspberryPi 3B+.

## Getting Started

If you want to use this project, simply clone like you would do usually:

`git clone git@github.com:MadJlzz/sfeir-iot-demo.git`

If you want to participate, please fork the project and clone you own copy instead of this one with:

`git clone git@github.com:<USERNAME>/sfeir-iot-demo.git`

## Prerequisites

In order to launch the project you will need several things to make everything work.

Here's what you'll need in matter of hardware components:

| Component       | Number |
| --------------- |:------:|
| Raspberry Pi 3  | 1      |
| Breadboard      | 1      |
| Resistors 230Ω  | 3      |
| Resistors 1kΩ   | 1      |
| RGB Led         | 1      |
| DHT11           | 1      |
| Jumpers         | ~10    |

It should cost you around 50€ but everything is reusable so it's still a good investment if you are interested in electronics.

All of the code used for the RaspberryPi is written using Python. It was tested with `Python 2.7`.

Please check you have `gpio` (>= 2.46) installed on your Pi. Normally it should already be installed.
```
pi@madpi:~/Documents/repositories/sfeir-iot-demo $ gpio -v
gpio version: 2.46
Copyright (c) 2012-2018 Gordon Henderson
This is free software with ABSOLUTELY NO WARRANTY.
For details type: gpio -warranty

Raspberry Pi Details:
  Type: Pi 3+, Revision: 03, Memory: 1024MB, Maker: Sony
  * Device tree is enabled.
  *--> Raspberry Pi 3 Model B Plus Rev 1.3
  * This Raspberry Pi supports user-level GPIO access.
```

This code need third party libraries too. Please follow the installation guide [here](https://pypi.org/project/Adafruit_Python_DHT/) and [here](https://pypi.org/project/paho-mqtt/)

You should be good to go now!

## Executing

Please ensure that you have configured correctly the Google Cloud Platform. Remember you have to replace some variables in `main.py` in order
to target your right GCP assets.

Lastly, to launch the program, you should run the `main.py` file like so:

```
python main.py
```

## Authors

* **Julien Klaer** - *Initial work* - [MadJlzz](https://github.com/MadJlzz)

See also the list of [contributors](https://github.com/MadJlzz/sfeir-iot-demo/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Google Cloud Platform Official documentation

## Disclaimer

The piece of code found here was not written with the idea of good maintability or good design. So please, do not use this in production or at you own risks.



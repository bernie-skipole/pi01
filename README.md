# README #

This project is intended to be a general purpose web service which will run on a Raspberry pi, and is a basis for future projects. It presents a web service displaying basic password authenticated output controls, and lists inputs.

The code is developed using the skipole web framework - see hhttp://skipole.bitbucket.io/

Note: Raspberry Pi is a trademark of the Raspberry Pi Foundation, this project, and the skipole web framework, is not associated with any Raspberry Pi products or services.

Initially the project is set with example inputs and outputs, and username 'admin' password 'password'.

You will need the python3 version of rpi.gpio

To check if you have it, try

sudo python3

and then

import RPi.GPIO as GPIO

If this is accepted without errors, you are ok, if not, exit from python with ctrl-D and then install it using:

sudo apt-get install python3-rpi.gpio




 

# Puzzle Vision

The Puzzle Vision project is a small Python module that integrates a web server with a serial-monitor to provide access 
to data coming from a Robot Controller attached via a Serial interface. Specifically, this code is meant to run on a
Raspberry Pi that is attached to a AStar32u4 Robot Controller HAT. 

This program will display the data that is sent by the AStar32u4, and allows commands to be sent to the Controller
from a web portal. Finally, it will eventually include the ability to view the images that are being taken by
the Controller for debuggin purposes.

The following still needs to be figured out:

1. Serve Templates instead of Raw HTML, so we can customize the response based on data requested.
2. If HomeController works as seperate class, move all controllers out of SerialServer.py
3. Should communication between devices happen over I2C or Serial? It is currently Serial.
4. Currently there is a Serial --> USB adapter that is connecting the AStar32u4 to the RPi. This needs to be changed to
use the RPi's built-in GPIO Serial pins.
5. The Serial Communication task should happen on a background thread, and data should be passed to the web server.

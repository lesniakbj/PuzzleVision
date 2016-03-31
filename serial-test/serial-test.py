#!/usr/bin/env python

import io
import serial
from sys import stdin

# Defaults
port = '/dev/ttyUSB0'
baud = 57600

ser = serial.Serial(
	port,
	baud,
	timeout = 1
)

print('Connected to ', ser.name)


while 1:
	data = ser.readline()
	print(data)
	
	out = stdin.readline()
	ser.write(bytes(out, 'UTF-8'))
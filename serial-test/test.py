 #!/usr/bin/env python
import io
import serial

serial_port = serial.Serial(
'/dev/ttyUSB0',
57600,
timeout = 1 )

data_list = []

while 1:
    data = ''

    if serial_port.inWaiting():
        data = serial_port.readline()

    if len(data) > 0:
        data_list.append(data)
        print('Data rec: ', data)
        
        serial_port.write(bytes("Test message", 'UTF-8'))
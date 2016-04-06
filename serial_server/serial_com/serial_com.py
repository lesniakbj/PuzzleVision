#!/usr/bin/env python
import io
import serial
import config
import multiprocessing

class SerialCom(multiprocessing.Process):
    data_list = []

    def __init__(self):
        multiprocessing.Process.__init__(self)    
        self.serial_port = serial.Serial(
            config.serial.PORT, 
            config.serial.BAUD, 
            timeout = 1
        )

        
    def close(self):
        self.serial_port.close()

        
    def checkForData(self):
        if self.serial_port.inWaiting():
            data = self.serial_port.readline()

            if len(data) > 0:
                self.data_list.append(data)
                print('Data received from device: {}' % data)
        
                return data

    def writeSerial(self, msg):
        self.serial_port.write(bytes(msg, 'UTF-8'))

    def run(self):
        self.serial_port.flushInput()
        
        while True:
            msg = self.checkForData()

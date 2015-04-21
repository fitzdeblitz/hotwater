__author__ = 'michael.lohan'
import os
import time


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0414609ea2ff/w1_slave'

class TempSensor:

    def __init__(self, name, deviceName):
        self.name = name
        self.deviceName = deviceName
        self.devicesAddress = '/sys/bus/w1/devices/' + deviceName + '/w1_slave'

    def tempRaw(self):
        f = open(self.devicesAddress, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def readTemp(self):

        lines = self.tempRaw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.tempRaw()

        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            return int(temp_c)

class SensorMgr:
    def __init__(self):
        self.gable = TempSensor('Gable Solar Panel','28-0414609ea2ff')
        self.tankLower =  TempSensor('Tank Lower','28-0414609ea2ff')
        self.backBoiler = TempSensor('Back Boiler','28-0414609ea2ff')
        self.tankUpper = TempSensor('Tank Upper','28-0414609ea2ff')

    def isGableHotterThanTank(self):
        return self.gable.readTemp() > self.tankLower.readTemp()

    def isBackBoilerHotterThanTank(self):
        return self.backBoiler.readTemp() > self.tankUpper.readTemp()
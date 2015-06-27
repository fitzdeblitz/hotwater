import os
import time
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0414609ea2ff/w1_slave'

temp_sensor_gable_or_roof = '/sys/bus/w1/devices/28-000005e4b7ba/w1_slave'
temp_sensor_gable_or_roof2 = '/sys/bus/w1/devices/28-000005e77594/w1_slave'

temp_sensor_tbottom = '/sys/bus/w1/devices/28-0414608267ff/w1_slave'
temp_sensor_ttop  = '/sys/bus/w1/devices/28-041460ba02ff/w1_slave'


class TempSensor:
    def __init__(self, name, device_name):
        self._name = name
        self._device_name = device_name
        self._devices_address = '/sys/bus/w1/devices/' + device_name + '/w1_slave'

    @property
    def name(self):
        return self._name

    def _tempRaw(self):
        f = open(self._devices_address, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def readTemp(self):
        lines = self._tempRaw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._tempRaw()

        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            return int(temp_c)

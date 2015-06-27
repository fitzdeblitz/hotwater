import os
import time
import RPi.GPIO as GPIO

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class TempSensor:
    def __init__(self, name, device_name):
        self._name = name
        self._device_name = device_name
        self._devices_address = '/sys/bus/w1/devices/' + device_name + '/w1_slave'

    @property
    def name(self):
        return self._name

    def read_temp(self):
        lines = self.read_raw_temp()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_raw_temp()

        temp_output = lines[1].find('t=')

        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0
            return int(temp_c)

    def read_raw_temp(self):
        f = open(self._devices_address, 'r')
        lines = f.readlines()
        f.close()
        return lines

import os
import time


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

temp_sensor = '/sys/bus/w1/devices/28-0414609ea2ff/w1_slave'

class TempSensor:

    def __init__(self, name, device_name):
        self._name = name
        self._device_name = device_name
        self._devices_address = '/sys/bus/w1/devices/' + device_name + '/w1_slave'

    def tempRaw(self):
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

class SensorMgr:
    def __init__(self):
        self._gable = TempSensor('Gable Solar Panel','28-0414609ea2ff')
        self._tank_lower =  TempSensor('Tank Lower','28-0414609ea2ff')
        self._back_boiler = TempSensor('Back Boiler','28-0414609ea2ff')
        self._tank_upper = TempSensor('Tank Upper','28-0414609ea2ff')

    def isGableHotterThanTank(self):
        return self._gable.readTemp() > self._tank_lower.readTemp()

    def isBackBoilerHotterThanTank(self):
        return self._back_boiler.readTemp() > self._tank_upper.readTemp()
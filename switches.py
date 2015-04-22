import os

import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(21, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class Switch:

    _state = False
    _override = False
    _override_state = False

    def __init__(self, name, pin_number):
        self._name = name
        self._pin_number = pin_number

    def turnOn(self):
        if self._state==False :
            self.updateGPIO()
            self._state = True

    def turnOff(self):
        if self._state :
            self.updateGPIO()
            self._state = False

    def overrideOn(self):
        if self._override==False :
            self.updateGPIO()
            self._override = True

    def overrideOff(self):
        if self._override :
            self.updateGPIO()
            self._override = False

    def overrideStateOn(self):
        if self._override_state==False :
            self.updateGPIO()
            self._override_state = True

        self._override_state = True

    def overrideStateOff(self):
        if self._override_state :
            self.updateGPIO()
            self._override_state = False



    def updateGPIO(self):
        if self._override:
            GPIO.output(self._pin_number,self._override_state)
        else:
            # todo add time check so the _switch does change to quickly
            GPIO.output(self._pin_number,self._state)


class SwitchMgr:

    def __init__(self):
        self._gable_pump__switch = Switch('Gable Pump', 21)
        self._back_boiler_pump__switch = Switch('Back Boiler Pump', 20)
        self._under_floor_heating_pump__switch = Switch('Under Floor Heating Pump', 19)
        self._immersion_shower_switch = Switch('Immersion Shower Heater', 18)
        self._immersion_bath_switch = Switch('Immersion Shower Heater', 17)

    def turnGablePumpOn(self):
        self._gable_pump__switch.turnOn()

    def turnGablePumpOff(self):
       self._gable_pump__switch.turnOff()

    def turnGablePumpAlwaysOn(self):
        self._gable_pump__switch.overrideOn()
        self._gable_pump__switch.overrideStateOn()

    def turnGablePumpAlwaysOff(self):
        self._gable_pump__switch.overrideOn()
        self._gable_pump__switch.overrideOff()

    def setGablePumpAutomatic(self):
        self._gable_pump__switch.overrideOff()
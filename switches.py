import os

import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(21, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


class Switch:

    state = False
    override = False
    overrideState = False

    def __init__(self, name, pinNumber):
        self.name = name
        self.pinNumber = pinNumber

    def turnOn(self):
        if self.state==False :
            self.updateGPIO()
            self.state = True

    def turnOff(self):
        if self.state :
            self.updateGPIO()
            self.state = False

    def overrideOn(self):
        if self.override==False :
            self.updateGPIO()
            self.override = True

    def overrideOff(self):
        if self.override :
            self.updateGPIO()
            self.override = False

    def overrideStateOn(self):
        if self.overrideState==False :
            self.updateGPIO()
            self.overrideState = True

        self.overrideState = True

    def overrideStateOff(self):
        if self.overrideState :
            self.updateGPIO()
            self.overrideState = False



    def updateGPIO(self):
        if self.override:
            GPIO.output(self.pinNumber,self.overrideState)
        else:
            # todo add time check so the switch does change to quickly
            GPIO.output(self.pinNumber,self.state)


class SwitchMgr:

    def __init__(self):
        self.gablePumpSwitch = Switch('Gable Pump', 21)
        self.backBoilerPumpSwitch = Switch('Back Boiler Pump', 20)
        self.underFloorHeatingPumpSwitch = Switch('Under Floor Heating Pump', 19)
        self.immersionShowerSwitch = Switch('Immersion Shower Heater', 18)
        self.immersionBathSwitch = Switch('Immersion Shower Heater', 17)

    def turnGablePumpOn(self):
        self.gablePumpSwitch.turnOn()

    def turnGablePumpOff(self):
       self.gablePumpSwitch.turnOff()

    def turnGablePumpAlwaysOn(self):
        self.gablePumpSwitch.overrideOn()
        self.gablePumpSwitch.overrideStateOn()

    def turnGablePumpAlwaysOff(self):
        self.gablePumpSwitch.overrideOn()
        self.gablePumpSwitch.overrideOff()

    def setGablePumpAutomatic(self):
        self.gablePumpSwitch.overrideOff()
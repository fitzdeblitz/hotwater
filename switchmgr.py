try:
    from rpi.switch import Switch
except ImportError:
    from simulator.switch import Switch


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
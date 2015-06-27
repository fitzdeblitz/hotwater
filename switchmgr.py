try:
    from rpi.switch import Switch
except ImportError:
    from simulator.switch import Switch


class SwitchMgr:
    def __init__(self):
        self._gable_pump_switch = Switch('Gable Pump', 21)
        self._back_boiler_pump_switch = Switch('Back Boiler Pump', 20)
        self._under_floor_heating_pump_switch = Switch('Under Floor Heating Pump', 19)
        self._immersion_shower_switch = Switch('Immersion Shower Heater', 18)
        self._immersion_bath_switch = Switch('Immersion Shower Heater', 17)

    def turn_gable_pump_on(self):
        self._gable_pump_switch.turn_on()

    def turn_gable_pump_off(self):
        self._gable_pump_switch.turn_off()

    def turn_gable_pump_always_on(self):
        self._gable_pump_switch.override_on()
        self._gable_pump_switch.override_state_on()

    def turn_gable_pump_always_off(self):
        self._gable_pump_switch.override_on()
        self._gable_pump_switch.override_off()

    def set_gable_pump_automatic(self):
        self._gable_pump_switch.override_off()



# simulator temperature sensor
class TempSensor:
    def __init__(self, name, device_name):
        self._name = name
        self._device_name = device_name

    @property
    def name(self):
        return self._name

    def read_temp(self):
        return 20


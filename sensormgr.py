try:
    from rpi.tempsensor import TempSensor
except ImportError:
    from simulator.tempsensor import TempSensor


class SensorMgr:
    def __init__(self):
        self._roof_green_house = TempSensor('Gable Solar Panel', '28-000005e4b7ba')
        self._gable = TempSensor('Roof Green House', '28-000005e77594')
        self._tank_lower = TempSensor('Tank Lower', '28-0414608267ff')
        self._tank_upper = TempSensor('Tank Upper', '28-041460ba02ff')
        self._back_boiler = TempSensor('Back Boiler', '28-0414609848ff')

        self._tempsensors = [
            self._roof_green_house,
            self._gable,
            self._tank_lower,
            self._tank_upper,
            self._back_boiler
        ]

    def is_gable_hotter_than_tank(self):
        return self._gable.read_temp() > self._tank_lower.read_temp()

    def is_back_boiler_hotter_than_tank(self):
        return self._back_boiler.read_temp() > self._tank_upper.read_temp()

    def get_tempsensors(self):
        result = []
        # for now read temp on request, but later will come from db
        for sensor in self._tempsensors:
            result.append({'name': sensor.name, 'value': sensor.read_temp()})
        return result
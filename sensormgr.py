try:
    from rpi.tempsensor import TempSensor
except ImportError:
    from simulator.tempsensor import TempSensor


class SensorMgr:
    def __init__(self):
        self._roofGreenHouse = TempSensor('Gable Solar Panel','28-000005e4b7ba')
        self._gable = TempSensor('Roof Green House','28-000005e77594')
        self._tank_lower = TempSensor('Tank Lower','28-0414608267ff')
        self._tank_upper = TempSensor('Tank Upper','28-041460ba02ff')
        self._back_boiler = TempSensor('Back Boiler','28-0414609848ff')

        self._temp_sensors = [
            self._roofGreenHouse,
            self._gable,
            self._tank_lower,
            self._tank_upper,
            self._back_boiler
        ]

    def isGableHotterThanTank(self):
        return self._gable.readTemp() > self._tank_lower.readTemp()

    def isBackBoilerHotterThanTank(self):
        return self._back_boiler.readTemp() > self._tank_upper.readTemp()

    def get_thermostats(self):
        thermostats = []
        # for now read temp on request, but later will come from db
        for sensor in self._temp_sensors:
            thermostats.append({'sensor': sensor.name, 'value': sensor.readTemp()})
        return thermostats
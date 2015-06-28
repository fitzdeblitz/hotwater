
import time
from threading import Thread


class ControllerThread(Thread):
    def __init__(self, sensormgr, switchmgr):
        Thread.__init__(self)
        self.sensormgr = sensormgr
        self.switchmgr = switchmgr

    def run(self):
        while True:
            if self.sensormgr.is_gable_hotter_than_tank():
                self.switchmgr.turn_gable_pump_on()
            else:
                self.switchmgr.turn_gable_pump_off()

            time.sleep(5)

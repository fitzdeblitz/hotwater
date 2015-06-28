

import time
from threading import Thread
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class ControllerThread(Thread):
    def __init__(self, sensormgr, switchmgr):
        Thread.__init__(self)
        self.sensormgr = sensormgr
        self.switchmgr = switchmgr

    def run(self):
        while True:
            if self.sensormgr.is_gable_hotter_than_tank():
                logging.debug('turning gable pump on')
                self.switchmgr.turn_gable_pump_on()
            else:
                logging.debug('turning gable pump off')
                self.switchmgr.turn_gable_pump_off()

            time.sleep(5)

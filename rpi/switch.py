import os
import RPi.GPIO as GPIO ## Import GPIO library
import logging

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(21, GPIO.OUT) ## Setup GPIO Pin 7 to OUT

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )


class Switch:
    _state = False
    _override = False
    _override_state = False

    def __init__(self, name, pin_number):
        self._name = name
        self._pin_number = pin_number

    def turn_on(self):
        if not self._state:
            logging.debug('turn on {0}'.format(self._name))
            self._state = True
            self._update_gpio()

    def turn_off(self):
        if self._state:
            logging.debug('turn off {0}'.format(self._name))
            self._state = False
            self._update_gpio()

    def override_on(self):
        if not self._override:
            logging.debug('override on {0}'.format(self._name))
            self._override = True
            self._update_gpio()

    def override_off(self):
        if self._override:
            logging.debug('override off {0}'.format(self._name))
            self._override = False
            self._update_gpio()

    def override_state_on(self):
        if not self._override_state:
            logging.debug('override state on {0}'.format(self._name))
            self._override_state = True
            self._update_gpio()

    def override_state_off(self):
        if self._override_state:
            logging.debug('override state off {0}'.format(self._name))
            self._override_state = False
            self._update_gpio()

    def _update_gpio(self):
        if self._override:
            GPIO.output(self._pin_number, self._override_state)
        else:
            # todo add time check so the _switch does change to quickly
            GPIO.output(self._pin_number, self._state)

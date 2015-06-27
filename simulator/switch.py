

# simulator switch
class Switch:
    _state = False
    _override = False
    _override_state = False

    def __init__(self, name, pin_number):
        self._name = name
        self._pin_number = pin_number

    def turnOn(self):
        if self._state==False :
            self._state = True

    def turnOff(self):
        if self._state :
            self._state = False

    def overrideOn(self):
        if self._override==False :
            self._override = True

    def overrideOff(self):
        if self._override :
            self._override = False

    def overrideStateOn(self):
        if self._override_state==False :
            self._override_state = True

        self._override_state = True

    def overrideStateOff(self):
        if self._override_state :
            self._override_state = False

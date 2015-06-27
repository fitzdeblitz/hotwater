

# simulator switch
class Switch:
    _state = False
    _override = False
    _override_state = False

    def __init__(self, name, pin_number):
        self._name = name
        self._pin_number = pin_number

    def turn_on(self):
        if not self._state:
            self._state = True

    def turn_off(self):
        if self._state:
            self._state = False

    def override_on(self):
        if not self._override:
            self._override = True

    def override_off(self):
        if self._override:
            self._override = False

    def override_state_on(self):
        if not self._override_state:
            self._override_state = True

    def override_state_off(self):
        if self._override_state:
            self._override_state = False

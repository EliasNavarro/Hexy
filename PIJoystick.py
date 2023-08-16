from inputs import get_gamepad
import threading
import time

class PIJoystick(object):
    MAX_JOY_VAL = 116

    def __init__(self):
        self.JoystickY = 0
        self.JoystickX = 0
        self.LeftButton = 0
        self.CenterButton = 0
        self.RightButton = 0
        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

    def read(self): # return the buttons/triggers that you care about in this method
        time.sleep(0.003)
        x = self.JoystickX
        y = self.JoystickY
        lb = self.LeftButton
        cb = self.CenterButton
        rb = self.RightButton
        return [x, y, lb, cb, rb]

    def _monitor_controller(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.JoystickY = (((event.state - 2) / PIJoystick.MAX_JOY_VAL) - 1) # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.JoystickX = (((event.state - 20) / PIJoystick.MAX_JOY_VAL) - 1)# / PIJoystick.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'BTN_TRIGGER':
                    self.LeftButton = event.state
                elif event.code == 'BTN_THUMB':
                    self.CenterButton = event.state
                elif event.code == 'BTN_THUMB2':
                    self.RightButton = event.state

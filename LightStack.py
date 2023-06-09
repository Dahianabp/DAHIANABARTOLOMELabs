from Lights import Light
import time


class lightStack:
    """
    This class represents a stack of lights used for a specific purpose,
    such as a traffic signal for a particular direction.
    """
    def __init__(self, green_pin, yellow_pin, red_pin):
        self._greenLight = Light(green_pin, "Green Light")
        self._yellowLight = Light(yellow_pin, "Yellow Light")
        self._redLight = Light(red_pin, "Red Light")
        
    def turnOnGreen(self):
        self._greenLight.on()
        self._yellowLight.off()
        self._redLight.off()

    def turnOnYellow(self):
        self._greenLight.off()
        self._yellowLight.on()
        self._redLight.off()

    def turnOnRed(self):
        self._greenLight.off()
        self._yellowLight.off()
        self._redLight.on()

    def turnOff(self):
        self._greenLight.off()
        self._yellowLight.off()
        self._redLight.off()

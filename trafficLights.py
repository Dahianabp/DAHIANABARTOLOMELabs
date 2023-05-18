from Lights import Light
from Displays import *
from Buzzer import *
from Button import *
import time

class TrafficLightController:
    def __init__(self):
        print("TrafficLightController: constructor")

        self._greenLight = Light(9, "Green Light")
        self._yellowLight = Light(5, "Yellow Light")
        self._redLight = Light(0, "Red Light")
        
        self._pedestrianCrossingButton = Button(17, "pedestrianCrossingButton", buttonhandler=self, lowActive=True)
        self._buzzer = ActiveBuzzer(13)

        self._pedestrianCrossingRequested = False

        self._display = LCDDisplay(sda = 20, scl = 21, i2cid = 0)


    def go(self):
        print("TrafficLightController: go")
        self._display.reset()
        self._display.showText("Dont Walk")
        self._redLight.off()
        self._greenLight.on()
        if self._pedestrianCrossingRequested == True:
            time.sleep(2)
        else:
            time.sleep(3)
        self._greenLight.off()


    def caution(self):
        print("TrafficLightController: caution")
        self._greenLight.off()
        self._yellowLight.on()
        time.sleep(1)
        self._yellowLight.off()

    def stop(self):
        print("TrafficLightController: stop")
        self._display.reset()
        self._display.showText("Walk")
        self._yellowLight.off()
        self._redLight.on()
        if self._pedestrianCrossingRequested == True:
            self._buzzer.beep(tone=50,duration=3000)
            self._pedestrianCrossingRequested = False
        else:    
            self._buzzer.beep(tone=50,duration=2000)
        self._redLight.off()
    
    def requestPedestrianCrossing(self):
        print("Crossing Requested...")
        self._pedestrianCrossingRequested = True
        self._display.reset()
        self._display.showText("Crossing Requested...")

    def buttonPressed(self, name):
        if name == "pedestrianCrossingButton":
            self.requestPedestrianCrossing()
    

    def buttonReleased(self, name):
        pass
    
    def start(self):
        while True:
            self.go()
            self.caution()
            self.stop()

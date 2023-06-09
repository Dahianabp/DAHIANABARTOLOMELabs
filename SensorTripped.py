from Sensors import *

class MotionSensor(DigitalSensor):

    def __init__(self, pin):
        super().__init__(28, lowactive=False)

    def motionDetected(self):
        return self.tripped()
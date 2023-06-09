"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal transitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from Lights import Light
from Displays import *
from SensorTripped import *
from Sensors import * 
from LightStack import *

class trafficLightController:
    def __init__(self):
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling

        self._button1 = Button(17, "CrossingRequestButton1", buttonhandler=None)
        self._button2 = Button(10, "CrossingRequestButton2", buttonhandler=None)
        self._timer = SoftwareTimer(None)
        self._carSensor = MotionSensor(28)
        self._trafficLight1 = lightStack(9, 5, 0) #represent a stack of lights found in a traffic light
        self._trafficLight2 = lightStack(14, 22, 13)
        self._pedestrianCrossing2 = LCDDisplay(sda=20, scl=21, i2cid=0)
        self._pedestrianCrossing1 = LCDDisplay(sda=18, scl=19, i2cid=1)

        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(4, self, debug=False)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        self._model.addButton(self._button2)
        # add other buttons (up to 2 more) if needed
        
        # Add any timer you have.
        self._model.addTimer(self._timer)
        
        # Now add all the transitions that are supported by my Model
        # obviously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        # Some examples:
        self._model.addTransition(0, BTN1_PRESS, 1)  # Transition from state 0 to state 1 on button1 press
        self._model.addTransition(2, BTN2_PRESS, 3)  # Transition from state 2 to state 3 on button2 press
        self._model.addTransition(0, TIMEOUT, 1)  # Transition from state 0 to state 1 on timeout
        self._model.addTransition(1, TIMEOUT, 2)  # Transition from state 1 to state 2 on timeout
        self._model.addTransition(2, TIMEOUT, 3)  # Transition from state 2 to state 3 on timeout
        self._model.addTransition(3, TIMEOUT, 0)  # Transition from state 3 to state 0 on timeout
    
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """
    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            print("TrafficLightController: State 0")
            self._trafficLight1.turnOnGreen()
            self._trafficLight2.turnOnRed()
            self._pedestrianCrossing1.showText("Don't Walk!")
            self._pedestrianCrossing2.reset()
            self._pedestrianCrossing2.showText("Walk!")
            
        elif state == 1:
            print("TrafficLightController: State 1")
            self._trafficLight1.turnOnYellow()
            self._trafficLight2.turnOnRed()
            self._pedestrianCrossing1.showText("Don't Walk!")
            self._pedestrianCrossing2.showText("Don't Walk!")
            
        elif state == 2:
            print("TrafficLightController: State 2")
            if self._carSensor.motionDetected(): 
                self._model.gotoState(3)
            else:   
                self._trafficLight1.turnOnRed()
                self._trafficLight2.turnOnGreen()
                self._pedestrianCrossing1.reset()
                self._pedestrianCrossing1.showText("Walk!")
                self._pedestrianCrossing2.showText("Don't Walk!")
           
            
        elif state == 3:
            print("TrafficLightController: State 3")
            self._trafficLight1.turnOnRed()
            self._trafficLight2.turnOnYellow()
            self._pedestrianCrossing1.showText("Don't Walk!")
            self._pedestrianCrossing2.showText("Don't Walk!")

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            print("TrafficLightController: Entering State 0")
            self._timer.start(5)
            
        elif state == 1:
            print("TrafficLightController: Entering State 1")
            self._timer.start(3)
            
        elif state == 2:
            print("TrafficLightController: Entering State 2")
            self._timer.start(5)


        elif state == 3:
            print("TrafficLightController: Entering State 3")
            self._timer.start(3)

    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just left
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """
    def stateLeft(self, state):
        pass
    


# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
#if __name__ == '__main__':
    # TrafficLightController().run()


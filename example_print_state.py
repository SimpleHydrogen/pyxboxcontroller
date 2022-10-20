"""
A simple test of pyxboxcontroller.
Press start button to exit!

- Dan Forbes Mid October 2022
"""
import time

from pyxboxcontroller import XboxController, XboxControllerState

# Connect to controller
controller = XboxController(id=0)

try:
    # Polling loop
    while True:
        
        # Get current state of controller
        state:XboxControllerState = controller.state
        print(state)
        
        # Check to exit loop
        if state.start:
            print(f"Start pressed, exciting loop! :)")
            break
        
        time.sleep(0.05)
        
except Exception as exc:
    print(f"Code failed because {exc}")
    raise exc
"""
A simple test of pyxboxcontroller.
Press start button to exit!

- Dan Forbes Mid October 2022
"""
import time

from pyxboxcontroller import XboxController, XboxControllerState

if __name__ == "__main__":
    # Connect to controller
    controller = XboxController(0)

    # Loop parameters
    REFRESH_INTERVAL:float = 0.1

    # Polling loop
    try:
        while True:
            
            # Get current state of controller
            state:XboxControllerState = controller.state
            print(state)
            
            # Check to exit loop
            if state.start:  # Press start button to exit 
                print(f"Start pressed, exciting loop! :)")
                break
            
            time.sleep(REFRESH_INTERVAL)
            
    except Exception as exc:
        print(f"Code failed because {exc}")
        raise exc
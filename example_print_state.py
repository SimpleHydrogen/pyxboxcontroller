"""
A simple test of pyxboxcontroller.
Press start button to exit!

- Dan Forbes Mid October 2022
"""
import time
from pyxboxcontroller import XboxController, XboxControllerState

# Loop parameters
REFRESH_INTERVAL:float = 0.1

if __name__ == "__main__":
    try:
        controller = XboxController(0)  # Connect to controller

        while True:            
            # Get current state of controller
            state:XboxControllerState = controller.state
            print(state)

            # Check to exit loop
            if state.start:  # Press start button to exit 
                print(f"Start pressed, exciting loop! :)")
                break

            time.sleep(REFRESH_INTERVAL)

    # Controller not connected    
    except ConnectionError as exc:
        raise ConnectionError("No Controller connected.") from exc

    # Something else went wrong
    except Exception as exc:
        raise exc
    
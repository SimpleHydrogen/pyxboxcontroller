"""
A simple test of pyxboxcontroller.
Simple loop which prints the state of a connected XInput controller.
Press start button to exit!

- Dan Forbes 2022
"""
import time

from pyxboxcontroller import XboxController, XboxControllerState

# Loop parameters
REFRESH_INTERVAL:float = 0.1


def example_print_state():

    # Connect to controller
    controller = XboxController(0)

    while True:

        # Get current state of controller
        state: XboxControllerState = controller.state
        print(state)

        # Check to exit loop
        if state.start:  # Press start button to exit
            print("Start pressed, exciting loop! :)")
            break

        # Sleep before reading the state again
        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    try:
        example_print_state()

    # Controller not connected
    except ConnectionError as exc:
        raise ConnectionError("No Controller connected.") from exc

    # Something else went wrong
    except Exception as exc:
        raise exc

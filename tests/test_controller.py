import os, sys
sys.path.append(os.path.dirname(__name__))

def test_default_state() -> None:
    """Test creation of default controller state"""
    from pyxboxcontroller.controller import XboxControllerState

    default_state = XboxControllerState.default_state()

    print(default_state)

    assert isinstance(default_state , XboxControllerState)

    assert isinstance(XboxControllerState.buttons, dict)

def test_XboxController() -> None:
    from pyxboxcontroller import XboxController, XboxControllerState

    controller = XboxController(0)

    state = controller.state

    assert isinstance(state , XboxControllerState)
    print(state)


if __name__ == "__main__":
    test_default_state()
    test_XboxController()
    
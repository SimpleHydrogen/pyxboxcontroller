import os, sys
sys.path.append(os.path.dirname(__name__))


def test_default_state() -> None:
    """Test creation of default controller state"""
    from pyxboxcontroller.controller import XboxControllerState

    default_state = XboxControllerState.default_state()

    print(default_state)

    assert isinstance(default_state, XboxControllerState)

    assert isinstance(XboxControllerState.buttons, dict)


def test_XboxController() -> None:
    from pyxboxcontroller import XboxController, XboxControllerState

    controller = XboxController(0)

    state = controller.state

    assert isinstance(state, XboxControllerState)
    print(state)

    state.a
    state.b
    state.x
    state.y
    state.lb
    state.rb
    state.l_thumb_x
    state.l_thumb_y
    state.r_trigger
    state.l_trigger
    state.dpad_up
    state.dpad_down
    state.dpad_left
    state.dpad_right
    state.l3
    state.r3
    state.packet_number
    state.select
    state.start


def test_XboxBatteryInfo():
    # Connect to conttoller
    from pyxboxcontroller import XboxController, XboxBatteryInfo

    controller = XboxController(0)

    battery_info = controller.battery_info

    assert isinstance(battery_info, XboxBatteryInfo)

    battery_info.level
    battery_info.battery_type

    print(battery_info)

    print(controller.battery_level)


if __name__ == "__main__":
    test_default_state()
    test_XboxController()
    test_XboxBatteryInfo()

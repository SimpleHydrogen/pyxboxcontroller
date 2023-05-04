"""
Minimal way to get the current state of a connected XInput device (e.g. Xbox controller).
Wraps Windows' XInput library to communicate with controllers.
http://msdn.microsoft.com/en-gb/library/windows/desktop/ee417001%28v=vs.85%29.aspx

- Dan Forbes - Mid October 2022
"""
from functools import cache
from enum import IntEnum

from pyxboxcontroller import XInput


class XboxControllerState:
    """
    Parses an XInputState Struct into a sensible representation.\n

    Some examples of accessing the states' values:  \n
    >>> left_thumbstick_x = state.l_thumb_x
    >>> right_thumbstick_y = state.r_thumb_y
    >>> x_pressed:bool = state.x
    >>> lb_pressed:bool = state.lb  \n

    Alternately buttons (e.g. "a") can be gotten with:  \n
    >>> a_pressed:bool = state.buttons["a"]

    Check the packet number with:
    >>> state.packet_number
    """

    # Button map represents the bitmasks for accessing each button encoded in gamepad.buttons.
    # See https://learn.microsoft.com/en-us/windows/win32/api/xinput/ns-xinput-xinput_gamepad
    _BUTTON_MAP: dict[str, int] = {
        "dpad_up": 1,
        "dpad_down": 2,
        "dpad_left": 4,
        "dpad_right": 8,
        "start": 16,
        "select": 32,
        "l3": 64,
        "r3": 128,
        "lb": 256,
        "rb": 512,
        "a": 4096,
        "b": 8192,
        "x": 16384,
        "y": 32768,
    }

    def __init__(self, state: XInput.XINPUT_STATE):
        # Get gamepad struct from XInput state
        self.packet_number: int = state.packet_number
        gamepad: XInput.XINPUT_GAMEPAD = state.gamepad

        # # NOTE FOR DEBUG
        # if buttons not in self.BUTTON_MAP.values():
        #     print(f"Unknown button or combination: {buttons}")

        # Get states of each button
        self.buttons: dict[str, bool] = {
            btn : self._get_button_state(btn, gamepad.buttons)
            for btn in self._BUTTON_MAP}

        # Thumbsticks
        # TODO add deadzone checking
        # round to 4 decimal places
        # rounding ignores the error with converting signed 32-bit int to float
        # (-32768 to 32767) to (-1.0 to 1.0)
        self.l_thumb_x: float = round(gamepad.l_thumb_x / 32767., 4)
        self.l_thumb_y: float = round(gamepad.l_thumb_y / 32767., 4)
        self.r_thumb_x: float = round(gamepad.r_thumb_x / 32767., 4)
        self.r_thumb_y: float = round(gamepad.r_thumb_y / 32767., 4)

        # Triggers
        self.l_trigger: float = round(gamepad.left_trigger / 255., 4)
        self.r_trigger: float = round(gamepad.right_trigger / 255., 4)

    @classmethod
    def default_state(cls):
        """Returns a default state of XboxControllerState"""
        class XInputSpoofState:
            """Spoof an XInput state packet"""
            packet_number: int = -1
            class gamepad:
                buttons: int = 0
                l_thumb: float = 0.
                l_thumb_x: float = 0.
                l_thumb_y: float = 0.
                r_thumb: float = 0.
                r_thumb_x: float = 0.
                r_thumb_y: float = 0.
                left_trigger: float = 0.
                right_trigger: float = 0.
        return cls(XInputSpoofState())

    def __repr__(self) -> str:
        return f"""
    Packet number:{self.packet_number},
    Buttons:{self.buttons},
    Left thumbstick: {(self.l_thumb_x, self.l_thumb_y)},
    Right thumbstick: {(self.r_thumb_x, self.r_thumb_y)},
    Left trigger: {self.l_trigger}, 
    Right trigger: {self.r_trigger}
    """

    def _get_button_state(self, button: str, buttons: int) -> bool:
        """Returns True or False if the given button was pressed.
        bitwise and (&) of the bitmask and gamepad.buttons number"""
        mask: int = self._BUTTON_MAP[button]
        pressed: bool = (mask & buttons) != 0
        return pressed

    # Thumbstick getter
    @property
    def l_thumb(self) -> tuple[float, float]:
        """Returns the state of (X,Y) for the left thumbstick"""
        return (self.l_thumb_x, self.l_thumb_y)
    @property
    def r_thumb(self) -> tuple[float, float]:
        """Returns the state of (X,Y) for the right thumbstick"""
        return (self.r_thumb_x, self.r_thumb_y)

    @property
    def triggers(self) -> tuple[float, float]:
        """Returns the position of triggers (L,R)"""
        return (self.l_trigger, self.r_trigger)

    # Individual button getters
    @property
    def a(self) -> bool:
        return self.buttons["a"]
    @property
    def b(self) -> bool:
        return self.buttons["b"]
    @property
    def x(self) -> bool:
        return self.buttons["x"]
    @property
    def y(self) -> bool:
        return self.buttons["y"]
    @property
    def lb(self) -> bool:
        return self.buttons["lb"]
    @property
    def rb(self) -> bool:
        return self.buttons["rb"]
    @property
    def start(self) -> bool:
        return self.buttons["start"]
    @property
    def select(self) -> bool:
        return self.buttons["select"]
    @property
    def dpad_up(self) -> bool:
        return self.buttons["dpad_up"]
    @property
    def dpad_down(self) -> bool:
        return self.buttons["dpad_down"]
    @property
    def dpad_right(self) -> bool:
        return self.buttons["dpad_right"]
    @property
    def dpad_left(self) -> bool:
        return self.buttons["dpad_left"]
    @property
    def l3(self) -> bool:
        return self.buttons["l3"]
    @property
    def r3(self) -> bool:
        return self.buttons["r3"]

    @classmethod
    @property
    @cache
    # Default buttons dict
    def buttons(cls) -> dict[str, bool]:
        """dict containing current state of buttons"""
        return {btn:False for btn in cls._BUTTON_MAP}


class BatteryLevel(IntEnum):
    """Different battery levels.\n
    EMPTY = 0, LOW = 1, MEDIUM = 2, FULL = 3"""
    EMPTY = 0
    LOW = 1
    MEDIUM = 2
    FULL = 3

    def __str__(self) -> str:
        return self.name

class BatteryType(IntEnum):
    """Different battery types"""
    DISCONNECTED = 0
    WIRED = 1
    ALKALINE = 2
    NIMH = 3  # nickel metal hydride
    UNKNOWN = 255


class XboxBatteryInfo:
    """
    Parses an XInputBatteryInformation Struct into a sensible representation.\n

    Access the battery type with:  \n
    >>> battery_type: BatteryType = battery_info.battery_type

    Check the charge level like:  \n
    >>> level: BatteryLevel = battery_info.battery_level
    """

    def __init__(self, battery_info: XInput.XINPUT_BATTERY_INFORMATION) -> None:
        self.battery_type: BatteryType = BatteryType(battery_info.battery_type)
        self.level: BatteryLevel = BatteryLevel(battery_info.battery_level)

    @classmethod
    def default_state(cls):
        """Returns a default state of XboxBatteryInfo"""
        class XInputSpoofBatteryInfo:
            """Spoof an XInput battery info packet"""
            battery_type = BatteryType.DISCONNECTED
            battery_level = BatteryLevel.EMPTY
        return cls(XInputSpoofBatteryInfo())

    def __repr__(self) -> str:
        return f"""
    Battery level: {self.level.name},
    Battery type: {self.battery_type.name}
    """


class XboxController:
    """
    Provides access to the current state of a connected xbox controller.\n

    Connect to a controller with:
    >>> my_controller = XboxController(id)
    Try id=0 to connect to the 1st controller connected\n

    The state of the controller is given by:
    >>> state: XboxControllerState = my_controller.state

    The state of a button (e.g. "x") for that given state can be gotten with:
    >>> x_pressed: bool = state.x

    You can get the charge level of the battery with:
    >>> level: BatteryLevel = my_controller.battery_level

    BatteryLevel can be used as an int with values between 0-3,
    with 0 representing empty, and 3 representing full.

    In practice, you can check if the battery is low with:
    >>> if my_controller.battery_level < BatteryLevel.MEDIUM:
            ...

    The complete battery information can be gotten with:
    >>> battery_info: XboxBatteryInfo = my_controller.battery_info

    Raises a RuntimeError when communication with controller fails.
    """

    # TODO
    # Deadzones
    # Rumble

    # Specifies this is a controller for getting battery info
    _battery_device_type: int = 0

    def __init__(self, controller_id: int):
        self.id = controller_id
        self._state = XInput.XINPUT_STATE()
        self._battery_info = XInput.XINPUT_BATTERY_INFORMATION()
        self._last_packet_number: int = -1
        self._last_state: XboxControllerState = XboxControllerState.default_state()

    @property
    def state(self) -> XboxControllerState:
        """Get the current state of the controller"""

        # Get controller state from XInput
        res = XInput.GetState(self.id, self._state)

        # Handle response from XInput
        self.handle_response_code(res, current_action="get state")

        # Get current packet number
        packet_number: int = self._state.packet_number

        # No packets from controller since last call
        if packet_number == self._last_packet_number:
            return self._last_state

        # Convert XInput state struct into sensible response
        new_state = XboxControllerState(self._state)

        # Recall latest packet
        self._last_packet_number, self._last_state = packet_number, new_state

        return new_state

    @property
    def battery_info(self) -> XboxBatteryInfo:
        """Get the battery information of the controller"""
        response = XInput.GetBatteryInformation(
            self.id,
            self._battery_device_type,
            self._battery_info)

        # Handle response from XInput
        self.handle_response_code(response, "get battery info")

        # Convert the XInput struct into a sensible response
        battery_info = XboxBatteryInfo(self._battery_info)

        return battery_info

    @property
    def battery_level(self) -> BatteryLevel:
        """Get the current charge level of the battery.
        BatteryLevel can be used as an int, with values between 0 and 3,
        representing empty and full respectively."""
        return self.battery_info.level

    def handle_response_code(
            self,
            xinput_response_code: XInput.Codes,
            current_action: str
            ) -> None:
        """Check the XInput response code,
        raises the appropriate error if the function didn't succeed"""
        match xinput_response_code:

            case XInput.Codes.SUCCESS:
                pass

            case XInput.Codes.NOT_CONNECTED:
                exc = ConnectionError(
                    (f"No controller connected with id: {self.id},"
                     f"last packet id: {self._last_packet_number}"))
                raise exc

            case _ as exc:
                raise RuntimeError(
                    (f"Unknown error {xinput_response_code}"
                     f"attempting to {current_action} of device {self.id}"),
                    exc)

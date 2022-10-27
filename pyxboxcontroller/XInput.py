"""
C_Structs and other objects for communicating with XInput DLL.

- Dan Forbes - Mid October 2022
"""
import ctypes

# Get link to XInput library
XINPUT_DLL = ctypes.windll.xinput1_4

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('buttons', ctypes.c_ushort),
        ('left_trigger', ctypes.c_ubyte),
        ('right_trigger', ctypes.c_ubyte),
        ('l_thumb_x', ctypes.c_short),
        ('l_thumb_y', ctypes.c_short),
        ('r_thumb_x', ctypes.c_short),
        ('r_thumb_y', ctypes.c_short),
        ]
    
class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('packet_number', ctypes.c_ulong),
        ('gamepad', XINPUT_GAMEPAD),
    ]

class Codes:
        NOT_CONNECTED = 1167
        SUCCESS = 0
        
def GetState(id:int, state:XINPUT_STATE) -> Codes:
    return XINPUT_DLL.XInputGetState(id, ctypes.byref(state))

# class XINPUT_VIBRATION(ctypes.Structure):
#     _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
#                 ("wRightMotorSpeed", ctypes.c_ushort)]

# class XINPUT_BATTERY_INFORMATION(ctypes.Structure):
#     _fields_ = [("BatteryType", ctypes.c_ubyte),
#                 ("BatteryLevel", ctypes.c_ubyte)]
    
# pyxboxcontroller
This module allows for accessing the current state of a connected Xbox controller via the [XInput library](https://learn.microsoft.com/en-gb/windows/win32/xinput/getting-started-with-xinput?redirectedfrom=MSDN#getting-controller-state) on Windows.

## Installation
Simply install using pip
`pip install pyxboxcontroller`

## Connect to controller
Connect to the controller with id (starting at 0) using:
`controller = XboxController(id)`
## Getting the current state of the controller
The current state of the controller can be gotten with:
`state:XboxControllerState = controller.state`
This returns an `XboxControllerState` object.


Some examples of accessing the states' values:
```
left_thumbstick_x:float = state.l_thumb_x
right_thumbstick_y:float = state.r_thumb_y
x_pressed:bool = state.x
lb_pressed:bool = state.lb
```

Alternately the state of the button e.g. x can be gotten with:
` button_pressed:bool = state.buttons["x"]`
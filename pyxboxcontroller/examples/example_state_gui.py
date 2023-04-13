"""
A simple GUI displaying the current state of a connected Xinput device, such as an Xbox Controller.
Press start button to exit!

- Dan Forbes 2022
"""
import tkinter as tk
from tkinter.messagebox import showerror
from tkinter import ttk

from pyxboxcontroller import XboxController, XboxControllerState


def example_state_gui():

    # Connect to controller
    controller = XboxController(0)

    # Create GUI
    gui = DisplayState(controller)
    gui.run()


class DisplayState(tk.Frame):
    """ Displays the current state of the given xbox controller. Press start to close"""

    def __init__(self,
            xbox_controller: XboxController,
            root: tk.Tk | None = None
            ):
        tk.Frame.__init__(self, root, padx=30, pady=15)

        # Window properties
        self.master.title("pyxboxcontroller")
        self.master.resizable(False, False)
        self.grid()

        self.controller = xbox_controller
        self.last_state = XboxControllerState.default_state()

        # Check if controller is connected
        try:
            self.state = self.controller.state
        except ConnectionError as exc:
                showerror("Not connected", f"No controller connected with id: {self.controller.id}")
                raise exc 

        self.create_widgets()

        # Bind ESC key to close function
        self.master.bind('<Escape>', lambda _: self.close())

        # Setup Controller Polling
        self.interval_ms = 15
        self.after(self.interval_ms, self.update_state)

    def run(self) -> None:
        """Run the gui."""
        self.master.mainloop()

    def update_state(self):
        """Updates the gui's with new state information"""
        self.last_state: XboxControllerState = self.controller.state

        # Packet number
        self.packet_number_label.configure(
            text=f"Packet Number : {self.last_state.packet_number}")

        # Buttons
        for label, (btn, pressed) in zip(self.button_labels, self.last_state.buttons.items()):
            label.configure(text=f"{btn} : {pressed}")

        # Thumbsticks
        self.l_thumbstick.configure(text=f"l_thumb : {self.last_state.l_thumb}")
        self.r_thumbstick.configure(text=f"r_thumb : {self.last_state.r_thumb}")

        # Triggers
        l_label, r_label = self.triggers
        l_label.configure(text=f"l_trigger : {self.last_state.l_trigger}")
        r_label.configure(text=f"r_trigger : {self.last_state.r_trigger}")

        # Check if the closing condition is met
        self.check_close()

        # Update GUI
        self.after(self.interval_ms, self.update_state)

    def check_close(self):
        """Close the app if start is pressed."""
        if self.last_state.start:
            self.close()

    def create_widgets(self):
        """Draws the GUI"""
        row, column = 1, 1

        # GUI Info
        tk.Label(self,
                text="Press the start button or the Esc key to exit!",
                font='Helvetica 16 bold'
                ).grid(column=column, row=row)
        row += 1

        # Packet number
        self.packet_number_label = ttk.Label(self, text="Packet Number: -1")
        self.packet_number_label.grid(column=column, row=row)
        row += 1

        # Triggers
        self.triggers = (ttk.Label(self), ttk.Label(self))
        for trig in self.triggers:
            trig.grid(column=column, row=row)
            row += 1

        # Thumbsticks
        self.l_thumbstick, self.r_thumbstick = ttk.Label(self), ttk.Label(self)
        self.l_thumbstick.grid(row=row, column=column)
        row += 1
        self.r_thumbstick.grid(row=row, column=column)
        row += 1

        # Labels for buttons
        self.button_labels = [
            ttk.Label(self, text=f"{button} : {pressed}")
            for button, pressed in XboxControllerState.buttons.items()]
        
        for btn in self.button_labels:
            btn.grid(row=row, column=column)
            row += 1

        # Exit Button
        ttk.Button(self, text="Exit", command=self.close).grid(row=row, column=column)

    def close(self):
        """Close the GUI."""
        self.quit()


if __name__ == "__main__":

    # Run the GUI if this script is called directly
    try:
        example_state_gui()

    # Controller not connected
    except ConnectionError as exc:
        print(exc)

    # Something else went wrong
    except Exception as exc:
        raise exc

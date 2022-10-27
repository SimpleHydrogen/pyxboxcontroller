"""
A simple test of pyxboxcontroller.
Press start button to exit!

- Dan Forbes Mid October 2022
"""

import tkinter as tk
import tkinter.ttk as ttk

from pyxboxcontroller import XboxController, XboxControllerState

class DisplayState(ttk.Frame):
    """ Displays the current state of the given xbox controller. Press start to close"""
    def __init__(self, controller:XboxController, root: tk.Tk | None = None):
        tk.Frame.__init__(self, root, padx=30, pady=15)
        # self.master.geometry("260x420")
        self.master.title("pyxboxcontroller")
        self.master.resizable(False, False)
        self.grid()
        
        self.controller = controller
        self.last_state = XboxControllerState.default_state()
        
        self.create_widgets()
        
        self.master.bind('<Escape>', lambda _: self.close())
        
        self.INTERVAL_MS = 15
        self.after(self.INTERVAL_MS, self.update_state)

    def run(self) -> None:
        """Run the gui."""
        self.master.mainloop()
        
    def update_state(self):
            self.last_state:XboxControllerState = self.controller.state
            
            # Packet number
            self.packet_number_label.configure(text=f"Packet Number : {self.last_state.packet_number}")
            
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
            
            self.check_close()
            
            self.after(self.INTERVAL_MS, self.update_state)
            
    def check_close(self):
        """Close the app if start is pressed."""
        if self.last_state.start:
            self.close()
    
    def create_widgets(self):
        """Draws the GUI"""
        r, c = 1, 1
        
        tk.Label(self, 
                 text="Press the start button or the Esc key to exit!", font='Helvetica 16 bold').grid(column=c, row=r)
        r += 1
        
        # Packet number
        self.packet_number_label = ttk.Label(self, text="Packet Number: -1")
        self.packet_number_label.grid(column=c, row=r)
        # c += 1
        r += 1
        
        # Triggers
        self.triggers = (ttk.Label(self), ttk.Label(self))
        for trig in self.triggers:
            trig.grid(column=c, row=r)
            r += 1
        
        self.l_thumbstick, self.r_thumbstick = ttk.Label(self), ttk.Label(self)
        self.l_thumbstick.grid(row=r, column=c)
        r += 1
        self.r_thumbstick.grid(row=r, column=c)
        r += 1
        
        # c += 1
        
        # Labels for buttons 
        self.button_labels = [ttk.Label(self, text=f"{button} : {pressed}") 
                               for button, pressed in XboxControllerState.buttons.items()]
        for btn in self.button_labels: 
            btn.grid(row=r, column=c)
            r += 1
        # c += 1
        
        # Exit Button
        ttk.Button(self, text="Exit", command=self.close).grid(row=r, column=c)
        
    def close(self):
        self.quit()

if __name__ == "__main__":
    try:
        controller = XboxController(0)  # Connect to controller
    
        gui = DisplayState(controller)
        gui.run()
    
    # Controller not connected    
    except ConnectionError as exc:
        print(exc)
        
    # Something else went wrong
    except Exception as exc:
        raise exc
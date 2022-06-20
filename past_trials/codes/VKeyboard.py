# VKeyboard.py
import tkinter as tk


class VKeyboard(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        # Don't show the 'Toplevel' at instantiation
        super().withdraw()

        self.create()

        # Process all application == parent events
        parent.bind_all('<FocusIn>', self.on_event, add='+')
        parent.bind_all('<Button-1>', self.on_event, add='+')

    def on_event(self, event):
        w = event.widget

        # Don't process the own Button
        if w.master is not self:
            w_class_name = w.winfo_class()

            if w_class_name in ('Entry',):
                if self.state() == 'withdrawn':
                    self.deiconify()

                self.entry = w

            elif w_class_name in ('Button',):
                super().withdraw()
                w.focus_force()

    def create(self):
        # define the virtual keyboard `tk.Button`
        pass
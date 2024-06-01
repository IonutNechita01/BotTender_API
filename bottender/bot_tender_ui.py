import tkinter as tk
from threading import Thread
from time import sleep

class BotTenderUI(tk.Tk):
    def __init__(self, bot_tender):
        super().__init__()
        self.bot_tender = bot_tender
        self.title("BotTender UI")
        
        self.status_label = tk.Label(self, text="", font=("Helvetica", 24))
        self.status_label.pack(expand=True)

        self.fullscreen()
        self.update_status()
        
        # Periodically check the status
        self.check_status()

    def fullscreen(self):
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", self.exit_fullscreen)

    def exit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)
        self.destroy()

    def update_status(self):
        status = self.bot_tender.getStatus()["status"]
        if status == "BUSY":
            self.status_label.config(text="Loading...")
        else:
            self.status_label.config(text="")

    def check_status(self):
        self.update_status()
        self.after(500, self.check_status) 
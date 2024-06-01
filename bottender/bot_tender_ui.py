import tkinter as tk
from threading import Thread
from time import sleep

class BotTenderUI(tk.Tk):
    def __init__(self, bot_tender):
        super().__init__()
        self.bot_tender = bot_tender

        self.fullscreen()
        self.update_status()
        
        # Periodically check the status
        self.check_status()

    def fullscreen(self):
        self.attributes('-fullscreen', True)

    def update_status(self):
        status = self.bot_tender.getStatus()["status"]
        # show a loading screen when status == "BUSY"
        if status == "BUSY":
            self.loading_screen()
        else:
            self.main_screen()

    def loading_screen(self):
        self.clear_screen()
        label = tk.Label(self, text="Loading...", font=("Arial", 24))
        label.pack(expand=True)

    def main_screen(self):
        self.clear_screen()
        label = tk.Label(self, text="BotTender", font=("Arial", 24))
        label.pack(expand=True)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()    

    def check_status(self):
        self.update_status()
        self.after(500, self.check_status) 
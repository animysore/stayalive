import time
import threading
import tkinter as tk
from tkinter import ttk
import keyboard
import os

PATH = os.path.dirname(os.path.abspath(__file__))

STATUS = [
    'Click Start to StayAlive',
    'Just StayinAlive...'
]

def stayalive(event, interval = 2):
    while event.is_set():
        keyboard.press_and_release('up')
        print('keypress')
        time.sleep(interval)  
    
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.stopped = True
        self.create_widgets()
        self.stayalive_thread = None
        self.event = threading.Event()

    def create_widgets(self):
        self.character = tk.Label(self, text="Interval (seconds)")
        self.interval = tk.Entry(self)
        self.interval.insert(0, 5)
        self.start = tk.Button(self, command=self.toggle_start)
        self.status = tk.Label(self)

        self.refresh_button()
        self.character.pack(side="left")
        self.interval.pack(side="left")
        self.start.pack(side="top")
        self.status.pack(side="bottom")

    def refresh_button(self):
        if self.stopped:
            self.start['text'] = 'Start'
            self.start['fg'] = 'green'
            self.status['text'] = STATUS[0]
        else:
            self.start['text'] = 'Stop'
            self.start['fg'] = 'red'
            self.status['text'] = STATUS[1]


    def toggle_start(self):
        if self.stopped:
            interval = self.interval.get()
            self.stayalive_thread = threading.Thread(target=stayalive, args=(self.event, int(interval)))
            self.event.set()
            self.stayalive_thread.start()
            self.stopped = False
            self.refresh_button()
            
        else:
            self.event.clear()
            self.stayalive_thread.join()
            self.stopped = True
            self.refresh_button()
    
if __name__ == '__main__':
    root = tk.Tk()
    root.title('StayAlive')
    root.iconphoto(False, tk.PhotoImage(file='{}/stayalive.png'.format(PATH)))
    app = Application(master=root)
    app.mainloop()
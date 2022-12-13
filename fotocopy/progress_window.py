# progress window for fotoco.py
import tkinter as tk
from tkinter import ttk
import sys

    
class progress_window():

    _progress = 0 # 0..100
    __MAX_PROGRESS = 100
    
    def __init__(self):
        self._show_progress()

    def stop_now(self):
        self.root.destroy()        
        
        
        
    def _show_progress(self,title="fotoco.py progress"):
        self.root = tk.Tk()
        self.root.grid()
        self.root.title(title)
        self.root.resizable(width=False, height=False)
        self.root.columnconfigure(0,minsize=150,weight=1)
        self.root.rowconfigure(0,minsize=30,weight=1)
        self.root.rowconfigure(1,minsize=30,weight=1)
        self.root.rowconfigure(2,minsize=30,weight=1)        


        self.lbl_status = tk.Label(master=self.root, text="Status")
        self.lbl_status.grid(row=0, column=0, padx=5, pady=5, sticky="we")
        self._progressbar = tk.ttk.Progressbar(master=self.root,
                                           orient="horizontal",
                                           mode="determinate",
                                           maximum=self.__MAX_PROGRESS)
        self._progressbar.grid(row=1,column=0)
        
        self.btn_stop = ttk.Button(master=self.root,
                                   text="STOP",
                                   command=self.stop_now)
        self.btn_stop.grid(row=2, column=0)
       
        self.root.update()
        return self.root

    def nudge(self):
        self._progress = self._progress + 1
        self._progressbar.step(1)
        self._progressbar.update()

    def reset_progress(self):
        self._progress = 0
        self._progressbar["value"] = 0
        self._progressbar.update()
        self.btn_stop.configure(text="STOP")
        self.btn_stop.update()

    def set_progress( self, val ):
        self._progress = val
        self._progressbar["value"] = val
        self._progressbar.update()

    def finish(self):        
        self.set_progress(self.__MAX_PROGRESS)
        self.lbl_status.configure(text="Done, finished!")
        self.btn_stop.configure(text="Close")
        self.btn_stop.configure(command=self.stop_now)

    def set_status(self, stat):
        self.lbl_status.configure(text=stat)
        self.lbl_status.update()

# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer pygame surtout pour jouer les chasons, rien d'autre
import pygame
from pygame import mixer
# Importer json pour pouvoir ouvrir des fichiers jsons
import json
# Importer subprocess pour pouvoir faire un appel a une nouvelle application de python
import subprocess
from PIL import Image, ImageTk

class SplashScreen(Frame):
    def __init__(self, master=None, width=0.8, height=0.6, useFactor=True):
        Frame.__init__(self, master)
        self.pack(side=TOP, fill=BOTH, expand=YES)

        # get screen width and height
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = (useFactor and ws*width) or width
        h = (useFactor and ws*height) or height
        # calculate position x, y
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        self.master.overrideredirect(True)
        self.lift()

if __name__ == '__main__':
    root = Tk()

    sp = SplashScreen(root)
    sp.config(bg="#3366ff")

    m = Label(sp, text="This is a test of the splash screen\n\n\nThis is only a test.\nwww.sunjay-varma.com")
    m.pack(side=TOP, expand=YES)
    m.config(bg="red", justify=CENTER, font=("calibri", 29))

    Button(sp, text="Press this button to kill the program", bg='red', command=root.destroy).pack(side=BOTTOM, fill=X)
    root.mainloop()

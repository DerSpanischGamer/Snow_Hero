from tkinter import *
import os
import json

root = Tk()
largueur = 720
ancheur = 480
frame = Frame(root, width = largueur, height = ancheur)

def key(e):
    print("pressed", e.char)

w = Scale(root, from_=0, to=1, resolution = 0.01, orient = HORIZONTAL)
w.set(0.5)
w.pack()

print(w.get())

frame.bind("<KeyPress>", key)        # detecte la touche que l'utilisateur a appuye
frame.pack()

frame.focus_set()
root.mainloop()

from tkinter import *

import Threading
from queue import Queue
import time

root = Tk()
largueur = 720
ancheur = 480
frame = Frame(root, width = largueur, height = ancheur)

def key(e):
    print("pressed", e.char)

print_lock = threading.Lock()
q = Queue()

for x in range(10):
    t = threading.Thread(target = threader)
    

frame.bind("<KeyPress>", key)        # detecte la touche que l'utilisateur a appuye
frame.pack()

frame.focus_set()
root.mainloop()

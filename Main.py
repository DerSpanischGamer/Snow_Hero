from tkinter import *

class MenuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Snow Hero")

root = Tk()
root.geometry("720x480")
m = MenuGUI(root)
root.mainloop()

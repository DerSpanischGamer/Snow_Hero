from tkinter import Tk

class MenuGUI:
    def __init__(self, master):
        self.master = master
        master.title("50% awesome, 50% nicoly")

    def greet(self):
        print("Henlo")

root = Tk()
m = MenuGUI(root)
root.mainloop()

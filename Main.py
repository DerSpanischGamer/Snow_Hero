from tkinter import *
import os

class MenuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Snow Hero")

        i = 0
        for dos in os.walk(os.path.curdir + "//chasons"): # on prend une liste de tous les dossiers et sous dossiers
            for chanson in dos[1]: # dedans l'object dos, seulement nous interesse le deuxieme element (on commence par 0), mais on ne peut pas faire une variable x qui soit egale au truc, on doit faire une etape intermediare avec la boucle for :(
                w = Button(text = str(chanson)).place(x = 100, y = (i * 50) + 50) # faire que le buton lance l'ecran pour selectionner la chason ou pas
                i += 1
            break

root = Tk()
root.geometry("720x480")

m = MenuGUI(root)
root.mainloop()

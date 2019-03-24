from tkinter import *
import os
import test

class MenuGUI:
    def __init__(self, master):
        self.master = master
        master.title("Snow Hero")

        dir = "" # le directory de la chanson


        def sortir():
            master.destroy()

        Label(master, text = "Snow Hero", font = ("Helvetica", 40)).place(x = 240, y = 0)
        Button(master, text = "Sortir", command = sortir).place(x = 300, y = 430)

        def lancerChanson(titre):
            dir = titre

        i = 0
        for dos in os.walk(os.path.curdir + "//chasons"): # on prend une liste de tous les dossiers et sous dossiers
            for chanson in dos[1]: # dedans l'object dos, seulement nous interesse le deuxieme element (on commence par 0), mais on ne peut pas faire une variable x qui soit egale au truc, on doit faire une etape intermediare avec la boucle for :(
                w = Button(master, text = str(chanson), command=lancerChanson(str(chanson))).place(x = 100, y = (i * 50) + 50) # faire que le buton lance l'ecran pour selectionner la chason ou pas
                i += 1
            break
        #test.__init__(self, master)

largueur = 720
ancheur = 480

root = Tk()
root.geometry(str(largueur) + "x" + str(ancheur))

m = MenuGUI(root)
root.mainloop()

# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Import Timer pour pouvoir appeler des fonctions chaque x secondes
from threading import Timer
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer json pour pouvoir ouvrir des fichiers jsons
import json

import time
from random import randint

root = Tk()
root.title("Snow Hero !")
root.resizable(False, False)
# La fonction sortir est tout au debut pour qu'elle soit la premiere a etre chargee
def sortir():
    root.destroy()

# Espace variables
pause = False    # le jeu est-il pause?
jeuActif = False # false si le joueur joue pas, true s'il joue

largueur = 720
ancheur = 480

lignes = [[], [], [], [], []]
dispo = [0, 0, 0, 0, 0]
colors = ["green", "red", "yellow", "blue", "orange"]

chanson = [] # chaque element de l'array represente une actualisation du jeu qui doit se passer chaque "actuTemps" secondes

actuTemps = 0.05
blockSpawn = 7

oldtime = - actuTemps - 20 # Utilise pour bouger des blocs
newtime = 0

frame = Frame(root)

volume = 0.2 # effacer si ce qu'il y a juste apres n'est pas commente
# Decomenter si a la fin on a reussi a faire qu'on puisse lire des fichiers
# try:
#     volume = eval(sys.argv[1])
#     dir = sys.argv[2]
# except:
#     print("Erreur avec les arguments ._.")
#     sortir()

# On charge le fichier qui gardera tous les donnees

# Ici il faudra dessiner la guitarre, le fond et les points

canvas = Canvas(root, height = ancheur, width = largueur)
canvas.pack()

canvas.create_rectangle(185, 0, 535, 480, fill = "black", outline = "white") # Guitarre

canvas.create_line(255, 0, 255, 480, fill = "white")
canvas.create_line(325, 0, 325, 480, fill = "white")
canvas.create_line(395, 0, 395, 480, fill = "white")
canvas.create_line(465, 0, 465, 480, fill = "white")

canvas.create_rectangle(195, 420, 245, 470, outline = "green")
canvas.create_rectangle(265, 420, 315, 470, outline = "red")
canvas.create_rectangle(335, 420, 385, 470, outline = "yellow")
canvas.create_rectangle(405, 420, 455, 470, outline = "blue")
canvas.create_rectangle(475, 420, 525, 470, outline = "orange")

# Preparer pygames pour jouer des chasons

# Ici il y aura un probleme (except) si la fenetre a ete detruite avec d'etre montree, c'est a dire, s'il y a eu un probleme pendant que le jeu se loadait
try:
    frame.bind("<FocusOut>", pause) # l'utilisateur n'a pas le jeu selectionne, du coup on met en pause s'il etait en train de jouer
    frame.pack()
    frame.focus_set()
except:
    pass

# Finalement on lance la chanson avec les carres

class Shape: # Celui-ci sera le responsable de creer les rectangles
    def __init__(self, id, coords, canvas):
        self.id = id
        self.coords = coords
    def spawn(self, canvas, color):
        """Crée un rectagle"""
        canvas.create_rectangle(self.coords, tag="note", fill = color)

def bougerCarres(): # Meme fonction pour bouger et creer les carres
    i = 0
    while not pause:
        newtime = time.time()
        global oldtime
        if newtime - oldtime >= actuTemps:
            oldtime = newtime
            canvas.move("note", 0, 5) # On bouge les notes
            # Regarder si l'utilsateur a raté la note pour l'effacer
            notes = canvas.find_withtag("note")

            for note in notes:
                if canvas.coords(note)[1] >= 400: canvas.delete(note)
            canvas.update()     # Et on actualise le canvas

            i += 1
            if i > blockSpawn:
                spawnerCarres()
                i = 0
        time.sleep(0.01)


def spawnerCarres(ligne = 0):
    #l = ligne # Activer si on reussi a faire ce systeme automatique
    l = randint(0, len(lignes) - 1)
    carre = Shape(0, ((l * 70) + 195, -50, (l * 70) + 245, 0), canvas)
    lignes[l].append(carre.spawn(canvas, colors[l]))


# Gerer les cles
def key(event):
    print("pressed", repr(event.char))

frame.bind("<Key>", key) # ajotuer la detection des touches

bougerCarres()
root.mainloop()

# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Import Timer pour pouvoir appeler des fonctions chaque x secondes
from threading import Timer
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer pygame surtout pour jouer les chasons, rien d'autre
import pygame
from pygame import mixer
# Importer json pour pouvoir ouvrir des fichiers jsons
import json

root = Tk()

# La fonction sortir est tout au debut pour qu'elle soit la premiere a etre chargee
def sortir():
    root.destroy()

# Espace variables
pause = False    # le jeu est-il pause?
jeuActif = False # false si le joueur joue pas, true s'il joue

largueur = 720
ancheur = 480

carres = []

chanson = [] # chaque element de l'array represente une actualisation du jeu qui doit se passer chaque "actuTemps" secondes
actuTemps = 0.125

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

pygame.init()
pygame.mixer.pre_init(frequency = 22050, size = -16, channels = 2, buffer = 4096)
pygame.mixer.init()
pygame.mixer.music.set_volume(volume)

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
    def spawn(self, canvas):
        """Crée un rectagle"""
        canvas.create_rectangle(self.coords, tag="note")

def bougerSpawnerCarres(): # Meme fonction pour bouger et creer les carres
    while not pause:
        print("Faire plus tard")

# Gerer les cles
def key(event):
    print("pressed", repr(event.char))

frame.bind("<Key>", key) # ajotuer la detection des touches

root.mainloop()

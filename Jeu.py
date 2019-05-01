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

frame = Frame(root, height = ancheur, width = largueur)

try:
    volume = eval(sys.argv[1])
    dir = sys.argv[2]
except:
    print("Erreur avec les arguments ._.")
    sortir()

# On charge le fichier qui gardera tous les donnees

fichier = open("./chansons/" + dir + "/chanson.txt", "r")
for ligne in fichier:
    carres.append(ligne)
fichier.close()

# Ici il faudra dessiner la guitarre, le fond et les points

c = Canvas(root)
c.pack()
c.create_rectangle(0, 200, 400, 400)

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

# Celui-ci sera le responsable de creer les rectangles
class Shape:
    def __init__(self, id, coords, canvas):
        self.id = id
        self.coords = coords
    def spawn(self, canvas):
        """Crée un rectagle"""
        canvas.create_rectangle(self.coords, tag="note")

# Meme fonction pour bouger et creer les carres
def bougerSpawnerCarres():
    while pause == False:
        print("Faire plus tard")

root.mainloop()

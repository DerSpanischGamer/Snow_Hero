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
largueur = 720
ancheur = 480

cen = 455 # centre des carres dont on detecte (carres ou l'utilisateur doit appuyer)

lignes = [[], [], [], [], []]
dispo = [0, 0, 0, 0, 0]
colors = ["green", "red", "yellow", "blue", "orange"]

touches = [90, 88, 66, 78, 77] # z, x, b, n, m

reset = False

chanson = [] # chaque element de l'array represente une actualisation du jeu qui doit se passer chaque "actuTemps" secondes

actuTemps = 0.05
blockSpawn = 15

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

b0 = canvas.create_rectangle(195, 420, 245, 470, outline = "green")
b1 = canvas.create_rectangle(265, 420, 315, 470, outline = "red")
b2 = canvas.create_rectangle(335, 420, 385, 470, outline = "yellow")
b3 = canvas.create_rectangle(405, 420, 455, 470, outline = "blue")
b4 = canvas.create_rectangle(475, 420, 525, 470, outline = "orange")

carresFin = [b0, b1, b2, b3, b4]
# Preparer pygames pour jouer des chasons

# Ici il y aura un probleme (except) si la fenetre a ete detruite avec d'etre montree, c'est a dire, s'il y a eu un probleme pendant que le jeu se loadait
try:
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
        id = canvas.create_rectangle(self.coords, tag="note", fill = color)
        return id

def bougerCarres(): # Meme fonction pour bouger et creer les carres
    demarrer.destroy()
    titre.pack_forget()
    titre.pack()

    i = 20
    while True:
        newtime = time.time()
        global oldtime
        if newtime - oldtime >= actuTemps:
            oldtime = newtime
            canvas.move("note", 0, 5) # On bouge les notes
            # Regarder si l'utilsateur a raté la note pour l'effacer
            notes = canvas.find_withtag("note")

            for note in notes:
                if canvas.coords(note)[1] >= 525:
                    canvas.delete(note)
                    for ligne in lignes:
                            if note in ligne:
                                ligne.remove(note)
                                break
            canvas.update()     # Et on actualise le canvas

            i += 1
            if i > blockSpawn:
                spawnerCarres(0)
                i = 0

            global reset
            if reset:
                reset = False
                for i in range(len(carresFin)):
                    canvas.itemconfig(carresFin[i], fill="black")
                canvas.update()
            time.sleep(0.01)

def spawnerCarres(ligne):
    #l = ligne # Activer si on reussi a faire ce systeme automatique
    l = randint(0, len(lignes) - 1)

    carre = Shape(0, ((l * 70) + 195, -50, (l * 70) + 245, 0), canvas)
    lignes[l].append(carre.spawn(canvas, colors[l]))

def detruireCarre(l):
    if len(lignes[l]) == 0: return # la ligne n'a aucun carre

    coor = canvas.coords(lignes[l][0])[1] + 25 # Coordonnees du centre du carre
    if coor - cen < 50 and coor - cen > -50: # Ils sont en train de se toucher, du coup on peut le detecter comme une colision
        canvas.delete(lignes[l][0])
        lignes[l].pop(0)

# Gerer les cles
def key(event):
    l = -1
    try:
        l = touches.index(event.keycode)
    except:
        pass
    if l != -1:
        global reset
        reset = True

        canvas.itemconfig(carresFin[l], fill=colors[l])
        canvas.update()

        detruireCarre(l)

# Dessiner l'ecran pre-jeu
titre = Label(root, text = "Snow Hero", font=("Helvetica", 50))
titre.pack()
titre.place(x = 194, y = 0)

demarrer = Button(root, height = 2, width = 9, text = "Commencer", command= lambda: bougerCarres())
demarrer.pack()
demarrer.place(x = 325, y = ancheur/2 - 12)

frame.bind("<Key>", key) # ajotuer la detection des touches

root.mainloop()

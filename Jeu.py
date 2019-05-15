# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Import Timer pour pouvoir appeler des fonctions chaque x secondes
from threading import Timer
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer json pour pouvoir ouvrir des fichiers jsons
import json
from PIL import Image, ImageTk
from tkinter import ttk

# Importer Threading pour avoir un Thread qui gere la guitarre
import threading
# Importer serial pour pouvoir se communiquer avec la guitarre
import serial
# Importer tout ca pour pouvoir trouver le port de la guitarre
import serial.tools.list_ports

import asyncio

import atexit

import sys

import time
from random import randint

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

carresFin = []

port = ""# Le port auquel la guitarre est connectee
guitarre = False # Par defaut il n'y a pas de guitarre

reset = False # S'il faut reseter les carres (animation)
sortir = False # True s'il faut sortir du loop

actuTemps = 0.05
blockSpawn = 15

oldtime = - actuTemps - 20 # Utilise pour bouger des blocs
newtime = 0

# Gerer les cles
def key(event):
    t = event.keycode
    if t == 27:
        global sortir
        sortir = True
    l = -1
    try:
        l = touches.index(t)
    except:
        pass
    if l != -1 and not guitarre:
        global reset
        reset = True

        canvas.itemconfig(carresFin[l], fill=colors[l])
        canvas.update()

        detruireCarre(l)

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

    chercher.destroy()

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

            global sortir
            if sortir:
                break
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

async def ecouter():
    """ Attend les touches sur la guitarre"""
    ser = serial.Serial(port, 9600)
    while True:
        detruireCarre(int(chr(ser.readline()[0])))
        global sortir
        if sortir:
            break
    root.quit()


def _asyncio_thread(async_loop):
    async_loop.run_until_complete(ecouter())

def chercherGuitarre(async_loop):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p[1]:
            global port
            port = p[0]
            guitarre = True

            global chercher
            chercher.destroy()

            threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()

def exit_handler():
    async_loop.close()
    print ('My application is ending!')

if __name__ == '__main__':
    root = Tk()
    root.title("Snow Hero !")
    root.resizable(False, False)

    frame = Frame(root)

    frame.pack()
    frame.focus_set()
    frame.bind("<Key>", key) # ajotuer la detection des touches

canvas = Canvas(root, height = ancheur, width = largueur)
canvas.pack()

# load the .gif image file
gif1 = PhotoImage(file='mus.png')
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0,0, image=gif1, anchor=NW)

#creatre score

score = Label(root, text="Your score", bg="red")
score.pack()
score.place(x=20 ,y=150)
temps = Label(root, text="Temps restant", bg="red")
temps.pack()
temps.place(x=20,y=180)

# Dessiner l'ecran
titre = Label(root, text = "Snow Hero", font=("Helvetica", 50))
titre.pack()
titre.place(x = 194, y = 0)

demarrer = Button(root, height = 2, width = 9, text = "Commencer", command = lambda: bougerCarres())
demarrer.pack()
demarrer.place(x = 325, y = ancheur/2 - 12)

async_loop = asyncio.get_event_loop() # Boucle asyncronisee

chercher = Button(root, height = 2, width = 20, text = "Chercher guitarre", command = lambda: chercherGuitarre(async_loop))
chercher.pack()
chercher.place(x = 285, y = ancheur/2 + 50)


    # Ici on dessine la guitarre, le fond et les points
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
atexit.register(exit_handler)


















mainloop()

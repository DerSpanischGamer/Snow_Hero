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
def out():
    global arreterTiming
    arreterTiming = True
    root.destroy()

# Espace variables
largueur = 720
ancheur = 480

cen = 455 # centre des carres dont on detecte (carres ou l'utilisateur doit appuyer)

score_total = 0
jeu_points = []

arreterTiming = False
timer = 0 # Conte les secondes depuis le debut

carresFin = []

reset = False # S'il faut reseter les carres (animation)
sortir = False # True s'il faut sortir du loop

actuTemps = 0.05
blockSpawn = 15
carresTime = 0 # Le nombre de actulisation qu'il y a eu depuis le dernier carre

oldtime = - actuTemps - 20 # Utilise pour bouger des blocs
newtime = 0

# Gerer les cles
def key(event):
    t = event.keycode
    if t == esc:
        global sortir
        sortir = True

        out()
    l = -1
    try:
        l = touches.index(t)
    except:
        pass
    if l != -1 and not guitarre:
        global reset
        reset = True

        canvas.itemconfig(carresFin[l], fill = colors[l])
        canvas.update()

        detruireCarre(l)

class Shape: # Celui-ci sera le responsable de creer les rectangles
    def __init__(self, id, coords, canvas):
        self.id = id
        self.coords = coords
    def spawn(self, canvas, color):
        """Crée un rectagle"""
        id = canvas.create_rectangle(self.coords, tag="note", fill = color)
        return id

def bougerCarres(loop): # Meme fonction pour bouger et creer les carres
    demarrer.destroy()

    titre.pack_forget()
    titre.pack()

    chercher.destroy()

    threading.Thread(target=timing_thread, args=(loop,)).start()

    carresTime = 20
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

            carresTime += 1
            if carresTime > blockSpawn:
                spawnerCarres(0)
                carresTime = 0

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

def points(x):
    dis = canvas.coords(lignes[x][0])[1] - 420
    global score_total
    if dis>0:
        sur=50-dis
        per=(sur*100)/50
        jeu_points.append(per)
    elif dis<0:
        sur=50+dis
        per=(sur*100)/50
        jeu_points.append(per)
    else:
        jeu_points.append(100)
    score_total = sum(jeu_points) / len(jeu_points)

def spawnerCarres(ligne):
    #l = ligne # Activer si on reussi a faire ce systeme automatique
    l = randint(0, len(lignes) - 1)

    carre = Shape(0, ((l * 70) + 195, -50, (l * 70) + 245, 0), canvas)
    lignes[l].append(carre.spawn(canvas, colors[l]))

def detruireCarre(l):
    if len(lignes[l]) == 0: return # la ligne n'a aucun carre

    coor = canvas.coords(lignes[l][0])[1] + 25 # Coordonnees du centre du carre
    if coor - cen < 50 and coor - cen > -50: # Ils sont en train de se toucher, du coup on peut le detecter comme une colision
        points(l)
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

def timing():
    global arreterTiming
    while not arreterTiming:
        global timer
        timer += 1
        print(timer)
        time.sleep(1)
        # actualiser le conteur
    print("On recommence?")

def timing_thread(l):
    l.run_until_complete(timing())

def recommencer(loop):
    # Reinitialiser les points
    jeu_points = []
    score_total = 0

    for lin in lignes:
        for i in lin:
            canvas.delete(i)

    for lin in lignes:
        for i in lin: lin.remove(i)

    carresTime = 0

    global arreterTiming
    arreterTiming = True

    threading.Thread(target=timing_thread, args=(loop,)).start()

def exit_handler():
    async_loop.close()
    print("Votre précision en pourcentage est de : ", score_total, "%.")
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

    async_loop = asyncio.get_event_loop()   # Boucle asyncronisee
    conteur_loop = asyncio.get_event_loop() # Boucle pour gerer le passage du temp

    demarrer = Button(root, height = 2, width = 9, text = "Commencer", command = lambda: bougerCarres(conteur_loop))
    demarrer.pack()
    demarrer.place(x = 325, y = ancheur/2 - 12)

    chercher = Button(root, height = 2, width = 20, text = "Chercher guitarre", command = lambda: chercherGuitarre(async_loop))
    chercher.pack()
    chercher.place(x = 285, y = ancheur/2 + 50)

    recom = Button(root, height = 2, width = 9, text = "Recommencer", command = lambda: recommencer(conteur_loop))
    recom.pack()
    recom.place(x = 285, y = ancheur / 2 - 25)

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

    root.mainloop()

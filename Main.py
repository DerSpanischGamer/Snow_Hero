# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer pygame surtout pour jouer les chasons
import pygame
from pygame import mixer
# Importer json pour pouvoir ouvrir des fichiers jsons
import json
# Importer scaleinsound
import winsound

root = Tk()

# Zone des variables
pause = False    # le jeu est-il pause?
jeuActif = False # false si le joueur joue pas, true s'il joue
dir = ""         # le directory de la chanson qui a été selectionnée

largueur = 720
ancheur = 480

chansons = [] # une liste qui garde tous les dossiers avec des chasons dedans

volume = DoubleVar()

titre = "Titre"
auteur = "Auteur"
description = "Description"
image = ""

# Charger la configuration

with open('./config.json') as f:
    donnees = json.load(f)
    volume = donnees['volume']

# Zones des fonctions
def sortir():
    root.destroy()

def key(event):
    print("pressed", repr(event.char))

def pause(event):
    if jeuActif:
        pause = True

def callback(event):
    print ("clicked at", event.x, event.y)


def actuVol(d):
    volume = eval(d)
    pygame.mixer.music.set_volume(volume)

    with open("./config.json") as f:
        d = json.load(f)
        d['volume'] = volume

        with open("./config.json", "w") as e:
            json.dump(d, e)

# Dessiner le menu principal

frame = Frame(root, width = largueur, height = ancheur)

Label(text = "Snow Hero", font = ("Helvetica", 40)).place(x = 240, y = 0)
Button(text = "Sortir", command = sortir).place(x = 360, y = 450)

# Preparer pygames pour jouer des chasons

pygame.init()
pygame.mixer.pre_init(frequency = 22050, size = -16, channels = 2, buffer = 4096)
pygame.mixer.init()
pygame.mixer.music.set_volume(volume)

# Regarder les fichiers qui sont en ./chansons et les montrer

def test():
    print("lmao")

i = 0
for dos in os.walk(os.path.curdir + "//chansons"): # on prend une liste de tous les dossiers et sous dossiers

    scrollbar = Scrollbar(root)
    scrollbar.pack(side = RIGHT, fill = Y)

    listbox = Listbox(root, yscrollcommand = scrollbar.set)

    for chanson in dos[1]: # dedans l'object dos, seulement nous interesse le deuxieme element (on commence par 0), mais on ne peut pas faire une variable x qui soit egale au truc, on doit faire une etape intermediare avec la boucle for :(
        listbox.insert(END, str(chanson))
        chansons.append(str(chanson))
    listbox.place(x = 50, y = 70)
    scrollbar.config(command = listbox.yview)

    def lancerChanson():
        try:
            dir = chansons[listbox.curselection()[0]]
        except:
            Label(text = "Selectionne une chason", bg = "red").place(x = 315, y = 260)
            winsound.Beep(300, 100)

    Button(text = "Jouer", command = lancerChanson).place(x = 80, y = 240)
    break # break car seulement le premier element de la liste nous interesse car c'est le seul qui dis les dossiers dedans la URL choisie


if len(chansons) != 0: # Selectioner la premiere chason
    listbox.select_set(0)
    dir = chansons[listbox.curselection()[0]]

scale = Scale(root, from_=0, to=1, resolution = 0.01, orient = HORIZONTAL)
scale.set(volume)
scale.place(x = 215, y = 248)
scale.config(command = actuVol)

# TODO: Nicoly tu fais ca, tu dois dessiner a droite une partie ou il y a toute la description de la chason, c'est moi qui va te donner tous les donnees sur la chason tqt
# Dessiner la preselection de l'image

# Configurer les binds

frame.bind("<FocusOut>", pause) # l'utilisateur n'a pas le jeu selectionne, du coup on met en pause s'il etait en train de jouer
frame.bind("<Button-1>", callback) # fait un printe d'ou on a clique
frame.bind("<Key>", key)        # detecte la touche que l'utilisateur a appuye
frame.pack()
frame.focus_set()

selec = ""
while True:
    try:
        # Cette partie gère la chanson selectionee
        if selec != listbox.curselection()[0]:
            pygame.mixer.music.stop()
            selec = listbox.curselection()[0]

            pygame.mixer.music.load("./chansons/" + chansons[selec] + "/chanson.aiff")
            pygame.mixer.music.play()
        # Cette partie gère le volume

    except:
        pass
    try:
        root.update_idletasks()
        root.update()
    except:
        print("Bye bye :)")
        break

root.mainloop()


# montrer les details de la chanson

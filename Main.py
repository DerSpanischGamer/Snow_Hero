# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Importer os pour pouvoir acceder aux dossiers
import os
# Importer pygame surtout pour jouer les chasons
import pygame
from pygame import mixer


# TODO: fixer le volume (mettre un slider ?) aussi faire beau pour qu'on puisse voir toutes les infos



root = Tk()

# Zone des variables
pause = False    # le jeu est-il pause?
jeuActif = False # false si le joueur joue pas, true s'il joue
dir = ""         # le directory de la chanson qui a été selectionnée

largueur = 720
ancheur = 480

chansons = [] # une liste qui garde tous les dossiers avec des chasons dedans

# Zones des fonctions
def sortir():
    exit()

def key(event):
    print("pressed", repr(event.char))

def pause(event):
    if jeuActif:
        pause = True

def callback(event):
    print ("clicked at", event.x, event.y)

# Dessiner le menu principal

frame = Frame(root, width = largueur, height = ancheur)

Label(text = "Snow Hero", font = ("Helvetica", 40)).place(x = 240, y = 0)
Button(text = "Sortir", command = sortir).place(x = 360, y = 450)

# Preparer pygames pour jouer des chasons

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# Regarder les fichiers qui sont en ./chansons et les montrer

i = 0
for dos in os.walk(os.path.curdir + "//chansons"): # on prend une liste de tous les dossiers et sous dossiers

    scrollbar = Scrollbar(root)
    scrollbar.pack(side = RIGHT, fill = Y)

    listbox = Listbox(root, yscrollcommand = scrollbar.set)

    for chanson in dos[1]: # dedans l'object dos, seulement nous interesse le deuxieme element (on commence par 0), mais on ne peut pas faire une variable x qui soit egale au truc, on doit faire une etape intermediare avec la boucle for :(
        listbox.insert(END, str(chanson))
        chansons.append(str(chanson))
    listbox.place(x = 310, y = 70)
    scrollbar.config(command = listbox.yview)

    def lancerChanson():
        try:
            dir = chansons[listbox.curselection()[0]]
            print(dir)
        except:
            Label(text = "Selectionne une chason", bg = "red").place(x = 315, y = 260)
            winsound.Beep(300, 100)

    Button(text = "Jouer", command = lancerChanson).place(x = 360, y = 240)
    break # break car seulement le premier element de la liste nous interesse car c'est le seul qui dis les dossiers dedans la URL choisie

# Configurer les binds

frame.bind("<FocusOut>", pause) # l'utilisateur n'a pas le jeu selectionne, du coup on met en pause s'il etait en train de jouer
frame.bind("<Button-1>", callback) # fait un printe d'ou on a clique
frame.bind("<Key>", key)        # detecte la touche que l'utilisateur a appuye
frame.pack()
frame.focus_set()

selec = ""
sound = pygame.mixer.Sound("./chanson.aiff")
while True:
    try:
        if selec != listbox.curselection()[0]:
            sound.stop()
            selec = listbox.curselection()[0]

            sound = pygame.mixer.Sound("./chansons/" + chansons[selec] + "/chanson.aiff")
            sound.play()
    except:
        pass
    root.update_idletasks()
    root.update()

root.mainloop()


# montrer les details de la chanson

# Importer tkinter pour pouvoir faire une fenetre
from tkinter import *
# Importer Threading pour avoir un Thread qui gere la guitarre
import threading
# Importer serial pour pouvoir se communiquer avec la guitarre
#import serial
# Importer tout ca pour pouvoir trouver le port de la guitarre
#import serial.tools.list_ports
# Importer asyncio pour faire des fonctions asynchrones
import asyncio
# Importer atexit pour pouvoir faire des choses quand le programme se ferme
import atexit
# Pas necessaire en theorie
import sys
# Time pour pouvoir avoir un rythme stable
import time
# Pour faire l'apparition des carres dans les colognes aleatoires
from random import randint

# Espace variables
largueur = 720 # largueur fenetre
ancheur = 480 # ancheur fenetre

cen = 455 # centre des carres dont on detecte (carres ou l'utilisateur doit appuyer)

temprest = 30 # Temps restant

score_total = 0 #Score total en pourcentage
jeu_points = [] #Pourcentage de precision pour chaque carre detruit

lignes = [[], [], [], [], []] # Blocs par ligne
colors = ["green", "red", "yellow", "blue", "orange"] # Couleur de chaque ligne

touches = [] # Touches (rempli au debut)

carresFin = []

port = ""# Le port auquel la guitarre est connectee
guitarre = False # Par defaut il n'y a pas de guitarre

loop = asyncio.get_event_loop() # Boucle pour gerer la guitarre
ecouter_t = None # Task pour la fonction ecouter

reset = False # S'il faut reseter les carres (animation)
sortir = False # True s'il faut sortir du loop

actuTemps = 0.05 # Interval de temps de chaque cycle
blockSpawn = 15 # Nombre de cycles qui doivent passer depuis le dernier bloc apparu pour faire apparaitre un autre
actuTimer = 0 # Nombre de cycles passes depuis la derniere mise a jour du conteur en arriere

oldtime = - actuTemps - 20 # Utilise pour bouger des blocs
newtime = 0

sor = None # Bouton sortir

# La fonction sortir est tout au debut pour qu'elle soit la premiere a etre chargee
def out():
    root.destroy()
    loop.stop()
    loop.close()

def keysetup_instruction():
    """ Instruction pour assigner les touches via la console """
    if len(touches) == 5:
        setup_button.destroy()
        print("Les touches on étés assignées")
    else:
        print("Quel touche pour la colonne", len(touches)+1, "? : ")

def key(event):
    """ En entree prent une touche, la transforme en son id.
    Sert pour l'assignation des touches ainsi que pour detruire ou pas les carres. """
    t = event.keycode
    if not guitarre and len(touches) < 5: #Verifie si la touche a ete input pour etre assignee
        if t in touches:
            print("Touche deja assignee!")
        else:
            touches.append(t) #La touche est assignee
            keysetup_instruction() #Instruction pour prochaine touche (colonne)
    else:
        l = -1
        if t == 27:
            global sortir
            sortir = True
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

class Shape: # Celui-ci sera le responsable de creer les rectangles
    def __init__(self, id, coords, canvas):
        self.id = id
        self.coords = coords
    def spawn(self, canvas, color):
        """Crée un rectagle"""
        id = canvas.create_rectangle(self.coords, tag="note", fill = color)
        return id

def recommencer():
    global score_total
    global jeu_points
    global sco
    score_total = 0
    jeu_points = []
    sco.set(str(round(score_total, 4)) + "%")

    for lin in lignes:
        for i in lin:
            canvas.delete(i)

    for lin in lignes:
        for i in lin:
            lin.remove(i)

    global sortir
    sortir = False

    i = 0

    canvas.update()
    bougerCarres()

def bougerCarres(): # Meme fonction pour bouger et creer les carres
    if not guitarre and len(touches) < 5: #Ne peut commencer le jeu que si 5 touches sont assignees
        print("Les touches n'ont pas été assignées!")
    else:
        # Effacer tous les boutons
        global sor
        try: sor.destroy()
        except: pass

        global demarrer
        demarrer.destroy()

        titre.pack_forget()
        titre.pack()

        chercher.destroy()

        global temprest
        temprest = 30
        temp.set(temprest)

        i = 20
        while True:
            newtime = time.time()
            global oldtime
            if newtime - oldtime >= actuTemps:
                oldtime = newtime
                canvas.move("note", 0, 5) # On bouge les notes
                # Regarder si l'utilsateur a raté la note pour l'effacer
                notes = canvas.find_withtag("note")

                for note in notes:
                    if canvas.coords(note)[1] >= 525:
                        canvas.delete(note)
                        for ligne in lignes:
                                if note in ligne:
                                    ligne.remove(note)
                                    break

                i += 1
                if i > blockSpawn:
                    spawnerCarres(0)
                    i = 0

                global reset
                if reset:
                    reset = False
                    for i in range(len(carresFin)):
                        canvas.itemconfig(carresFin[i], fill="black")

                global actuTimer
                actuTimer += 1
                if actuTimer > 20:
                    actuTimer = 0
                    temprest -= 1
                    temp.set(temprest)
                if temprest == 0: break

                sco.set(str(round(score_total, 4)) + "%")

                global sortir
                if sortir:
                    break
                canvas.update()
                time.sleep(0.01)
        sor = Button(root, height = 2, width = 9, text = "Sortir", command = lambda: out())
        sor.pack()
        sor.place(x = 305, y = ancheur/2  + 12)

        demarrer = Button(root, height = 2, width = 12, text = "Recommencer", command = lambda: recommencer())
        demarrer.pack()
        demarrer.place(x = 305, y = ancheur/2 - 30)

def points(x):
    """Calcule points pour chaque destruction et met a jour le score total"""
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
    score_total=sum(jeu_points) / len(jeu_points)

def spawnerCarres(ligne):
    #l = ligne # Activer si on reussi a faire ce systeme automatique
    l = randint(0, len(lignes) - 1)

    carre = Shape(0, ((l * 70) + 195, -50, (l * 70) + 245, 0), canvas)
    lignes[l].append(carre.spawn(canvas, colors[l]))

def detruireCarre(l):
    if len(lignes[l]) == 0: # la ligne n'a aucun carre
        jeu_points.append(0) #Si la touche est appuyee sans qu'il y ait de carre cela est compte comme 0% de precision. (Pour eviter le 'spam' des touches)
        score_total=sum(jeu_points) / len(jeu_points)

    coor = canvas.coords(lignes[l][0])[1] + 25 # Coordonnees du centre du carre
    if coor - cen < 50 and coor - cen > -50: # Ils sont en train de se toucher, du coup on peut le detecter comme une colision
        points(l) #Calcul des points avant destruction
        canvas.delete(lignes[l][0])
        lignes[l].pop(0)
    else: #Si la touche est appuyee trop tot, cela est compte comme 0% de precision.
        jeu_points.append(0)
        score_total=sum(jeu_points) / len(jeu_points)

async def ecouter():
    """ Attend les touches sur la guitarre"""
    ser = serial.Serial(port, 9600)
    while True:
        detruireCarre(int(chr(ser.readline()[0])))
        global sortir
        if sortir:
            break
    out()

def _asyncio_thread(async_loop):
    async_loop.run_until_complete(ecouter())

def chercherGuitarre(async_loop):
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p[1]:
            global port
            port = p[0]
            global guitarre
            guitarre = True

            global chercher
            chercher.destroy()
            setup_button.destroy()

            threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()

def exit_handler():
    loop.close()
    print("Votre précision en pourcentage est de : ", score_total, "%.")
    print ('My application is ending!')

if __name__ == '__main__':
    root = Tk()
    root.title("Snow Hero !")
    root.resizable(False, False)


    sco = StringVar("")
    temp = StringVar("")

    frame = Frame(root)

    frame.pack()
    frame.focus_set()
    frame.bind("<Key>", key) # ajotuer la detection des touches

    canvas = Canvas(root, height = ancheur, width = largueur)
    canvas.pack()

    # Dessiner l'ecran

    # Creer l'image de fond
    gif1 = PhotoImage(file='mus.png')
    canvas.create_image(0,0, image=gif1, anchor=NW)

    #creatre score
    score = Label(root, textvariable=sco, bg="red")
    score.pack()
    score.place(x=20 ,y=150)

    temps = Label(root, textvariable=temp, bg="red") #Timer
    temps.pack()
    temps.place(x=20,y=180)

    titre = Label(root, text = "Snow Hero", font=("Helvetica", 50))
    titre.pack()
    titre.place(x = 194, y = 0)

    demarrer = Button(root, height = 2, width = 9, text = "Commencer", command = lambda: bougerCarres())
    demarrer.pack()
    demarrer.place(x = 325, y = ancheur/2 - 20)

    chercher = Button(root, height = 2, width = 20, text = "Chercher guitarre", command = lambda: chercherGuitarre(loop))
    chercher.pack()
    chercher.place(x = 285, y = ancheur/2 + 25)

    setup_button = Button(root, height = 2, width = 20, text = "Assigner touches", command = lambda: keysetup_instruction())
    setup_button.pack()
    setup_button.place(x = 285, y = ancheur/2 + 70)

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

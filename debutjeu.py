from tkinter import *
from random import *
import time

pause = False

def move():
    '''Bouge l'objet vers le bas, tant que pause soit False (pas de pause...)'''
    bou2.forget()

    while pause == False:
        notes = can1.find_withtag("note") # prend toutes les notes (tous les objects avec la tag note)

        for note in notes:
            if can1.coords(note)[1] >= 250: can1.delete(note) # regarde les coordonnees et si elles >= 250 efface l'object
            else:                           can1.move("note", 0, 15)

        can1.update()
        time.sleep(0.1)
    bou2.pack()

class Shape:
    def __init__(self, id, coords, canvas):
        '''il faudra surement enlever le coords d'ici'''
        self.id = id
        self.coords = coords
    def spawn(self, canvas):
        '''crée un rectagle'''
        id = canvas.create_rectangle( self.coords, tag="note" )

win=Tk()

can1= Canvas(win , bg= 'dark grey', width=200, height= 500)
limit= can1.create_line(0, 250, 200, 250, fill='white') #ligne droite, =limite a partir laquelle on peut detruire rectangle
can1.pack()

bou1 = Button(win ,text='rectangle', width = 8, command=lambda: rec1.spawn(can1) ) #cree un rectangle
bou1.pack(side=BOTTOM)

bou2 = Button(win, text='start', width=8, command = move) #bouge le rectangle
bou2.pack()


rec1=Shape(0, (10, 10, 30, 30), can1) #je sais pas comment ca marche mais ca a marche


win.mainloop()

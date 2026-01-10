from tkinter import *
import time
from Cotxe import *
from ZPoint import *
from WPoint import *
from pantalla import *
from joc import *
import json

tk=Tk()
tk.attributes("-fullscreen", True)
w = Canvas(tk)
w.pack(fill=BOTH, expand=True)
tk.bind("<Escape>", lambda e:tk.destroy())

ample_window = tk.winfo_screenwidth()
alt_window = tk.winfo_screenheight()

screen=Pantalla(WPoint(0,0),WPoint(500,281),
             ZPoint(0,0),ZPoint(ample_window,alt_window))

# TO-DO: Canviar inicialització cotxes per fitxer .json
c1=Cotxe(250,100,15,23,v=1)
c2=Cotxe(1250,1600,10,8,v=2)
cotxes=[c1]

joc=Joc("Barcelona", cotxes, screen)

while True:
    w.delete("all")
    w.config(bg="#78CC54")
    
    #Dibuixem l'escenari
    for i in range(0,len(joc.parets)-1,2):
        joc.parets[i].show(joc.parets[i+1], w, screen)
    
    for i in range(0, len(joc.recompenses)):
        joc.recompenses[i].show(w, screen)

    for i in range(0, len(joc.obstacles)):
        joc.obstacles[i].show(w, screen)
    
    c1.reset()  
    c1.controls()
    c1.mou()
    c1.xoc_paret(joc)
    c1.recompensa_agafada(joc)
    c1.xoc_obstacle(joc)
    c1.show(w, screen)
    c1.mostra_puntuacio(w, ample_window-50, 20)
    c1.mostra_vides(w, 20, 20)
    
    w.update()
    screen.TranslateWorld(1)
    time.sleep(10/1000)
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
cotxes=[c1,c2]

joc=Joc("sections_UAB", cotxes)

while True:
    w.delete("all")
    for i in range(0,len(joc.parets)-1,2):
        joc.parets[i].dibuixa(joc.parets[i+1], w, screen)
    c1.pinta(w, screen)
    screen.TranslateWorld(1)
    c1.mou()
    w.update()
    time.sleep(20/1000)
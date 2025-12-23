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

c1=Cotxe(1210,1500,10,8,v=1)
c2=Cotxe(1250,1600,10,8,v=2)
cotxes=[c1,c2]

joc=Joc()

while True:
    w.delete("all")
    joc.construir_carretera(screen.wMin,screen.wMax,w,screen)
    screen.TranslateWorld(1)
    w.update()
    time.sleep(50/1000) #50ms de pausa
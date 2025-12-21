from tkinter import *
import time
from Cotxe import *
from VPoint import *
from WPoint import *
from WorldView import *
import json

def lectura_json():
    f=open("carretera.json","r")
    dades=json.load(f)
    f.close()
    cotxes=[]
    for c in dades['cars']:
        c1=Cotxe(c['start_position']["x"],c['start_position']["y"],c['width'],c['height']) 
        cotxes.append(c1)

tk=Tk()
w=Canvas(tk,width=800,height=800)
w.pack() 

wv=WorldView(WPoint(1200,1400),WPoint(1700,1400+500*0.75),
             VPoint(0,0),VPoint(800,600))

#c1=Cotxe(10,10,30,20)
#c2=Cotxe(10,100,30,20,v=1)
#c1=Cotxe(1210,1500,10,5)
#c2=Cotxe(1250,1600,10,5,v=2)
#cotxes=[c1,c2]
cotxes=lectura_json()
while True:
    w.delete("all")
    #w.create_line(10+dx,10,200+dx,200)
    for c in cotxes:
        #c.mou()
        w.create_rectangle(c.x,c.y,c.x+c.w,c.y+c.h)
        #c.pinta(w,wv)
    w.update()
    wv.translateWindow(3,0)
    
    time.sleep(50/1000) #50ms de pausa


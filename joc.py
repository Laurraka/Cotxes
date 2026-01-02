import json
from WPoint import *
from LinearEquation import *
from pantalla import *
from Cotxe import *

#Fer diccionari de ranges de la carretera
f=open("carretera.json","r")
dades=json.load(f)
f.close()

class Joc:
    def __init__(self, escenari, cotxes):
        self.parets=[]
        for tram in dades[escenari].keys():
            self.parets.append(Paret(dades[escenari][tram]['p1']['x'],dades[escenari][tram]['p1']['y'],dades[escenari][tram]['p3']['x'],dades[escenari][tram]['p3']['y']))
            self.parets.append(Paret(dades[escenari][tram]['p2']['x'],dades[escenari][tram]['p2']['y'],dades[escenari][tram]['p4']['x'],dades[escenari][tram]['p4']['y']))

        self.cotxes=[]
        for c in cotxes:
            self.cotxes.append(c) # TO-DO: Canviar inicialització per fitxer .json

class Paret:
    def __init__(self, x0, y0, x1, y1): #(x0,y0) és el punt que està més amunt
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

    def dibuixa(self, w1, w, screen): #self és la paret de l'esquerra. w1 és un objecte paret, i és la paret de la dreta
        P0=screen.WorldToZoomXY(self.x0, self.y0)
        P1=screen.WorldToZoomXY(self.x1, self.y1)
        Q0=screen.WorldToZoomXY(w1.x0, w1.y0)
        Q1=screen.WorldToZoomXY(w1.x1, w1.y1)
        w.create_polygon(
            P0.x, P0.y,
            Q0.x, Q0.y,
            Q1.x, Q1.y,
            P1.x, P1.y,
            fill="#545353"
        )

    def XocaCotxe(self, cotxe): #TO-DO
        V1=WPoint(cotxe.x,cotxe.y)
        V2=WPoint(cotxe.x+cotxe.w*math.cos(cotxe.angle), cotxe.y-cotxe.w*math.sin(cotxe.angle))
        V3=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle))
        V4=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle)+cotxe.w*math.cos(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle)-cotxe.w*math.sin(cotxe.angle))
        
        return False


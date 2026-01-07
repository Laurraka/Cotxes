import keyboard
from LinearEquation import *
from joc import *
import math

import keyboard
from LinearEquation import *
from joc import *
import math

class Cotxe:
    def __init__(self,x,y,w,h,v=1):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.v=v
        self.angle=0

        self.toca_paret = False
        self.toca_obstacle=False
        self.puntuacio=0
        self.vides=3

        self.img_3_cors = carrega_imatge("imatges/3_cors.png", 120, 32)

    def reset(self):
        self.toca_paret = False

    def mou(self):
        self.y=self.y+self.v

    def show(self,w,screen):
        self.y=self.y+self.v

    def show(self,w,screen):
        p1=screen.WorldToZoomXY(self.x,self.y)
        p2=screen.WorldToZoomXY(self.x+self.w*math.cos(self.angle), self.y-self.w*math.sin(self.angle))
        p3=screen.WorldToZoomXY(self.x+self.h*math.sin(self.angle), self.y+self.h*math.cos(self.angle))
        p4=screen.WorldToZoomXY(self.x+self.h*math.sin(self.angle)+self.w*math.cos(self.angle), self.y+self.h*math.cos(self.angle)-self.w*math.sin(self.angle))
        if self.toca_paret:
            w.create_polygon(
                p1.x,p1.y,
                p2.x,p2.y,
                p4.x,p4.y,
                p3.x,p3.y,
                fill="red"
            )
        else:
            w.create_polygon(
                p1.x,p1.y,
                p2.x,p2.y,
                p4.x,p4.y,
                p3.x,p3.y,
                fill="green"
            )
        
    def mostra_puntuacio(self, w, x, y):
        w.create_text(
            x, y,                
            text=f"Punts: {self.puntuacio}",
            fill="black",
            font=("Arial", 14)
        )

    def mostra_vides(self, w, x, y):
        if self.vides==3:
            w.create_image(x, y, image=self.img_3_cors, anchor="nw")
    
    def controls(self):
        if keyboard.is_pressed('left'):
            self.x=self.x-2
        if keyboard.is_pressed('right'):
            self.x=self.x+2
    
    def xoc_paret(self, joc):
        for paret in joc.parets:
            if paret.xoca_cotxe(self):
                self.toca_paret = True

    def recompensa_agafada(self, joc):
        for rec in joc.recompenses:
            if rec.agafada(self, joc):
                break

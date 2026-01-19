import keyboard
from LinearEquation import *
from joc import *
import math
from funcions_adicionals import *

class Cotxe:
    def __init__(self,x,y,w,h,v=1):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.v=v
        self.angle=0

        self.toca_obstacle=False
        self.puntuacio=0
        self.vides=3
        self.mort=False

        self.img_3_cors = carrega_imatge("imatges/3_cors.png", 120, 32)
        self.img_2_cors = carrega_imatge("imatges/2_cors.png", 120, 32)
        self.img_1_cor = carrega_imatge("imatges/1_cor.png", 120, 32)

        self.im = Image.open("imatges/cotxe.png")
        self.im = self.im.resize((60, 120), Image.NEAREST)

    def mou(self):
        self.x=self.x+self.v*math.sin(self.angle)
        self.y=self.y+self.v

    def show(self,w,screen):
        centre=screen.WorldToZoomXY(self.x+self.w/2,self.y+self.h/2)
        
        im_rotada = self.im.rotate(math.degrees(self.angle), expand=True)
        self.imatge = ImageTk.PhotoImage(im_rotada)
        w.create_image(centre.x, centre.y, image=self.imatge, anchor="center")
        
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
        if self.vides==2:
            w.create_image(x, y, image=self.img_2_cors, anchor="nw")
        if self.vides==1:
            w.create_image(x, y, image=self.img_1_cor, anchor="nw")
        if self.vides<1:
            self.mort=True
    
    def controls(self):
        if keyboard.is_pressed('left'):
            self.angle-=0.1
        if keyboard.is_pressed('right'):
            self.angle+=0.1
    
    def xoc_paret(self, joc):
        for paret in joc.parets:
            if paret.xoca_cotxe(self):
                self.mort = True

    def recompensa_agafada(self, joc):
        for rec in joc.recompenses:
            if rec.agafada(self, joc):
                break

    def xoc_obstacle(self, joc):
        for obs in joc.obstacles:
            if obs.colisio(self, joc):
                if self.toca_obstacle==False:
                    self.vides-=1
                    self.puntuacio=self.puntuacio-50
                    self.toca_obstacle=True
                    return
                else:
                    return   
        
        self.toca_obstacle=False
        
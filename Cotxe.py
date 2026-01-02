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

    def reset(self):
        self.toca_paret = False

    def mou(self):
        self.y=self.y+self.v

    def pinta(self,w,screen):
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
        
    def controls(self):
        if keyboard.is_pressed('left'):
            self.angle=self.angle+0.1
        if keyboard.is_pressed('right'):
            self.angle=self.angle-0.1
    
    def xoc_paret(self, wMin, wMax, screen, carretera):
        L1=LinearEquation(self.x, self.y, self.x, self.y+self.h)
        L2=LinearEquation(self.x, self.y, self.x+self.w, self.y)
        L3=LinearEquation(self.x+self.w, self.y, self.x+self.w, self.y+self.h)
        L4=LinearEquation(self.x, self.y+self.h, self.x+self.w, self.y+self.h)

        equacions_esquerra=carretera.equacions_rectes(wMin,wMax,screen)[0] #en teoria es de la mateixa classe que L1
        equacions_dreta=carretera.equacions_rectes(wMin,wMax,screen)[1]
        
        # for eq in equacions_esquerra:
        #     if L1.intersection(eq):
        #         self.toca_paret=True
        #         break
        #     if L2.intersection(eq):
        #         self.toca_paret=True
        #         break
        #     if L3.intersection(eq):
        #         self.toca_paret=True
        #         break
        #     if L4.intersection(eq):
        #         self.toca_paret=True
        #         break
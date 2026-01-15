from LinearEquation import *
from PIL import Image, ImageTk
import numpy as np
import math

def linesCollided(x1, y1, x2, y2, x3, y3, x4, y4):
    LA=LinearEquation(x1,y1,x2,y2)
    LB=LinearEquation(x3,y3,x4,y4)

    if (LA.intersection(LB)):
        if LA.m!=math.inf and LB.m!=math.inf:
            punt_tall=WPoint((LB.b-LA.b)/(LA.m-LB.m), (LB.m*LA.b-LA.m*LB.b)/(LB.m-LA.m))
        
            in_segment1 = (min(x1, x2) <= punt_tall.x <= max(x1, x2) and 
                        min(y1, y2) <= punt_tall.y <= max(y1, y2))
        
            in_segment2 = (min(x3, x4) <= punt_tall.x <= max(x3, x4) and 
                      min(y3, y4) <= punt_tall.y <= max(y3, y4))
        
            return in_segment1 and in_segment2
        else:
            if LA.m==math.inf:
                punt_tall=WPoint(LA.getX(1), LB.m*LA.getX(1)+LB.b)
                in_segment1 = (min(x1, x2) <= punt_tall.x <= max(x1, x2) and 
                        min(y1, y2) <= punt_tall.y <= max(y1, y2))
        
                in_segment2 = (min(x3, x4) <= punt_tall.x <= max(x3, x4) and 
                        min(y3, y4) <= punt_tall.y <= max(y3, y4))
        
                return in_segment1 and in_segment2
            if LB.m==math.inf:
                punt_tall=WPoint(LB.getX(1), LA.m*LB.getX(1)+LA.b)
                in_segment1 = (min(x1, x2) <= punt_tall.x <= max(x1, x2) and 
                        min(y1, y2) <= punt_tall.y <= max(y1, y2))
        
                in_segment2 = (min(x3, x4) <= punt_tall.x <= max(x3, x4) and 
                        min(y3, y4) <= punt_tall.y <= max(y3, y4))
        
                return in_segment1 and in_segment2
    return False

def carrega_imatge(nom, amplada, alçada):
    im = Image.open(nom)
    im = im.resize((amplada, alçada)) 
    img = ImageTk.PhotoImage(im)
    return img

#Rotem "angle" graus al voltant de l'eix del punt (x0,y0)
def rotar_respecte_x0_y0(x, y, angle, x0, y0):
    T=np.array([[1,0,-x0],[0,1,y0],[0,0,1]]) #Matriu de translació de (x0, y0) a l'origen
    T_inv=np.array([[1,0,x0],[0,1,-y0],[0,0,1]])
    R=np.array([[math.cos(angle),-math.sin(angle),0], [math.sin(angle), math.cos(angle), 0], [0,0,1]]) #Matriu de rotació
    inp=np.array([x,-y,1])
    m1=np.dot(T_inv, R)
    m2=np.dot(T,inp)
    return np.dot(m1,m2)

import json
from WPoint import *
from LinearEquation import *
from pantalla import *
from Cotxe import *
from funcions_adicionals import *

#Fer diccionari de ranges de la carretera
f=open("carretera.json","r")
carretera=json.load(f)
f.close()

g=open("recompenses.json","r")
recompenses=json.load(g)
g.close()

h=open("obstacles.json","r")
obstacles=json.load(h)
h.close()

i=open("metes.json","r")
metes=json.load(i)
i.close()

class Joc:
    def __init__(self, escenari, cotxes, screen):
        self.escenari=escenari
        self.meta=Meta(metes[escenari]['x'], metes[escenari]['y'], screen)
        
        self.parets=[]
        for tram in carretera[escenari].keys():
            self.parets.append(Paret(carretera[escenari][tram]['p1']['x'],carretera[escenari][tram]['p1']['y'],carretera[escenari][tram]['p3']['x'],carretera[escenari][tram]['p3']['y']))
            self.parets.append(Paret(carretera[escenari][tram]['p2']['x'],carretera[escenari][tram]['p2']['y'],carretera[escenari][tram]['p4']['x'],carretera[escenari][tram]['p4']['y']))

        self.cotxes=[]
        for c in cotxes:
            self.cotxes.append(c) # TO-DO: Canviar inicialització per fitxer .json

        self.recompenses=[]
        for compt in recompenses[escenari].keys():
            self.recompenses.append(Recompensa(recompenses[escenari][compt]['x'],recompenses[escenari][compt]['y'],
                                    recompenses[escenari][compt]['valor'], screen))
            
        self.obstacles=[]
        for obs in obstacles[escenari].keys():
            if obstacles[escenari][obs]["tipus"]=="senglar":
                self.obstacles.append(Porc(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], obstacles[escenari][obs]["direccio"], screen))

            if obstacles[escenari][obs]["tipus"]=="platan":
                self.obstacles.append(Plàtan(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], screen))

            if obstacles[escenari][obs]["tipus"]=="contenidor":
                self.obstacles.append(Contenidor(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], screen))

            if obstacles[escenari][obs]["tipus"]=="iaia":
                self.obstacles.append(Iaia(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], obstacles[escenari][obs]["direccio"], screen))

            if obstacles[escenari][obs]["tipus"]=="con":
                self.obstacles.append(Con(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], screen))

            if obstacles[escenari][obs]["tipus"]=="turista":
                self.obstacles.append(Turista(obstacles[escenari][obs]["x"], obstacles[escenari][obs]["y"], obstacles[escenari][obs]["direccio"], screen))

class Paret:
    def __init__(self, x0, y0, x1, y1): #(x0,y0) és el punt que està més amunt
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1

    def show(self, w1, w, screen): #self és la paret de l'esquerra. w1 és un objecte paret, i és la paret de la dreta
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

    def xoca_cotxe(self, cotxe):
        V1=WPoint(cotxe.x,cotxe.y)
        V2=WPoint(cotxe.x+cotxe.w*math.cos(cotxe.angle), cotxe.y-cotxe.w*math.sin(cotxe.angle))
        V4=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle))
        V3=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle)+cotxe.w*math.cos(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle)-cotxe.w*math.sin(cotxe.angle))
        
        vertexs_cotxe=[V1,V2,V3,V4]
        for i in range(0,4):
            j=i+1
            j=j%4
            if linesCollided(self.x0, self.y0, self.x1, self.y1, vertexs_cotxe[i].x, vertexs_cotxe[i].y, 
                             vertexs_cotxe[j].x, vertexs_cotxe[j].y):
                return True
        
        return False

class Recompensa:
    def __init__(self, x, y, valor, screen):
        self.x=x #(x,y) és el centre de la imatge
        self.y=y
        self.valor=valor
        self.amplada=screen.LongXZoomToWorld(32)
        self.alçada=screen.LongYZoomToWorld(32)

        self.img10=carrega_imatge("imatges/moneda_10.png", 32,32)
        self.img20=carrega_imatge("imatges/moneda_20.png", 32,32)
        self.img50=carrega_imatge("imatges/moneda_50.png", 32,32)

    def show(self, w, screen): 
        p=screen.WorldToZoomXY(self.x, self.y)

        if self.valor==10:
            w.create_image(p.x, p.y, image=self.img10, anchor="nw") #north west jeje

        if self.valor==20:
            w.create_image(p.x, p.y, image=self.img20, anchor="nw")

        if self.valor==50:
            w.create_image(p.x, p.y, image=self.img50, anchor="nw")

    def agafada(self, cotxe, joc):
        #TO-DO: Codi duplicat
        V1=WPoint(cotxe.x,cotxe.y)
        V2=WPoint(cotxe.x+cotxe.w*math.cos(cotxe.angle), cotxe.y-cotxe.w*math.sin(cotxe.angle))
        V4=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle))
        V3=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle)+cotxe.w*math.cos(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle)-cotxe.w*math.sin(cotxe.angle))
        vertexs_cotxe=[V1,V2,V3,V4]
        
        W1=WPoint(self.x,self.y)
        W2=WPoint(self.x+self.amplada,self.y)
        W4=WPoint(self.x,self.y+self.alçada)
        W3=WPoint(self.x+self.amplada,self.y+self.alçada)
        vertexs_recompensa=[W1,W2,W3,W4]
        
        for i in range(0,4):
            ii=i+1
            ii=ii%4
            for j in range(0,4):
                jj=j+1
                jj=jj%4
                if linesCollided(vertexs_cotxe[i].x, vertexs_cotxe[i].y, vertexs_cotxe[ii].x, vertexs_cotxe[ii].y,
                                 vertexs_recompensa[j].x, vertexs_recompensa[j].y, vertexs_recompensa[jj].x, vertexs_recompensa[jj].y):
                    cotxe.puntuacio+=self.valor
                    joc.recompenses.remove(self)
                    return True
                
        return False
    
class Obstacle:
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def show(self, w, imatge, screen):
        p=screen.WorldToZoomXY(self.x, self.y)
        w.create_image(p.x, p.y, image=imatge, anchor="nw")

    def colisio(self, cotxe, amplada, alçada, joc):
        #TO-DO: Codi duplicat
        #Vèrtexs del cotxe
        V1=WPoint(cotxe.x,cotxe.y)
        V2=WPoint(cotxe.x+cotxe.w*math.cos(cotxe.angle), cotxe.y-cotxe.w*math.sin(cotxe.angle))
        V4=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle))
        V3=WPoint(cotxe.x+cotxe.h*math.sin(cotxe.angle)+cotxe.w*math.cos(cotxe.angle), cotxe.y+cotxe.h*math.cos(cotxe.angle)-cotxe.w*math.sin(cotxe.angle))
        vertexs_cotxe=[V1,V2,V3,V4]
        
        #Vèrtexs de l'obstacle (TO-DO: OBSTACLE QUE NO GIRA)
        W1=WPoint(self.x,self.y)
        W2=WPoint(self.x+self.amplada,self.y)
        W4=WPoint(self.x,self.y+self.alçada)
        W3=WPoint(self.x+self.amplada,self.y+self.alçada)
        vertexs_recompensa=[W1,W2,W3,W4]

        #Comprovem si el cotxe està dins de l'obstacle. En cas afirmatiu, detectem col·lisió
        if max(W1.x, W4.x)<=min(V1.x, V4.x) and max(V2.x, V3.x)<=min(W2.x,W3.x) and max(W1.y, W2.y)<=min(V1.y, V2.y) and max(V3.y, V4.y)<=min(W3.y, W4.y):
            return True

        #Comprovem si l'obstacle està dins el cotxe. En cas afirmatiu, detectem col·lisió
        if max(V1.x, V4.x)<=min(W1.x, W4.x) and max(W2.x, W3.x)<=min(V2.x,V3.x) and max(V1.y, V2.y)<=min(W1.y, W2.y) and max(W3.y, W4.y)<=min(V3.y, V4.y):
            return True 
        
        for i in range(0,4):
            ii=i+1
            ii=ii%4
            for j in range(0,4):
                jj=j+1
                jj=jj%4
                if linesCollided(vertexs_cotxe[i].x, vertexs_cotxe[i].y, vertexs_cotxe[ii].x, vertexs_cotxe[ii].y,
                                 vertexs_recompensa[j].x, vertexs_recompensa[j].y, vertexs_recompensa[jj].x, vertexs_recompensa[jj].y):
                    return True
                
        return False
    
class Meta:
    def __init__(self, x, y, screen):
        self.x=x
        self.y=y

        self.amplada=screen.LongXZoomToWorld(400) 
        self.alçada=screen.LongYZoomToWorld(70)

        self.imatge=carrega_imatge("imatges/meta.png", 400, 70)

    def show(self, w, screen):
        p=screen.WorldToZoomXY(self.x, self.y)
        w.create_image(p.x, p.y, image=self.imatge, anchor="center")
    
class Porc(Obstacle):
    def __init__(self, x, y, direccio, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(80)#El que sigui
        self.alçada=screen.LongYZoomToWorld(60)

        if direccio==1:
            self.esquerra_dreta=True
            self.imatge=carrega_imatge("imatges/Porc_senglar_1.png", 80,60)
        else:
            self.esquerra_dreta=False
            self.imatge=carrega_imatge("imatges/Porc_senglar_2.png", 80,60)     

    def mou(self):
        if self.esquerra_dreta:
            self.x=self.x+0.5
        else:
            self.x=self.x-0.5
    
    def show(self, w, screen):
        super().show(w, self.imatge, screen)
        self.mou()
    
    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)

class Plàtan(Obstacle):
    def __init__(self, x, y, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(50) 
        self.alçada=screen.LongYZoomToWorld(45)

        self.imatge=carrega_imatge("imatges/plàtan.png", 50,45)

    def show(self, w, screen):
        super().show(w, self.imatge, screen)

    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)
    
class Contenidor(Obstacle):
    def __init__(self, x, y, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(80)#El que sigui
        self.alçada=screen.LongYZoomToWorld(70)

        self.imatge=carrega_imatge("imatges/contenidor.png", 80, 70)

    def show(self, w, screen):
        super().show(w, self.imatge, screen)

    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)
    
class Iaia(Obstacle):
    def __init__(self, x, y, direccio, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(75)#El que sigui
        self.alçada=screen.LongYZoomToWorld(97)

        if direccio==1:
            self.esquerra_dreta=True
            self.imatge=carrega_imatge("imatges/Iaia_1.png", 75,97)
        else:
            self.esquerra_dreta=False
            self.imatge=carrega_imatge("imatges/Iaia_2.png", 75,97)     

    def mou(self):
        if self.esquerra_dreta:
            self.x=self.x+0.25
        else:
            self.x=self.x-0.25
    
    def show(self, w, screen):
        super().show(w, self.imatge, screen)
        self.mou()
    
    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)
    
class Con(Obstacle):
    def __init__(self, x, y, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(60)#El que sigui
        self.alçada=screen.LongYZoomToWorld(75)

        self.imatge=carrega_imatge("imatges/con.png", 60, 75)

    def show(self, w, screen):
        super().show(w, self.imatge, screen)

    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)
    
class Turista(Obstacle):
    def __init__(self, x, y, direccio, screen):
        super().__init__(x, y)
        self.amplada=screen.LongXZoomToWorld(90)#El que sigui
        self.alçada=screen.LongYZoomToWorld(135)

        if direccio==1:
            self.esquerra_dreta=True
            self.imatge=carrega_imatge("imatges/Guiri_1.png", 90,135)
        else:
            self.esquerra_dreta=False
            self.imatge=carrega_imatge("imatges/Guiri_2.png", 90, 135)     

    def mou(self):
        if self.esquerra_dreta:
            self.x=self.x+0.4
        else:
            self.x=self.x-0.4
    
    def show(self, w, screen):
        super().show(w, self.imatge, screen)
        self.mou()
    
    def colisio(self, cotxe, joc):
        return super().colisio(cotxe, self.amplada, self.alçada, joc)

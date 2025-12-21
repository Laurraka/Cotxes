class Cotxe:
    def __init__(self,x,y,w,h,v=1):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.v=v
    def mou(self):
        self.x=self.x+self.v
    def pinta(self,w,screen):
        p1=screen.WorldToZoomXY(self.x,self.y)
        p2=screen.WorldToZoomXY(self.x+self.w,self.y+self.h)
        w.create_rectangle(p1.x,p1.y,p2.x,p2.y)
class Cotxe:
    def __init__(self,x,y,w,h,v=1):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.v=v
    def mou(self):
        self.x=self.x+self.v
    def pinta(self,w,wv):
        p1=wv.worldToViewXY(self.x,self.y)
        p2=wv.worldToViewXY(self.x+self.w,self.y+self.h)
        p3=wv.worldToViewXY(self.x+0.75*self.w, self.y)
        p4=wv.worldToViewXY( self.x+0.75*self.w, self.y+self.h)
        w.create_rectangle(p1.x,p1.y,p2.x,p2.y)
        w.create_line(p3.x,p3.y,p4.x,p4.y)
        '''w.create_rectangle(self.x,self.y,self.x+self.w,self.y+self.h)
        w.create_line(self.x+0.75*self.w, self.y, self.x+0.75*self.w, self.y+self.h)'''


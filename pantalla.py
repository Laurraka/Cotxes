from WPoint import *
from ZPoint import *

# --- Clase principal World ---

class Pantalla:
    """
    Gestiona la finestra de Pantalla (VX/VY) i la finestra del Món (WX/WY), 
    amb mètodes per transformar punts entre tots dos sistemes de coordenades.
    """

    def __init__(self, wMin, wMax, zMin, zMax):
        self.wMin = wMin
        self.wMax = wMax
        self.zMin = zMin
        self.zMax = zMax
       
    def __repr__(self) :
        s = f"World=({self.wMin.x},{self.wMin.y}) a ({self.wMax.x},{self.wMax.y}) "
        s += f"Zoom=({self.zMin.x},{self.zMin.y}) a ({self.zMax.x},{self.zMax.y})"
        return s

    # --- Transformacions -------------------

    #Transfromada World to Zoom (món a pantalla)
    def WorldToZoom(self, Wp: WPoint) -> ZPoint:

        # Evitar divisions per zero si el món/finestra té mida 0. Transformem punts a escala
        scale_x = (self.zMax.x - self.zMin.x) / (self.wMax.x - self.wMin.x) if (self.wMax.x - self.wMin.x) != 0 else 0.0
        scale_y = (self.zMax.y - self.zMin.y) / (self.wMax.y - self.wMin.y) if (self.wMax.y - self.wMin.y) != 0 else 0.0

        zx = int((Wp.x - self.wMin.x) * scale_x + self.zMin.x)
        zy = int((Wp.y- self.wMin.y) * scale_y + self.zMin.y)
        return ZPoint(zx, zy)

    def WorldToZoomXY(self, x: float, y: float) -> ZPoint:
        #Permet transformar a partir de 2 valors x,y en lloc d'un WPoint
   
        return self.WorldToZoom(WPoint(x, y))

     #Transfromada View to World (pantalla a món)
    def ZoomToWorld(self, Zp: ZPoint) -> WPoint: 

        denom_x = (self.zMax.x - self.zMin.x)
        denom_y = (self.zMax.y - self.zMin.y)

        wx = ((Zp.x - self.zMin.x) * (self.wMax.x - self.wMin.x) / denom_x) + self.wMin.x if denom_x != 0 else self.wMin.x
        wy = ((self.zMax.y - Zp.y - self.zMin.y) * (self.wMax.y - self.wMin.y) / denom_y) + self.wMin.y if denom_y != 0 else self.wMin.y

        return WPoint(wx, wy)

    def ZoomToWorldXY(self, x: int, y: int) -> WPoint:
        #Permet transformar a partir de 2 valors x,y en lloc d'un VPoint
        return self.ZoomToWorld(ZPoint(x, y))
    
    def LongXZoomToWorld(self, longX):
        scale_x = (self.wMax.x - self.wMin.x) / (self.zMax.x - self.zMin.x)
        return longX*scale_x

    def LongYZoomToWorld(self, longY):
        scale_y = (self.wMax.y - self.wMin.y) / (self.zMax.y - self.zMin.y)  
        return longY*scale_y 
    
    def TranslateWorld(self,dy):
        self.wMin.y+=dy
        self.wMax.y+=dy

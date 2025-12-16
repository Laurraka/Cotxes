from WPoint import *
from VPoint import *


# --- Clase principal World ---

class WorldView:
    """
    Gestiona la finestra de Pantalla (VX/VY) i la finestra del Món (WX/WY), 
    amb mètodes per transformar punts entre tots dos sistemes de coordenades.
    """

    def __init__(self, wMin, wMax, vMin, vMax):
        self.wMin = wMin
        self.wMax = wMax
        self.vMin = vMin
        self.vMax = vMax
       
    def __repr__(self) :
        s = f"World=({self.wMin.x},{self.wMin.y}) a ({self.wMax.x},{self.wMax.y}) "
        s += f"View=({self.vMin.x},{self.vMin.y}) a ({self.vMax.x},{self.vMax.y})"
        return s

    # --- Transformacions -------------------

    #Transfromada Word to View  (món a pantalla)
    def worldToView(self, Wp: WPoint) -> VPoint:
        wy = self.wMax.y - Wp.y
       
        # Evitar divisions per zero si el món/finestra té mida 0
        scale_x = (self.vMax.x - self.vMin.x) / (self.wMax.x - self.wMin.x) if (self.wMax.x - self.wMin.x) != 0 else 0.0
        scale_y = (self.vMax.y - self.vMin.y) / (self.wMax.y - self.wMin.y) if (self.wMax.y - self.wMin.y) != 0 else 0.0

        vx = int((Wp.x - self.wMin.x) * scale_x + self.vMin.x)
        vy = int(wy * scale_y + self.vMin.y)
        return VPoint(vx, vy)

    def worldToViewXY(self, x: float, y: float) -> VPoint:
        #Permet transformar a partir de 2 valors x,y en lloc d'un WPoint
        
        return self.worldToView(WPoint(x, y))

     #Transfromada View to World (pantalla a món)
    def viewToWorld(self, Vp: VPoint) -> WPoint:
        vy = self.vMax.y - Vp.y

        denom_x = (self.vMax.x - self.vMin.x)
        denom_y = (self.vMax.y - self.vMin.y)

        wx = ((Vp.x - self.vMin.x) * (self.wMax.x - self.wMin.x) / denom_x) + self.wMin.x if denom_x != 0 else self.wMin.x
        wy = ((vy - self.vMin.y) * (self.wMax.y - self.wMin.y) / denom_y) + self.wMin.y if denom_y != 0 else self.wMin.y

        return WPoint(wx, wy)

    def viewToWorldXY(self, x: int, y: int) -> WPoint:
        #Permet transformar a partir de 2 valors x,y en lloc d'un VPoint
        return self.viewToWorld(VPoint(x, y))
    
    def translateWindow(self,dx,dy):
        self.wMin.x+=dx
        self.wMax.x+=dx
        self.wMin.y+=dy
        self.wMax.y+=dy

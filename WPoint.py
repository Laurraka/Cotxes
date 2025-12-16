import math

class WPoint:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return f"({self.x},{self.y})"
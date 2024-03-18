from vector3 import Vec3

class Ray:
  def __init__(self, origin: Vec3, direction: Vec3):
    self.origin = origin
    self.direction = direction
  
  def getPoint(self, t):
    return self.origin + self.direction.scale(t)
  
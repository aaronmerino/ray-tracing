import math

class Vec3:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def length(self):
    a = self.x * self.x
    b = self.y * self.y
    c = self.z * self.z

    return math.sqrt(a + b + c)

  def scale(self, c):
    nx = self.x * c
    ny = self.y * c
    nz = self.z * c

    return Vec3(nx, ny, nz)

  def normalize(self):
    return self.scale(1/self.length())
    
  def add(self, a):
    nx = self.x + a.x
    ny = self.y + a.y
    nz = self.z + a.z

    return Vec3(nx, ny, nz)
  
  def subtract(self, a):
    nx = self.x - a.x
    ny = self.y - a.y
    nz = self.z - a.z

    return Vec3(nx, ny, nz)    
  
  def dot(self, a):
    return self.x * a.x + self.y * a.y + self.z * a.z
  
  def cross(self, a):
    cx = (self.y * a.z) - (self.z * a.y)
    cy = (self.z * a.x) - (self.x * a.z)
    cz = (self.x * a.y) - (self.y * a.x)

    return Vec3(cx, cy, cz)
  
  def __add__(self, a):
    if isinstance(a, Vec3):
      return self.add(a)
    else:
      raise TypeError("Must add two Vec3 objects")
    
  def __sub__(self, a):
    if isinstance(a, Vec3):
      return self.subtract(a)
    else:
      raise TypeError("Must subtract two Vec3 objects")
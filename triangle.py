from vector3 import Vec3
from color import Color
from ray import Ray
from surface import Surface

class Triangle(Surface):
  def __init__(self, color: Color, a: Vec3, b: Vec3, c: Vec3) -> None:
    super().__init__(color)

    self.a = a
    self.b = b
    self.c = c

  
  def hit(self, ray: Ray, t0: float, t1: float) -> tuple[bool, int, Vec3]:
    # cramer's rule
    a = self.a.x - self.b.x
    b = self.a.y - self.b.y
    c = self.a.z - self.b.z 

    d = self.a.x - self.c.x
    e = self.a.y - self.c.y
    f = self.a.z - self.c.z

    g = ray.direction.x
    h = ray.direction.y
    i = ray.direction.z

    j = self.a.x - ray.origin.x 
    k = self.a.y - ray.origin.y
    l = self.a.z - ray.origin.z

    M = a*(e*i - h*f) + b*(g*f - d*i) + c*(d*h - e*g)

    t = -1*(f*(a*k - j*b) + e*(j*c - a*l) + d*(b*l - k*c)) / M
    if ((t < t0) or (t > t1)):
      return False, -1, None
    
    G = (i*(a*k - j*b) + h*(j*c - a*l) + g*(b*l - k*c)) / M
    if ((G < 0) or (G > 1)):
      return False, -1, None

    B = (j*(e*i - h*f) + k*(g*f - d*i) + l*(d*h - e*g)) / M
    if ((B < 0) or (B + G) > 1):
      return False, -1, None
    
    n = ((self.b - self.a).cross((self.c - self.a))).normalize()
    return True, t, n
  
  






    

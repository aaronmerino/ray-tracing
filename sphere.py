from vector3 import Vec3
from color import Color
from ray import Ray
from surface import Surface
import math

class Sphere(Surface):
  def __init__(self, diffuse_color: Color, specular_color: Color, phong_exp: int, centre: Vec3, radius: int) -> None:
    super().__init__(diffuse_color, specular_color, phong_exp)

    self.centre = centre
    self.radius = radius

  
  def hit(self, ray: Ray, t0: float, t1: float) -> tuple[bool, int, Vec3]:
    c = self.centre
    e = ray.origin
    d = ray.direction
    r = self.radius

    # check discriminant
    disc =  (d.dot(e - c))**2 - (d.dot(d)) * ((e - c).dot(e - c) - r**2)

    if disc < 0:
      return False, -1, None
    elif disc > 0:
      # two solutions
      ta = ((d.scale(-1)).dot(e - c) - math.sqrt(disc))/d.dot(d)
      tb = ((d.scale(-1)).dot(e - c) + math.sqrt(disc))/d.dot(d)
      n1 = ((ray.getPoint(ta) - self.centre).scale(2)).normalize()
      n2 = ((ray.getPoint(tb) - self.centre).scale(2)).normalize()

      

      if ((ta < t0) or (ta > t1)):
        return False, -1, None
      else:
        return True, ta, n1
    else:
      # one solution
      ta = ((d.scale(-1)).dot(e - c))/d.dot(d)
      n1 = ((ray.getPoint(ta) - self.centre).scale(2)).normalize()
      return True, ta, n1 
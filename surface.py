from ray import Ray
from color import Color

class Surface:
  def __init__(self, diffuse_color: Color, specular_color: Color, phong_exp: int) -> None:
    self.diffuse_color = diffuse_color
    self.specular_color = specular_color
    self.phong_exp = phong_exp
  
  def hit(self, ray: Ray, t0: float, t1: float) -> bool:
    pass

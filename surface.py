from ray import Ray
from color import Color

class Surface:
  def __init__(self, color: Color) -> None:
    self.color = color
  
  def hit(self, ray: Ray, t0: float, t1: float) -> bool:
    pass

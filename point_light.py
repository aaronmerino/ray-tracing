from vector3 import Vec3
from color import Color
from light import Light


class PointLight(Light):
  def __init__(self, position: Vec3, color: Color) -> None:
    super().__init__(color)

    self.position = position
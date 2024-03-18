import math
from vector3 import Vec3
from ray import Ray


class Camera:

  def __init__(self, width: int, height: int, focal_length: float, view_point: Vec3, view_dir: Vec3):
    self.width = width
    self.height = height
    self.focal_length = focal_length
    self.view_point = view_point
    self.view_dir = view_dir

    up_vector = Vec3(0, 0, 1)

    self.w = (view_dir.scale(-1)).normalize()
    self.u = (up_vector.cross(self.w)).normalize()
    self.v = self.w.cross(self.u)


  def generate_view_ray(self, i: int, j: int) -> Ray:
    r = self.width // 2
    l = -r
    t = self.height // 2
    b = -t

    u = l + ((r-l)/self.width) * (i + 0.5)
    v = b + ((t-b)/self.height) * (j + 0.5)

    ray_direction = self.w.scale(-1*self.focal_length) + self.u.scale(u) + self.v.scale(v)

    return Ray(self.view_point, ray_direction)

from vector3 import Vec3
from ray import Ray
from camera import Camera
from surface import Surface
from triangle import Triangle
from sphere import Sphere
from color import Color
from point_light import PointLight
import math

from tkinter import Tk, Canvas, Frame, BOTH

WIDTH = 400
HEIGHT = 400
MAX_RENDER_DIST = 1000000

class Scene:
    def __init__(self, objects: list, lights: list, camera: Camera):
       self.objects = objects
       self.camera = camera
       self.lights = lights

    def render(self, canvas):
      for i in range(0, WIDTH):
        for j in range(0, HEIGHT):
          view_ray = self.camera.generate_view_ray(i, j)

          t1 = math.inf
          hit_obj = None
          normal = None
          pixel_color = None

          for o in self.objects:

            hit, t, n = o.hit(view_ray, 0, t1)

            if (hit):
              t1 = t
              hit_obj = o
              normal = n
          
          if (hit_obj is not None):
            ambient_light_intensity = Color(10, 45, 80).normalize()

            # default ambient color
            pixel_color = hit_obj.diffuse_color.normalize() * ambient_light_intensity

            # now go through each light source
            for light in self.lights:
              diff_coef = hit_obj.diffuse_color.normalize()

              light_intensitiy = light.color.normalize()

              hit_position = view_ray.getPoint(t1)

              light_direction = (light.position - hit_position).normalize()

              lambart = max(0, normal.dot(light_direction))

              lambart_intensity = Color(lambart, lambart, lambart)

              camera_direction = (view_ray.direction.normalize()).scale(-1)
              
              pixel_color += (diff_coef*light_intensitiy)*lambart_intensity


              spec_coef = hit_obj.specular_color.normalize()

              half_vector = (light_direction + camera_direction).normalize()

              phong = max(0, normal.dot(half_vector)) ** hit_obj.phong_exp

              phong_intensity = Color(phong, phong, phong)

              pixel_color += (spec_coef*light_intensitiy)*phong_intensity
          
          else:
            # default background color
            pixel_color = Color(10, 45, 80).normalize()
          
          # if (hit_obj is not None):
          #   # print((pixel_color.red, pixel_color.green, pixel_color.blue))

          # apply pixel_color to canvas at position (i, j)
          pixel_color_hex = "#%02x%02x%02x" % (int(min(pixel_color.red*255, 255)), int(min(pixel_color.green*255, 255)), int(min(pixel_color.blue*255, 255)))
          canvas.create_rectangle((i, j)*2, outline="", fill=pixel_color_hex)

            
if __name__ == "__main__":
  cam_pos = Vec3(0,-100,-50)
  cam_dir = Vec3(0,1,0.2)
  camera = Camera(WIDTH, HEIGHT, 400, cam_pos, cam_dir)

  scene_objects = []
  scene_objects.append(Sphere(Color(255, 120, 255), Color(100, 150, 450), 50, Vec3(0, 100, 0), 50))
  scene_objects.append(Sphere(Color(255, 120, 255), Color(150, 150, 150), 80, Vec3(-12, 60, -20), 10))
  scene_objects.append(Sphere(Color(255, 120, 255), Color(150, 150, 150), 80, Vec3(-12, 60, 20), 10))
  scene_objects.append(Sphere(Color(255, 120, 255), Color(150, 150, 150), 80, Vec3(12, 60, 20), 10))
  scene_objects.append(Sphere(Color(0, 0, 255), Color(150, 150, 150), 100, Vec3(-12, 80, 40), 10))

  scene_objects.append(Triangle(Color(255, 120, 50), Color(150, 150, 150), 100, Vec3(0, 60, -30), Vec3(40, 60, -20), Vec3(10, 60, 10)))
  scene_objects.append(Triangle(Color(255, 120, 50), Color(150, 150, 150), 100, Vec3(0, 60, -30), Vec3(40, 60, -20), Vec3(10, 60, 10)))
  scene_objects.append(Triangle(Color(255, 120, 50), Color(150, 150, 150), 100, Vec3(0, 60, -30), Vec3(10, 40, -50), Vec3(40, 60, -20)))

  scene_objects.append(Triangle(Color(50, 120, 250), Color(150, 150, 150), 100, Vec3(-50, 20, -80), Vec3(50, 20, -80), Vec3(-50, 200, -80)))
  scene_objects.append(Triangle(Color(50, 120, 250), Color(150, 150, 150), 100, Vec3(50, 20, -80), Vec3(50, 200, -80), Vec3(-50, 200, -80)))

  scene_objects.append(Triangle(Color(255, 120, 50), Color(150, 150, 150), 100, Vec3(-50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 20, 100)))
  scene_objects.append(Triangle(Color(255, 120, 50), Color(150, 150, 150), 100, Vec3(50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 200, 100)))

  scene_lights = []
  scene_lights.append(PointLight(Vec3(300, 10, 500), Color(455/2, 150/2, 55/2)))

  scene_lights.append(PointLight(Vec3(-300, 10, -200), Color(0, 250, 120)))


  scene = Scene(scene_objects, scene_lights, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT)
  canvas.pack(fill=BOTH, expand=1)

  scene.render(canvas)

  root.mainloop()


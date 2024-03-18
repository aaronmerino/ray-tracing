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
            ambient_light_intensity = Color(10, 25, 40).normalize()

            # default ambient color
            pixel_color = hit_obj.color.normalize() * ambient_light_intensity

            # now go through each light source
            for light in self.lights:
              diff_coef = hit_obj.color.normalize()
              light_intensitiy = light.color.normalize()

              hit_position = view_ray.getPoint(t1)

              light_direction = (light.position - hit_position).normalize()

              lambart = max(0, normal.dot(light_direction))

              lambart_intensity = Color(lambart, lambart, lambart)
              
              pixel_color += (diff_coef*light_intensitiy)*lambart_intensity
          
          else:
            # default background color
            pixel_color = Color(10, 25, 40).normalize()
          
          # if (hit_obj is not None):
          #   # print((pixel_color.red, pixel_color.green, pixel_color.blue))

          # apply pixel_color to canvas at position (i, j)
          pixel_color_hex = "#%02x%02x%02x" % (int(min(pixel_color.red*255, 255)), int(min(pixel_color.green*255, 255)), int(min(pixel_color.blue*255, 255)))
          canvas.create_rectangle((i, j)*2, outline="", fill=pixel_color_hex)

            
if __name__ == "__main__":
  cam_pos = Vec3(0,-300,-120)
  cam_dir = Vec3(0,1,0.5)
  camera = Camera(WIDTH, HEIGHT, 400, cam_pos, cam_dir)

  scene_objects = []
  scene_objects.append(Sphere(Color(255, 120, 255), Vec3(0, 100, 0), 50))
  scene_objects.append(Sphere(Color(255, 120, 255), Vec3(-12, 60, -20), 10))
  scene_objects.append(Sphere(Color(255, 120, 255), Vec3(-12, 60, 20), 10))
  scene_objects.append(Sphere(Color(255, 120, 255), Vec3(12, 60, 20), 10))
  scene_objects.append(Sphere(Color(255, 120, 255), Vec3(-12, 80, 40), 10))

  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(0, 60, -30), Vec3(40, 60, -20), Vec3(10, 60, 10)))
  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(0, 60, -30), Vec3(40, 60, -20), Vec3(10, 60, 10)))
  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(0, 60, -30), Vec3(10, 40, -50), Vec3(40, 60, -20)))

  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(-50, 20, -80), Vec3(50, 20, -80), Vec3(-50, 200, -80)))
  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(50, 20, -80), Vec3(50, 200, -80), Vec3(-50, 200, -80)))

  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(-50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 20, 100)))
  scene_objects.append(Triangle(Color(255, 120, 50), Vec3(50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 200, 100)))

  scene_lights = []
  scene_lights.append(PointLight(Vec3(300, 10, 500), Color(255, 255, 255)))

  scene_lights.append(PointLight(Vec3(-300, 10, -200), Color(0, 255, 255)))


  scene = Scene(scene_objects, scene_lights, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT)
  canvas.pack(fill=BOTH, expand=1)

  scene.render(canvas)

  root.mainloop()


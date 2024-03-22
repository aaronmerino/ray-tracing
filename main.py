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
MAX_RAY_BOUNCE = 20
MAX_RENDER_DIST = 1000000

class Scene:
    def __init__(self, objects: list, lights: list, camera: Camera):
       self.objects = objects
       self.camera = camera
       self.lights = lights

    def hit(self, ray, t0):
      t1 = math.inf
      hit_obj = None
      normal = None

      for o in self.objects:

        hit, t, n = o.hit(ray, t0, t1)

        if (hit):
          t1 = t
          hit_obj = o
          normal = n
      
      return t1, hit_obj, normal
    

    def render(self, canvas):
      for i in range(0, WIDTH):
        for j in range(0, HEIGHT):

          current_ray = self.camera.generate_view_ray(i, j)
          pixel_color = Color(0, 0, 0)
          current_spec = None
          ray_depth = 0

          while (ray_depth < MAX_RAY_BOUNCE):
            
            t1, hit_obj, normal = None, None, None

            if (ray_depth == 0):
              t1, hit_obj, normal = self.hit(current_ray, 0)
            else:
              t1, hit_obj, normal = self.hit(current_ray, 0.001)  

            if (hit_obj is not None):
              ambient_light_intensity = Color(20, 85, 120).normalize()

              # default ambient color
              pixel_color += hit_obj.diffuse_color.normalize() * ambient_light_intensity

              # now go through each light source
              for light in self.lights:
                # check if in shadow first:
                hit_position = current_ray.getPoint(t1)
                light_direction = (light.position - hit_position).normalize()

                ray_light = Ray(hit_position, light_direction)

                _, hit_shadow, _ = self.hit(ray_light, 0.001)
                if (hit_shadow is not None):
                  continue

                diff_coef = hit_obj.diffuse_color.normalize()

                light_intensitiy = light.color.normalize()

                lambart = max(0, normal.dot(light_direction))

                lambart_intensity = Color(lambart, lambart, lambart)

                camera_direction = (current_ray.direction.normalize()).scale(-1)
                
                pixel_color += (diff_coef*light_intensitiy)*lambart_intensity


                spec_coef = hit_obj.specular_color.normalize()

                half_vector = (light_direction + camera_direction).normalize()

                phong = max(0, normal.dot(half_vector)) ** hit_obj.phong_exp

                phong_intensity = Color(phong, phong, phong)

                
                if (ray_depth == 0):
                  pixel_color += (spec_coef*light_intensitiy)*phong_intensity
                else:
                  pixel_color += ((spec_coef*light_intensitiy)*phong_intensity)*current_spec


              reflection_dir = current_ray.direction - normal.scale(2*(current_ray.direction.dot(normal)))
              current_ray = Ray(current_ray.getPoint(t1), reflection_dir)
              current_spec = hit_obj.specular_color.normalize()
              ray_depth += 1
            else:
              # default background color
              pixel_color += Color(10, 45, 80).normalize()
              break


          # apply pixel_color to canvas at position (i, j)
          pixel_color_hex = "#%02x%02x%02x" % (int(min(pixel_color.red*255, 255)), int(min(pixel_color.green*255, 255)), int(min(pixel_color.blue*255, 255)))
          canvas.create_rectangle((i, j)*2, outline="", fill=pixel_color_hex)

            
if __name__ == "__main__":
  # cam_pos = Vec3(0,-100,-50)
  cam_pos = Vec3(220,20,100)
  cam_dir = Vec3(-1,0.4,-0.5)
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

  scene_objects.append(Triangle(Color(50, 120, 250), Color(150, 150, 150), 100, Vec3(-50, 20, -100), Vec3(50, 20, -100), Vec3(-50, 200, -100)))
  scene_objects.append(Triangle(Color(50, 120, 250), Color(150, 150, 150), 100, Vec3(50, 20, -100), Vec3(50, 200, -100), Vec3(-50, 200, -100)))

  scene_objects.append(Triangle(Color(50, 50, 50), Color(150, 150, 150), 100, Vec3(-50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 20, 100)))
  scene_objects.append(Triangle(Color(50, 50, 50), Color(150, 150, 150), 100, Vec3(50, 20, 100), Vec3(-50, 200, 100), Vec3(50, 200, 100)))

  scene_lights = []
  scene_lights.append(PointLight(Vec3(300, 10, 500), Color(455/2, 150/2, 55/2)))

  scene_lights.append(PointLight(Vec3(-200, 10, -200), Color(100, 250, 120)))

  # scene_objects.append(Sphere(Color(0, 0, 255), Color(150, 150, 150), 100, Vec3(150, 80, 60), 2))
  scene_lights.append(PointLight(Vec3(150, 80, 70), Color(400, 400, 100)))

  scene_lights.append(PointLight(Vec3(150, 10, 20), Color(200, 200, 100)))


  scene = Scene(scene_objects, scene_lights, camera)

  root = Tk()

  canvas = Canvas(root, width=WIDTH, height=HEIGHT)
  canvas.pack(fill=BOTH, expand=1)

  scene.render(canvas)

  root.mainloop()


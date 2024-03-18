class Color:
  def __init__(self, red: float, green: float, blue: float):
    self.red = min(red, 500)
    self.green = min(green, 500)
    self.blue = min(blue, 500)

  def normalize(self):
    max_value = 500

    if (max_value != 0):
      return Color(self.red / max_value, self.green / max_value, self.blue / max_value)
    else:
      return Color(self.red, self.green, self.blue)
    
  def add(self, a):
    nr = self.red + a.red
    ng = self.green + a.green
    nb = self.blue + a.blue

    return Color(nr, ng, nb)

  def multiply(self, a):
    nr = self.red * a.red
    ng = self.green * a.green
    nb = self.blue * a.blue

    return Color(nr, ng, nb)

  def __add__(self, a):
    if isinstance(a, Color):
      return self.add(a)
    else:
      raise TypeError("Must add two Color objects")
    
  def __mul__(self, a):
    if isinstance(a, Color):
      return self.multiply(a)
    else:
      raise TypeError("Must multiply two Color objects")
  
  def __str__(self):
    return f"Color: {self.red}, {self.green}, {self.blue}"
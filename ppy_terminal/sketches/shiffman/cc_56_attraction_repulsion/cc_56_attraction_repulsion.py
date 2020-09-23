
w = 500
h = 500

attractor = None
particles = []

class Particle:
  def __init__(self, x, y, r=5):
    self.pos = PVector(x, y)
    self.vel = PVector()
    self.vel_limit = 30
    self.acc = PVector()
    self.r = r
    self.c = color(255)

  def move(self):
    self.pos.add(self.vel)

    # limits
    if self.vel.mag() <= self.vel_limit:
      self.vel.add(self.acc)

    # handle x edges
    if self.pos.x > w+self.r:
      self.pos.x = -self.r
    elif self.pos.x < -self.r:
      self.pos.x = w+self.r

    # handle y edges
    if self.pos.y > h+self.r:
      self.pos.y = -self.r
    elif self.pos.y < -self.r:
      self.pos.y = h+self.r

  def render(self):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    point(self.pos.x, self.pos.y)
    popStyle()

  def attracted(self, target):
    direction = target.sub(self.pos)

def setup():
  size(w, h)
  background(0)
  frameRate(10)

  global attractor
  attractor = PVector(w/2, h/2)

  global particles
  for n in range(10):
    particles.append(Particle(random(w), random(h)))

def draw():

  #background(0)

  pushStyle()
  stroke(231, 76, 60)
  strokeWeight(10)
  point(attractor.x, attractor.y)
  popStyle()

  for p in particles:
    p.move()
    p.render()

  if frameCount % 20 == 0:
    print(frameCount)
  if frameCount % 200 == 0:
    exit()

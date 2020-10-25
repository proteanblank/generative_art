w = 500
h = 500
max_frames = 10000

attractor = None
particles = []

class Particle:
  def __init__(self, x, y, r=5):
    self.pos = PVector(x, y)
    self.vel = PVector()
    self.acc = PVector()
    self.vel_limit = 3000
    self.r = r
    self.c = color(100, 100, 100, 100)

  def move(self):
    self.pos.add(self.vel)

    # limits
    if self.vel.mag() <= self.vel_limit:
      self.vel.add(self.acc)

    """
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
    """

  def render(self):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    point(self.pos.x, self.pos.y)
    popStyle()

  def attracted(self, target):
    force = PVector.sub(target, self.pos)
    dsquared = force.magSq()
    dsquared = constrain(dsquared, 25, 100)
    G = 100
    strength = G / dsquared
    force.setMag(strength)
    self.acc = force

def setup():
  size(w, h)
  background(0)
  frameRate(10)

  global attractor
  attractor = PVector(w/2 + w*0.2*cos(0), h/2 + h*0.2*sin(0))

  global particles
  for n in range(10):
    particles.append(Particle(random(w), random(h)))

def draw():

  #background(0)

  pushStyle()
  stroke(231, 76, 60, 100)
  strokeWeight(10)
  attractor = PVector(w/2 + w*0.02*cos(frameCount*TAU/50), 
                      h/2 + h*0.02*sin(frameCount*TAU/50))
  #attractor.add(PVector(5*sin(frameCount*TAU/50), 5*cos(frameCount*TAU/50)))
  point(attractor.x, attractor.y)
  popStyle()

  for idx,p in enumerate(particles):
    p.attracted(attractor)
    p.move()
    p.render()

  if frameCount % 20 == 0:
    print(frameCount)
  if frameCount % max_frames == 0:
    exit()

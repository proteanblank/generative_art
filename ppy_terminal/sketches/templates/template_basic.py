def setup():
  global pg
  pg = createGraphics(1000, 1000)
  noLoop()

def draw():
  pg.beginDraw()
  pg.colorMode(HSB, 360, 100, 100, 100)
  pg.background(0, 0, 25)
  pg.stroke(60, 7, 86, 100)
  pg.noFill()

  for i in range(100):
    pg.ellipse(random(pg.width), random(pg.height), 100, 100)

  pg.endDraw()
  pg.save('image.png')
  exit()

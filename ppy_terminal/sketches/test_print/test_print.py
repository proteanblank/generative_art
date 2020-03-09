import sys
sys.path.append("/Users/apenne/Desktop/ppy")
import funfun

def setup(): 
    global pg
    pg = createGraphics(1000, 1000)
    noLoop()

def draw(): 
    pg.beginDraw()
    pg.background(102)
    pg.stroke(255)
    pg.line(pg.width*0.5, pg.height*0.5, pg.width, pg.height)
    funfun.editfun(pg)
    #for i in range(1000):
    #    pg.fill(random(255),50,50,10)
    #    pg.ellipse(random(pg.width),random(pg.height),random(pg.width*0.2),random(pg.height*0.2))
    pg.endDraw()
    pg.save('output.png')
    print(__file__)
    exit()

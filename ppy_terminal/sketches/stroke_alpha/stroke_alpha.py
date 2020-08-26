# Processing mode uses Python 2.7 but I prefer Python 3.x
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

# Normal Python imports
import os
import sys

# Bad way to make our "imports" dir available so we can import modules from it
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
from utilities import DrawUtils, OpsUtils, ConfigUtils
from setup_logging import log

args = {'seeded':False,
        'seed':1113388,
        'width':1080,
        'height':1080
        }

def setup():
  global pg
  pg = createGraphics(args['width'], args['height'])

  #  noLoop()

def draw():
  log.info('top')

  if args['seeded']:
      seed = int(random(0,9999999))
  else:
      seed = args['seed']
 
  # Instantiate primary drawing class
  du = DrawUtils(script_path=os.path.abspath(__file__),
                 width=args['width'],
                 height=args['height'],
                 seed=seed)
  log.info(frameCount)
  # Initialize random number generators with seed
  randomSeed(du.seed)
  noiseSeed(du.seed)

  pg.beginDraw()
  pg.colorMode(HSB, 360, 100, 100, 100)
  pg.background(0, 0, 25)
  pg.stroke(60, 7, 86, 100)
  pg.strokeWeight(50)
  pg.noFill()

  #pg.ellipse(random(pg.width), random(pg.height), random(pg.width), random(pg.height))
  pg.ellipse(100*frameCount, 100*frameCount,100*frameCount,100*frameCount)

  pg.endDraw()

 
  if frameCount == 3:
    du.save_graphic(pg, 'output', 0)
    exit()

  log.info('bottom')

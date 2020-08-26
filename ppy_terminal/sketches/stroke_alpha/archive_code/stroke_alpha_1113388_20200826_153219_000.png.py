# Processing mode uses Python 2.7 but I prefer Python 3.x
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

# Normal Python imports
import os
import sys
import shutil
from datetime import datetime

# Bad way to make our "imports" dir available so we can import modules from it
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
#from utilities import DrawUtils, OpsUtils, ConfigUtils  # moving utils into script itself to make code more portable
from setup_logging import log


def get_timestamp_string():
  timestamp = datetime.now()
  timestamp = timestamp.strftime('%Y%m%d_%H%M%S')
  return timestamp

def get_filename(counter):
  filename = '{}_{}_{}_{:03d}.png'.format(sketch_name, args['seed'], timestamp, counter)
  return filename

def make_dir(path):
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

def save_graphic(pg, path, counter):
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  pg.save(output_path)
  log.info('Saved to {}'.format(output_path))
  if counter == 0:
    make_dir('archive_code')
    src = script_path
    dst = os.path.join('archive_code',output_file + '.py')
    shutil.copy(src, dst)

def circle_point(cx, cy, rx, ry, a):
  """
  Translates polar coords to cartesian
  """
  x = cx + rx * cos(a)
  y = cy + ry * sin(a)
  return x, y

def noise_loop(a, r, min_val, max_val, x_c=0, y_c=0):
  """
  Samples 2D Perlin noise in a circle to make smooth noise loops
  Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
  """
  xoff = map(cos(a), -1, 1, x_c, x_c + 2*r)
  yoff = map(sin(a), -1, 1, y_c, y_c + 2*r)
  r = noise(xoff, yoff)
  return map(r, 0, 1, min_val, max_val)

def frange(start, end=None, increment=None):
  """
  Adapted from http://code.activestate.com/recipes/66472
  """
  if end == None:
    end = start + 0.0
    start = 0.0
  if increment == None:
    increment = 1.0
  L = []
  while 1:
    next = start + len(L) * increment
    if increment > 0 and next >= end:
      break
    elif increment < 0 and next <= end:
      break
    L.append(next)
  return L

##### Globals
timestamp = get_timestamp_string()
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
sketch_name = os.path.splitext(script_name)[0]


##### Knobs
args = {'seeded':False,
        'seed':1113388,
        'width':1080,
        'height':1080
        }


if args['seeded']:
    args['seed'] = int(random(0,9999999))

# Initialize random number generators with seed
randomSeed(args['seed'])
noiseSeed(args['seed'])

def setup():
  global pg
  pg = createGraphics(args['width'], args['height'])
  pg.beginDraw()
  pg.colorMode(HSB, 360, 100, 100, 100)
  pg.background(0, 0, 25)
  pg.stroke(60, 7, 86, 30)
  pg.strokeWeight(50)
  pg.endDraw()
  #  noLoop()

def draw():

  pg.beginDraw()
  pg.noFill()


  pg.beginShape()
  angles = frange(0, TAU, TAU/5)
  x_c = random(100)
  y_c = random(100)

  for a in angles+angles[:3]:
    r = noise_loop(a, 10, 0, args['width']*0.6, x_c, y_c)
    x, y = circle_point(args['width']/2, args['height']/2, r, r, a)
    pg.curveVertex(x,y)
  pg.endShape()
  
  pg.endDraw()

 
  if frameCount == 4:
    save_graphic(pg, 'output', 0)
    exit()


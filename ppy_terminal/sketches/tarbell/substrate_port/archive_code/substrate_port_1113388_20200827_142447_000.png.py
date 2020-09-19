################################################################################
# code and images by Aaron Penne
# https://github.com/aaronpenne
#
# released under MIT License (https://opensource.org/licenses/MIT)
################################################################################


################################################################################
# Imports
################################################################################

# Processing mode uses Python 2.7 but I prefer Python 3.x, pull in future tools
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

# Normal Python imports
import os
import sys
import shutil
import logging
from datetime import datetime
from collections import OrderedDict

################################################################################
# Helper methods
#
# These exist here in the script instead of a separate centralized file to
# preserve portability and ability to recreate image with a single script
################################################################################

# Standardizes 
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)

def get_timestamp_string():
  """
  Standardizes timestamp string format ex. 20200631_123055
  """
  return datetime.now().strftime('%Y%m%d_%H%M%S')

def get_filename(counter):
  """
  Standardizes filename string format ex. comet_12345_20200631_123055_001.png
  """
  return '{}_{}_{}_{:03d}.png'.format(sketch_name, args['seed'], timestamp, counter)

def make_dir(path):
  """
  Creates dir if it doesn't exist
  """
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

def save_graphic(pg, path, counter):
  """
  Saves image
  """
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  pg.save(output_path)
  log.info('Saved to {}'.format(output_path))

  # If first run through draw() then save copy of this script
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

  Effectively places a circle on a 2D perlin noise field. Circle has radius r, and
  center at (x_c,y_c). Point on the edge of the circle is selected at angle a, the 
  noise value at that point is grabbed and mapped between min_val and max_val
  """
  xoff = map(cos(a), -1, 1, x_c, x_c + 2*r)
  yoff = map(sin(a), -1, 1, y_c, y_c + 2*r)
  r = noise(xoff, yoff)
  return map(r, 0, 1, min_val, max_val)

def frange(start, end=None, increment=None):
  """
  Allows range() with floats. Adapted from http://code.activestate.com/recipes/66472
  """
  if end == None:
    end = start + 0.0
    start = 0.0
  if increment == None:
    increment = 1.0
  range_list = []
  while 1:
    next = start + len(range_list) * increment
    if increment > 0 and next >= end:
      break
    elif increment < 0 and next <= end:
      break
    range_list.append(next)
  return range_list

def color_tuple(c, color_space='HSB', round_off=True):
  """
  Takes color datatype and color_space (HSB or RGB) to return tuple of color components.
  Useful for describing or parsing human readable colors
  """
  if color_space == 'HSB':
    c_tuple = (hue(c), saturation(c), brightness(c), alpha(c))
  if color_space == 'RGB':
    c_tuple = (red(c), green(c), blue(c), alpha(c))

  if round_off:
    c_tuple = (round(c_tuple[0]), round(c_tuple[1]), round(c_tuple[2]), round(c_tuple[3]))

  return c_tuple


################################################################################
# Global Variables
################################################################################

timestamp = get_timestamp_string()
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
sketch_name = os.path.splitext(script_name)[0]


##### Knobs
args = {'seeded':False,
        'seed':1113388,
        'width':1080,
        'height':1080,
        'alpha':30,
        'maxpal':100,
        'numpal':0
        }
good_color = []

colors = [
          #(0, 0, 0, args['alpha']), #black
          (180, 100, 100, args['alpha']), #cyan
          (300, 100, 100, args['alpha']), #magenta
          (60, 100, 100, args['alpha']), #yellow
          ]


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
  pg.background(60, 7, 95)
  pg.blendMode(MULTIPLY)
  pg.endDraw()
  noLoop()

def draw():
  global good_color

  fc = (frameCount - 1) % len(colors)
  log.info('fc = {}'.format(fc))

  pg.beginDraw()
  pg.noFill()


  pg.beginShape()
  angles = frange(0, TAU, TAU/6)
  x_c = random(100)
  y_c = random(100)
  
  pg.stroke(colors[fc][0], colors[fc][1], colors[fc][2], args['alpha'])
  #pg.stroke(180, 100, 100, 50)
  pg.strokeWeight(60)

  for a in angles+angles[:3]:
    r = noise_loop(a, 100, 0, args['width']*0.7, x_c, y_c)
    x, y = circle_point(args['width']/2, args['height']/2, r, r, a)
    pg.curveVertex(x,y)
  pg.endShape()
  
  pg.endDraw()

  def extract_colors(filename):
    img = loadImage(filename)
    img.loadPixels()

    for i,c in enumerate(img.pixels):
      if color_tuple(c) not in [color_tuple(gc) for gc in good_color]:
        good_color.append(c)
        args['numpal'] += 1
      if args['numpal'] == args['maxpal']:
        break

  log.info('begin extraction')
  extract_colors('flowersA.jpg')
  log.info('end extraction')
  out = createGraphics(10, 10)
  out.beginDraw()
  i = 0
  out.strokeWeight(1)
  for x in range(10):
    for y in range(10):
      out.stroke(good_color[i])
      out.point(x,y)
      i += 1
  out.endDraw()
  sorted(good_color)
  for x in good_color:
    print(color_tuple(x))
  save_graphic(out, 'outputx', 0) 

  if frameCount == 3*len(colors):
    save_graphic(pg, 'output', 0)
    exit()


################################################################################
# porting Jared Tarbell's Happy Place to Python Processing
# all credit for the algorithm goes to them
#
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
from random import seed, shuffle, sample

################################################################################
# Globals
################################################################################

# Knobs to turn
w = 1080
h = 1080
use_rand_seed = False
rand_seed = 123456789

good_colors = []

# Utility variables
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
script_ext = os.path.splitext(script_name)[1]
sketch_name = os.path.splitext(script_name)[0]

# Initialize random number generators with seed
if use_rand_seed:
    rand_seed = int(random(99999,9999999))
randomSeed(rand_seed)
noiseSeed(rand_seed)
seed(rand_seed)

################################################################################
# Helper methods
#
# These exist here in the script instead of a separate centralized file to
# preserve portability and ability to recreate image with a single script
################################################################################

# Standardizes log formats 
# ex. 2020-06-31 12:30:55 - INFO - log is better than print
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
log = logging.getLogger(__name__)


def get_filename(counter):
  """Standardizes filename string format 

  ex. comet_12345_20200631_123055_001.png
  """
  return '{}_{}_{}_{:03d}.png'.format(sketch_name, rand_seed, timestamp, counter)

def make_dir(path):
  """Creates dir if it does not exist"""
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

def save_graphic(pg, path, counter):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  pg.save(output_path)
  log.info('Saved to {}'.format(output_path))

  # If first run through draw() then save copy of this script to enable easy reproduction
  if counter == 0:
    make_dir('archive_code')
    src = script_path
    dst = os.path.join('archive_code', output_file + script_ext)
    shutil.copy(src, dst)

def circle_point(cx, cy, rx, ry, a):
  """Translates polar coords to cartesian"""
  x = cx + rx * cos(a)
  y = cy + ry * sin(a)
  return x, y

def noise_loop(a, r, min_val, max_val, x_c=0, y_c=0):
  """Samples 2D Perlin noise in a circle to make smooth noise loops

  Effectively places a circle on a 2D perlin noise field. Circle has radius r, and
  center at (x_c,y_c). Point on the edge of the circle is selected at angle a, the 
  noise value at that point is grabbed and mapped between min_val and max_val
  
  Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
  """
  xoff = map(cos(a), -1, 1, x_c, x_c + 2*r)
  yoff = map(sin(a), -1, 1, y_c, y_c + 2*r)
  r = noise(xoff, yoff)
  return map(r, 0, 1, min_val, max_val)


def frange(min_val, max_val=None, increment=None):
  """Allows range() with floats

  Adapted from http://code.activestate.com/recipes/66472
  """
  if max_val == None:
    max_val = min_val + 0.0
    min_val = 0.0
  if increment == None:
    increment = 1.0
  range_list = []
  while 1:
    next = min_val + len(range_list) * increment
    if increment > 0 and next >= max_val:
      break
    elif increment < 0 and next <= max_val:
      break
    range_list.append(next)
  return range_list


def color_tuple(c, color_space='HSB', rounded=True):
  """Takes color (Processing datatype) and returns human readable tuple."""
  if color_space == 'HSB':
    c_tuple = (hue(c), saturation(c), brightness(c), alpha(c))
  if color_space == 'RGB':
    c_tuple = (red(c), green(c), blue(c), alpha(c))

  if rounded:
    c_tuple = (round(c_tuple[0]), round(c_tuple[1]), round(c_tuple[2]), round(c_tuple[3]))

  return c_tuple


def extract_colors(img_filename, max_colors=100, randomize=True):
  """Extracts unique pixels from a source image to create a color palette. 

  If randomize=False then the image is sampled left to right, then top to bottom. 
  """
  colors_list = []

  img = loadImage(img_filename)
  img.loadPixels()

  if randomize:
    shuffle(img.pixels)

  num_colors = 0
  for i,c in enumerate(img.pixels):
    # only grab new colors (no repeats)
    if color_tuple(c) not in [color_tuple(gc) for gc in colors_list]:
      colors_list.append(c)
      num_colors += 1
    if num_colors == max_colors:
      break

  return colors_list


def sort_color_hues(colors_list, sort_on='hsb'):
  """Takes list of colors (Processing datatype) and sorts the list on hue"""
  colors_tuples = [color_tuple(c) for c in colors_list]
  if sort_on == 'hsb':
    colors = sorted(zip(colors_tuples, colors_list), key=lambda x: (x[0][0], x[0][1], x[0][2]))
  if sort_on == 'bsh':
    colors = sorted(zip(colors_tuples, colors_list), key=lambda x: (x[0][2], x[0][1], x[0][0]))
  return [c for _,c in colors]
  


################################################################################
# Setup
################################################################################

def setup():
  global pg
  size(w,h)
  pg = createGraphics(w, h)
  pg.beginDraw()
  pg.colorMode(HSB, 360, 100, 100, 100)
  pg.background(60, 7, 95)
  pg.blendMode(MULTIPLY)
  pg.endDraw()

  noLoop()


################################################################################
# Draw
################################################################################

def draw():

  global good_colors

  good_colors = extract_colors('flowersA.jpg')

  good_colors = sort_color_hues(good_colors)

  colors_tuples = [color_tuple(c) for c in good_colors]
  for c in colors_tuples:
    print(c)

  out = createGraphics(10, 10)
  out.beginDraw()
  out.strokeWeight(1)
  i = 0
  for x in range(10):
    for y in range(10):
      out.stroke(good_colors[i])
      out.point(x,y)
      i += 1
  out.endDraw()
  
  save_graphic(out, 'output', 0) 


  exit()


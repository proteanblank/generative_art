################################################################################
# code and images by Aaron Penne
# https://github.com/aaronpenne
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
max_frames = 10000

attractor = None
particles = []

use_seed = True
rand_seed = 578919

img_filename = 'input/scribbles.png'
numpal = 512 # number of colors in palette
good_colors = []

# Utility variables
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
script_path = os.path.abspath(__file__)
script_name = os.path.basename(script_path)
script_ext = os.path.splitext(script_name)[1]
sketch_name = os.path.splitext(script_name)[0]

# Initialize random number generators with seed
if not use_seed:
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

def make_dir(path):
  """Creates dir if it does not exist"""
  try:
    os.makedirs(path)
  except OSError:
    if not os.path.isdir(path):
      raise

def get_filename(counter):
  """Standardizes filename string format 
  ex. comet_12345_20200631_123055_001.png
  """
  return '{}_{}_{}_{:03d}.png'.format(sketch_name, rand_seed, timestamp, counter)

def save_graphic(pg=None, path='output', counter=0):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  if pg:
    pg.save(output_path)
  else:
    save(output_path)
  log.info('Saved to {}'.format(output_path))


def save_code(pg=None, path='output', counter=0):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  make_dir('archive_code')
  src = script_path
  dst = os.path.join('archive_code', output_file + script_ext)
  shutil.copy(src, dst)

def mousePressed():
  save_graphic(None, 'output', frameCount)

def some_color():
  return good_colors[int(random(numpal))]

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

  # for i in range(int(max_colors*0.1)):
  #   colors_list.append(color(0, 0, 0))
  for i in range(int(max_colors*0.1)):
    colors_list.append(color(0, 0, 100))

  return colors_list


################################################################################
# Artwork methods
#
# where the fun actually starts
################################################################################

class Particle:
  def __init__(self, x, y, r=5):
    self.pos = PVector(x, y)
    self.vel = PVector(random(-5,5), random(-5,5))
    self.acc = PVector()
    self.vel_limit = 3000
    self.r = r
    self.c = some_color()
    self.c = color(hue(self.c), saturation(self.c), brightness(self.c), 20)
    if random(100)>90:
      self.c = color(0, 0, 0, 20)
    if random(100)>95:
      self.c = color(0, 0, 100, 20)

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

  def render_points(self):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    point(self.pos.x, self.pos.y)
    popStyle()

  def render_lines(self, target):
    pushStyle()
    stroke(self.c)
    strokeWeight(self.r)
    line(self.pos.x, self.pos.y, target.x, target.y)
    popStyle()

  def attracted(self, target):
    force = PVector.sub(target, self.pos)
    dsquared = force.magSq()
    dsquared = constrain(dsquared, 25, 100)
    G = 0.01
    strength = 0.1 # G / dsquared
    force.setMag(strength)
    self.acc = force



################################################################################
# Setup
################################################################################

def setup():
  size(w, h)
  colorMode(HSB, 360, 100, 100, 100)
  background(44, 6, 97)
  #frameRate(30)

  global good_colors
  good_colors = extract_colors(img_filename, numpal)

  global particles
  for n in range(10):
    #particles.append(Particle(random(w), random(h)))
    particles.append(Particle(w/2+random(-2,2), 
                              h/2+random(-2,2),
                              1))

  save_code(None, 'output', frameCount)


################################################################################
# Draw
################################################################################

def draw():

  #background(0)

  pushStyle()
  stroke(231, 76, 60, 100)
  strokeWeight(10)
  
  global attractor

  # circle attractor
  attractor = PVector(w/2 + 100*cos(frameCount*TAU/w/2), 
                      h/2 + 100*sin(frameCount*TAU/h/2))

  # sin attractor
  #attractor = PVector(frameCount, h/2 + h*0.1 * sin(frameCount*TAU/h*10))

  #point(attractor.x, attractor.y)
  popStyle()

  for idx,p in enumerate(particles):
    p.attracted(attractor)
    p.move()
    #p.render_points()
    if idx>0:
      p.render_lines(particles[idx-1].pos)
    #p.render_lines(attractor)

  if frameCount % 20 == 0:
    print('{} - {} fps'.format(frameCount, frameRate))
  if frameCount % w == 0:
    save_graphic(None, 'output', frameCount)
    #filter(BLUR, 2)    
  if frameCount % max_frames == 0:
    exit()

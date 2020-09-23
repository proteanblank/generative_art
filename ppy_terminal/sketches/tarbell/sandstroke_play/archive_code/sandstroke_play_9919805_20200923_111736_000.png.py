################################################################################
# porting Jared Tarbell's sand painter to Python Processing
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
w = 800
h = 800
use_seed = False
rand_seed = 578919
img_filename = 'input/flowersA.jpg'
num = 2 # number of friends
numpal = 512 # number of colors in palette
good_colors = []
friends = []

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


def save_code(pg=None, path='output', counter=0):
  """Saves image and creates copy of this script"""
  make_dir(path)
  output_file = get_filename(counter)
  output_path = os.path.join(path, output_file)
  make_dir('archive_code')
  src = script_path
  dst = os.path.join('archive_code', output_file + script_ext)
  shutil.copy(src, dst)

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


def sort_color_hues(colors_list, sort_on='hsb'):
  """Takes list of colors (Processing datatype) and sorts the list on hue"""
  colors_tuples = [color_tuple(c) for c in colors_list]
  if sort_on == 'hsb':
    colors = sorted(zip(colors_tuples, colors_list), key=lambda x: (x[0][0], x[0][1], x[0][2]))
  if sort_on == 'bsh':
    colors = sorted(zip(colors_tuples, colors_list), key=lambda x: (x[0][2], x[0][1], x[0][0]))
  return [c for _,c in colors]


def some_color():
  return good_colors[int(random(numpal))]


def reset_all():

  global friends

  # connect in a circle
  for i in range(num):
    fx = w/2 + 0.4*w*cos(TAU*i/num)
    fy = h/2 + 0.4*h*sin(TAU*i/num)
    friends.append(Friend(fx, fy, i))

  # connect in a grid
#  pad_pct = 0.1
#  i = 0
#  num_steps = 18
#  x_min = int(w*pad_pct)
#  x_max = int(w*(1-pad_pct))
#  x_step = int((x_max - x_min)/num_steps)
#  y_min = int(h*pad_pct)
#  y_max = int(h*(1-pad_pct))
#  y_step = int((y_max - y_min)/num_steps)
#  for x in range(x_min, x_max+x_step, x_step):
#    for y in range(y_min, y_max+y_step, y_step):
#      friends.append(Friend(x, y, i))
#      i += 1
#  global num
#  num = i
#
  for i in range(int(num*2.2)):
    a = int(floor(random(num)))
    b = int(floor(a+random(22))%num)
    if (b >= num) or (b < 0):
      b = 0
      print('+')
    if a != b:
      friends[a].connect_to(b)
      friends[b].connect_to(a)
      print('{} made friends with {}'.format(a,b))

################################################################################
# Setup
################################################################################

def setup():
  size(w, h)
  
  colorMode(HSB, 360, 100, 100, 100)
  #colorMode(HSB)
  strokeWeight(1.5)

  global good_colors
  good_colors = extract_colors(img_filename, numpal)

  background(0, 0, 100)
  frameRate(10)

  reset_all()

  save_code(None, 'output', frameCount)
  #noLoop()




################################################################################
# Draw
################################################################################

def draw():


  p1 = PVector(0, h/2)
  p2 = PVector(w/2, 0)

  p1.add(PVector(frameCount, frameCount))
  p2.add(PVector(frameCount, frameCount))

  pushStyle()
  strokeWeight(10)
  stroke(100, 50, 20)
  s = SandPainter()
  s.render(p1.x, p1.y, p2.x, p2.y)
  popStyle()

  pushStyle()
  strokeWeight(20)
  stroke(50, 50, 60)
  point(p1.x, p1.y)
  point(p2.x, p2.y)
  popStyle()

  if frameCount % 200 == 0:
    save_graphic(None, 'output', frameCount)

  if frameCount % 20 == 0:
    print(frameCount, frameRate)

  #exit()


def mousePressed():
  save_graphic(None, 'output', frameCount)


class Friend:
  def __init__(self, x=0, y=0, identifier=0):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
   
    self.id = identifier
   
    self.numcon = 0
    self.maxcon = 10
    self.lencon = 10+int(random(w*0.03))  
    self.connections = [0 for i in range(self.maxcon)]
  
    self.myc = some_color()
    self.myc = color(hue(self.myc), saturation(self.myc), brightness(self.myc), 5)
    self.h = hue(self.myc)
    self.s = saturation(self.myc)
    self.b = brightness(self.myc)
    self.numsands = 1
    self.sands = [SandPainter() for i in range(self.numsands)]

  def connect_to(self, f):
    if (self.numcon < self.maxcon):
      if not self.friend_of(f):
        self.connections[self.numcon] = f
        self.numcon += 1

  def friend_of(self, f):
    #FIXME possibly replace with simple is in?
    is_friend = False
    for i in range(self.numcon):
      if self.connections[i] == f:
        is_friend = True
    return is_friend

  def draw_lines(self):
    stroke(self.h, self.s, self.b, 70)
    for i in range(self.numcon):
      ox = friends[self.connections[i]].x
      oy = friends[self.connections[i]].y
      line(self.x, self.y, ox, oy)

  def expose(self):
    for dx in range(-2,3):
      a = 0.4-abs(dx)/5
      stroke(0, 0, 0, 100*a)
      point(self.x+dx, self.y)
      stroke(0, 0, 100, 100*a)
      point(self.x+dx-1, self.y-1)
    for dy in range(-2,3):
      a = 0.4-abs(dy)/5
      stroke(0, 0, 0, 100*a)
      point(self.x, self.y+dy)
      stroke(0, 0, 100, 100*a)
      point(self.x-1, self.y+dy-1)

  def expose_connections(self):
    stroke(self.myc)
    for i in range(self.numcon):
      ox = friends[self.connections[i]].x
      oy = friends[self.connections[i]].y

      #line(self.x, self.y, ox, oy)
      for s in range(self.numsands):
        self.sands[s].render(self.x, self.y, ox, oy)

  def find_happy_place(self):
    self.vx += random(-w*0.001, w*0.001)
    self.vy += random(-h*0.001, h*0.001)

  def move(self):
    self.x += self.vx
    self.y += self.vy

    self.vx *= 0.97
    self.vy *= 0.97

class SandPainter:
  def __init__(self):
    self.p = random(1)
    self.c = some_color()
    self.h = hue(self.c) 
    self.s = saturation(self.c)
    self.b = brightness(self.c)
    self.g = random(0.01, 0.1)

  def render(self, x, y, ox, oy):
    pushStyle()
    strokeWeight(20)
    stroke(self.h, 100, 80, 100)
    point((x+ox)/2, (y+oy)/2)
    #point(ox + (x-ox)*sin(self.p), oy+(y-oy)*sin(self.p))
    popStyle()

    self.g += random(-0.5, 0.5)
    maxg = 0.22
    if (self.g < -maxg):
      self.g = -maxg
    if (self.g > maxg):
      self.g = maxg

    stroke(self.h, self.s, self.b, 10) #*a
    for i in range(5):
      amt = noise((x+y)+(frameCount*0.02))
      line((x+ox)/2, (y+oy)/2, lerp(x, (x+ox)/2, amt), lerp(y, (y+oy)/2, amt))
      line((x+ox)/2, (y+oy)/2, lerp(ox, (x+ox)/2, amt), lerp(oy, (y+oy)/2, amt))

#     w = self.g/10
#     for i in range(11):
#       a = 0.1 - i/110
#       stroke(self.h, self.s, self.b, 100) #*a
#       point(ox+(x-ox)*sin(self.p+sin(i*w)), oy+(y-oy)*sin(self.p+sin(i*w)))
#       point(ox+(x-ox)*sin(self.p-sin(i*w)), oy+(y-oy)*sin(self.p-sin(i*w)))
# 

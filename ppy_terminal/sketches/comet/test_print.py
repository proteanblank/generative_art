################################################################################
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################


# Processing mode uses Python 2.7 but I prefer Python 3.x
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

# Normal Python imports
import os
import sys
import random

# Bad way to make our "imports" dir available so we can import modules from it
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
from utilities import DrawUtils, OpsUtils, ConfigUtils
from setup_logging import log

# argparse doesn't work with command line processing, using config files instead
args = ConfigUtils().config_to_dict('config')

# Instantiate primary drawing class
du = DrawUtils(script_path=os.path.abspath(__file__),
               width=args['width'], 
               height=args['height'], 
               seed=args['seed'])


# Initialize random number generators with seed
randomSeed(du.seed)
noiseSeed(du.seed)
random.seed(du.seed)

def setup(): 
    global pg
    pg = createGraphics(du.width, du.height)

    noLoop()

def draw(): 
    pg.beginDraw()
    pg.colorMode(HSB, 360, 100, 100, 100)
    pg.translate(pg.width/2, pg.height/2)

    pg.background(0, 0, 25)
    pg.stroke(60, 7, 86)
    pg.strokeWeight(1)
    pg.noFill()
    
    angles = du.frange(0, TAU, TAU/100)
    angles.extend(angles[0:3])

    for i in range(0, int(pg.width/3)):
        pg.beginShape()
        for a in angles:
            r = du.noise_loop(a, i/10.0, i*4, (pg.width*0.05)+i*4, 0, 0)
            x, y = du.circle_point(pg.width*0.15, pg.height*0.15, r, r, a)
            pg.curveVertex(x, y)
        pg.endShape()

    pg.endDraw()
    du.save_graphic(pg, 'output', frameCount)
    exit()

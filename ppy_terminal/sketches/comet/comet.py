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
#import random

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
#random.seed(du.seed)

def setup():

    # The graphics buffer which will become the final image
    global pg
    pg = createGraphics(du.width, du.height)

    # Only run draw() function once
    noLoop()

def draw(): 

    # beginDraw() starts writing to buffer graphic buffer, must be first call on the graphic
    pg.beginDraw()

    # sets color mode and max values for Hue, Saturation, Brightness, Alpha
    pg.colorMode(HSB, 360, 100, 100, 100)

    # sets colors
    pg.background(0, 0, 25)
    pg.stroke(60, 7, 86, 100)
    pg.strokeWeight(4)
    pg.noFill()
   
    # gets every point around a circle in given step
    num_angles = 100
    angles = du.frange(0, TAU, TAU/num_angles)

    # if using curveVertex, need to add 3 points to complete circle
    angles.extend(angles[0:3])

    for i in range(0, 400, 1):

        # Uncomment these 2 lines for wacky mod based effects
        #pg.stroke(60, 7, 86, map(i%50,0,50,100,0))
        #pg.strokeWeight(map(i,0,1000,50,1))

        pg.beginShape()
        for a in angles:
            r = du.noise_loop(a, i/40.0, i*10, (pg.width*0.05)+i*10, 0, 0)
            x, y = du.circle_point(pg.width*0.62, pg.height*0.62, r, r, a)
            pg.curveVertex(x, y)
        pg.endShape()

    pg.endDraw()

    # save buffer to image 
    du.save_graphic(pg, 'output', frameCount)

    # close Processing
    exit()

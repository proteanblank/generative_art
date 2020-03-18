
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

print(du.seed)
du.seed = 4

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
    pg.background(250)
    
    du.draw_test(pg, args['num_circles'])
     
    pg.endDraw()
    du.save_graphic(pg, 'output', frameCount)
    exit()

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

# Bad way to make our "imports" dir available so we can import modules from it
# Need to point to your location
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
from utilities import DrawUtils, OpsUtils
from setup_logging import log

# Setup parameters/arguments to be used everywhere 
args = {'width': 1080,
        'height': 1080,
        'seed': 11381138}
        
def setup():
    
    global out
    out = createGraphics(args['width'], args['height'])

    # Only run draw() function once
    noLoop()

def draw(): 

    if 'seed' in args:
        seed = args['seed']
    else:
        seed = int(random(0,9999999))

    # Instantiate primary drawing class
    du = DrawUtils(script_path=os.path.abspath(__file__),
                   width=args['width'], 
                   height=args['height'], 
                   seed=seed)
    
    # Initialize random number generators with seed
    randomSeed(du.seed)
    noiseSeed(du.seed)


    out.beginDraw()
    out.colorMode(HSB, 360, 100, 100, 100)
    out.background(out.color(39, 17, 93))
    out.fill(0, 0, 25)
    out.stroke(0, 0, 25)

    prev_line_img = createGraphics(args['width'], args['height'])
    for step in [10, 7, 4]:
        line_img = du.line_canvas(bg_color=(39, 17, 93),
                                  fill_color=(0, 0, 25),
                                  stroke_color=(0, 0, 25),
                                  step=step)
        mask_img = du.mask_ellipse()
        line_img.mask(mask_img)
        out.image(line_img, 0, 0)

    out.endDraw()

    du.save_graphic(out, 'output', 0)

    # close Processing
    exit()

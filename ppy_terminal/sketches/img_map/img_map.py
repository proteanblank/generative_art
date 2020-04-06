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

def setup():

    global ima
    ima = createGraphics(du.width, du.height)

    global imb
    imb = createGraphics(du.width, du.height)

    global imc
    imc_file = du.get_ext_agnostic_file('input', args['imc'])
    imc = loadImage(imc_file)
    imc.resize(du.width, du.height)
    du.save_graphic(imc, 'output', 3)

    global out
    out = createGraphics(du.width, du.height)
    out.beginDraw()
    out.endDraw()

    # Only run draw() function once
    noLoop()

def draw(): 

    ima.beginDraw()
    ima.colorMode(HSB, 360, 100, 100, 100)
    ima.rectMode(CENTER)
    ima.background(0, 0, 100)
    ima.noStroke()
    x_min = du.width * 0.2
    x_max = du.width * 0.8
    y_min = du.height * 0.2
    y_max = du.height * 0.8
    for i in range(args['num_objs_ima']):
        x = random(x_min, x_max)
        y = random(y_min, y_max)
        w = random(du.width * 0.3)
        h = random(du.height * 0.3)
        for j in range(int(random(1,args['num_folds_ima']))):
            ima.fill(0, 0, random(100))
            ima.ellipse(x, y, w-j*du.width*0.01, h-j*du.height*0.01)
    ima.filter(BLUR, 30)
    ima.endDraw()

    du.save_graphic(ima, 'output', 1)


    imb.beginDraw()
    imb.colorMode(HSB, 360, 100, 100, 100)
    imb.rectMode(CENTER)
    imb.background(0, 0, 100)
    imb.noStroke()
    x_min = du.width * 0.2
    x_max = du.width * 0.8
    y_min = du.height * 0.2
    y_max = du.height * 0.8
    for i in range(args['num_objs_imb']):
        x = random(x_min, x_max)
        y = random(y_min, y_max)
        w = random(du.width * 0.3)
        h = random(du.height * 0.3)
        for j in range(int(random(1,args['num_folds_imb']))):
            imb.fill(0, 0, random(100))
            imb.rect(x, y, w-j*du.width*0.02, h-j*du.width*0.02)
    imb.filter(BLUR, 30)
    imb.endDraw()

    du.save_graphic(imb, 'output', 2)

    ima.loadPixels()
    imb.loadPixels()
    imc.loadPixels()
    out.loadPixels()
    out.beginDraw()
    out.colorMode(HSB, 360, 100, 100, 100)
    m = [(brightness(x)+brightness(y))/2 for x,y in zip(ima.pixels, imb.pixels)]
    for i,n in enumerate(m):
        index = floor(map(n, 0, 255, 0, len(m)-1))
        out.pixels[i] = imc.pixels[index]
        if n > 253 or n < 3:
            out.pixels[i] = out.color(0, 0, 100)
    out.updatePixels()

    du.save_graphic(out, 'output', 0)

    # close Processing
    exit()


# Processing mode uses Python 2.7 but I prefer Python 3.x
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import with_statement

import os
import sys
import argparse

# Very bad way to get the "imports" dir available so we can import modules from it
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
from utilities import Utilities
from setup_logging import log

# Use the terminal to change params, helpful to stub out for later automation
description = 'Tests printing straight to file without rendering, test bed for bringing in normal python tricks like argparse'
parser = argparse.ArgumentParser()
parser.add_argument('--seed', default=1138,
                    help='random seed used for python and processing random and noise implementations')
parser.add_argument('--width', default=4000,
                    help='width in pixels of output image')
parser.add_argument('--height', default=4000,
                    help='height in pixels of output image')
args = parser.parse_args()

u = Utilities(rand_seed=args.seed)

u.print_seed()

log.info('test')
log.info(args.seed)
log.info(args.width)
log.info(args.height)

def setup(): 
    global pg
    pg = createGraphics(4000, 4000)
    noLoop()

def draw(): 
    pg.beginDraw()
    pg.background(250)
    
#   util.draw_test(pg)
    
    pg.endDraw()
    pg.save('output.png')
    print(__file__)
    exit()

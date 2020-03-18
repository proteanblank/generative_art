
# Processing mode uses Python 2.7 but I prefer Python 3.x
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

# Very bad way to get the "imports" dir available so we can import modules from it
sys.path.insert(0, '/Users/apenne/github.com/generative_art/ppy_terminal/imports')
from utilities import Utilities
from setup_logging import log

u = Utilities()

u.print_seed()

log.info('test')

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

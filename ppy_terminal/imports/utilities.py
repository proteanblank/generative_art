
################################################################################
# Helper and utility functions
# 
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################

import os
import logging
import sys

# from datetime import timezone

from setup_logging import log

class Utilities():
    def __init__(self, rand_seed=1138):
        self.rand_seed = rand_seed

    def print_seed(self):
        log.info(self.rand_seed)

def draw_test(pg): 
    for i in range(1000):
        pg.fill(random(255),50,50,10)
        pg.ellipse(random(pg.width),random(pg.height),random(pg.width*0.2),random(pg.height*0.2))

def get_timestamp_string():
    timestamp = datetime.now(timezone.utc)
    return timestamp.strftime('%Y%m%d_%H%M%S')

# FIXME Replace with smarter dir creation if necessary and split .py and pg.save and counter as arg, etc
def save_image(pg, filename, timestamp=True, output_dir='output'):
    '''
    Saves each frame with a structured filename to allow for tracking all output
    '''
    if timestamp==True:
        timestamp = get_timestamp_string()
    
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(filename, timestamp, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def circle_point(cx, cy, rx, ry, a):
    '''
    Translates polar coords to cartesian
    '''
    x = cx + rx * cos(a)
    y = cy + ry * sin(a)
    return x, y
    
def noise_loop(a, r, min_val, max_val, x_c, y_c):
    '''
    Samples 2D Perlin noise in a circle to make smooth noise loops
    Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
    '''
    xoff = map(cos(a), -1, 1, x_c, x_c + 2*r);
    yoff = map(sin(a), -1, 1, y_c, y_c + 2*r);
    r = noise(xoff, yoff)
    return map(r, 0, 1, this.min, this.max);


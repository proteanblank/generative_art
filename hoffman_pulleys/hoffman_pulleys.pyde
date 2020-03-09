##########################################################################
# Code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# Released under the MIT license (https://opensource.org/licenses/MIT)
##########################################################################

import datetime
from random import shuffle, seed, choice, randint

w = 800
h = 800

record = False
animate = False
seeded = False

rand_seed = 1138


##########################################################################
# Global variables - no need to touch
##########################################################################

# Gets filename of this script
filename = __file__[:-5]

# Gets current YYMMDD_HHMMSS timestamp (e.g. 20160530_065530)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    

##########################################################################
# Setup
##########################################################################
def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h)

    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(2)  # 1 for low, 2 for high

    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()

    # Sets random seed value for both Python and Processing
    global rand_seed
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        # Only applies to the random() Processing function
        randomSeed(rand_seed)
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
    else:
        rand_seed = randint(0, 2000000)
        seed(rand_seed)
        randomSeed(rand_seed)
        noiseSeed(rand_seed)

    # Set the number of frames per second to display
    frameRate(30)

    # Keeps text centered vertically and horizontally at (x,y) coords
    textMode(CENTER)
    textAlign(CENTER, CENTER)

    rectMode(CENTER)

    # Sets color space and max values
    colorMode(HSB, 360, 100, 100, 100)


##########################################################################
# Draw
##########################################################################
def draw():




    if record:
        save_frame_timestamp(filename, timestamp)
    if not animate:
        save_frame_timestamp(filename, timestamp)

    if height > 1000 or width > 1000:
        import sys
        exit()
        sys.exit()

##########################################################################
# Sketch functions
##########################################################################

                
##########################################################################
# Helper and utility functions (used across multiple sketches)
##########################################################################
def keyPressed():
    pass
    
    
def mousePressed():
    save_frame_timestamp(filename, timestamp)
    

def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''
    Saves each frame with a structured filename to allow for tracking all output
    '''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(
        output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)

def circle_point(cx, cy, rx, ry, a):
    '''
    Translates polar coords to cartesian
    '''
    x = cx + rx * cos(a) / 2
    y = cy + ry * sin(a) / 2
    return x, y

def noise_loop(a, r, min_val, max_val, x_c, y_c):
    '''
    Samples 2D Perlin noise in a circle to make smooth noise loops
    Adapted from https://github.com/CodingTrain/website/blob/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/P5/noiseLoop.js
    '''
    xoff = map(cos(a), -1, 1, x_c, x_c + 2 * r)
    yoff = map(sin(a), -1, 1, y_c, y_c + 2 * r)
    r = noise(xoff, yoff)
    return map(r, 0, 1, this.min, this.max)

def frange(start, end=None, inc=None):
    '''
    http://code.activestate.com/recipes/66472/
    '''
    if end == None:
        end = start + 0.0
        start = 0.0
    if inc == None:
        inc = 1.0
    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
    return L

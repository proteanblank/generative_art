################################################################################
# code and images by Aaron Penne
# https://github.com/aaronpenne/generative_art
#
# released under the MIT license (https://opensource.org/licenses/MIT)
################################################################################

# Standard Python imports
import datetime
from random import shuffle, seed


################################################################################
# Global variables - knobs to turn
################################################################################

# Logic controls
record = True  # Save every frame?
animate = False  # Loop through draw()? 
seeded = False  # Set random seeds?

# Canvas size
w = 800  # width
h = 800  # height

# Initializes randomness to make results repeateable (if randomize is set to True)
rand_seed = 1138

noise_increment = 0.02

################################################################################
# Global variables - color
################################################################################
color_background = (0, 0, 100)
color_foreground = (0, 0, 25)
color_stroke = (0, 0, 25)

################################################################################
# Global variables - no need to touch
################################################################################

# Gets filename of this script
filename = __file__[:-5]

# Gets current YYMMDD_HHMMSS timestamp (e.g. 20160530_065530)
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


# The setup() function is part of Processing, it gets called one time when this file is run
def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h)
    
    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high
    
    # Sets color space to Hue Saturation Brightness with max values of HSB respectively
    colorMode(HSB, 360, 100, 100, 100)
        
    # Set the number of frames per second to display
    frameRate(60)
    
    # Keeps text centered vertically and horizontally at (x,y) coords
    textMode(CENTER)
    textAlign(CENTER, CENTER)
    
    # Stops draw() from running in an infinite loop
    if not animate:
        noLoop()
        
    # Sets random seed value for both Python and Processing 
    if seeded:
        seed(rand_seed)       # Only applies to the random Python module
        randomSeed(rand_seed) # Only applies to the random() Processing function
        noiseSeed(rand_seed)  # Only applies to the noise() Processing function
    
    # Initializes colors for the first frame
    background(*color_background)
    stroke(*color_foreground)
    fill(*color_foreground)
    noStroke()
    
# The draw() function is part of Processing, it gets called in an infinite loop every frame
def draw():
    background(*color_background)
    fill(*color_background)

    xoff = 0
    for x in frange(w/5, 4*w/5, 1):
        yoff = 0
        for y in frange(h/5, 4*w/5, 1):
            noise_value = noise(xoff, yoff)
            alpha_value = map(noise_value, 0, 1, 0, 100)
            if alpha_value>50:
                fill(0, 0, 0, 100)
            else:
                fill(0, 0, 0, 0)
            ellipse(x, y, 2, 2)
            yoff += noise_increment
        xoff += noise_increment
        
        
    xoff = 0
    for x in frange(w/5, 4*w/5, 1):
        yoff = 0
        for y in frange(h/5, 4*w/5, 1):
            noise_value = noise(xoff+100, yoff+100)
            alpha_value = map(noise_value, 0, 1, 0, 100)
            if alpha_value>50:
                fill(0, 50, 50, 100)
            else:
                fill(0, 50, 50, 0)
            ellipse(x, y, 2, 2)
            yoff += noise_increment
        xoff += noise_increment
    
    if record:
        save_frame_timestamp(filename, timestamp)

def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def mousePressed():
    save_frame_timestamp(filename, timestamp)
    
def frange(start, end=None, inc=None):
    # http://code.activestate.com/recipes/66472/
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

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

################################################################################
# Global variables - color
################################################################################
color_background = (0, 0, 100)
color_foreground = (0, 0, 25)
color_stroke = (0, 0, 25)
pal = [(348.7, 50.4, 94.9),  # bright salmon
       (306.6, 40.8, 96.1), # bright pink
       (45.7, 78.8, 94.1),  # yellow
       (16.3, 28.6, 96.1),  # salmon
       (358.7, 75.6, 94.9), # red
       (0, 0, 25), # black
]

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

    draw_blob_slice(0.007, 50, pal[5])
    draw_blob_slice(0.007, 50, pal[4], 0.25)
    draw_blob_slice(0.007, 50, pal[3], 0.5)
    draw_blob_slice(0.007, 50, pal[2], 0.75)
    draw_blob_slice(0.007, 50, pal[1], 1)
    draw_blob_slice(0.007, 50, pal[0], 1.25)
    
    if record:
        save_frame_timestamp(filename, timestamp)


def draw_blob_slice(noise_increment=0.02, threshold=50, fill_color=(0,0,0), offset=0, step=0.5, radius=1):
    fill_color = color(*fill_color)
    xoff = 0
    for x in frange(w/5, 4*w/5, step):
        yoff = 0
        for y in frange(h/5, 4*w/5, step):
            noise_value = noise(xoff+offset, yoff+offset)
            alpha_value = map(noise_value, 0, 1, 0, 100)
            if alpha_value>threshold:
                fill(fill_color, 100)
            else:
                fill(fill_color, 0)
            ellipse(x, y, radius, radius)
            yoff += noise_increment
        xoff += noise_increment
        
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

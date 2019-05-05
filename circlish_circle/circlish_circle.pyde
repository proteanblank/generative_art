################################################################################
# Adapted from the incredible Daniel Shiffman
# https://natureofcode.com/book/chapter-6-autonomous-agents/
# https://www.youtube.com/watch?v=BjoM9oKOAKY&t=1326s
################################################################################


import datetime
from random import shuffle, seed


################################################################################
# Global variables
################################################################################

# Get time 
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set random seed value for both Python 'random' and Processing 'random'
rand_seed = 1138
print(rand_seed)
# Comment out seeds below to get new shape on every run
seed(rand_seed) # This only applys to the Python random functions
randomSeed(rand_seed) # This only applys to the Processing random functions


################################################################################
# Knobs to turn
################################################################################

filename = 'circlish_circle'

record = False
animate = True
animate_mode = 'sinusoid'

# Canvas size
w = 800  # width
h = 800  # height

steps = 800
num_loops = 1

frame_rate = 20

inc = 0.01
scl = 20
cols = floor(w/scl)
rows = floor(h/scl)
    
step = TAU/steps
t1 = 0
t2 = 1000
t3 = 10000
t4 = 100000
t5 = 1000000
t6 = 10000000

def setup():
    # Sets size of canvas in pixels (must be first line)
    size(w, h) # (width, height)
    
    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high
    
    # Sets color space to Hue Saturation Brightness with max values of HSB respectively
    colorMode(HSB, 360, 100, 100, 100)
        
    # Set the number of frames per second to display
    frameRate(frame_rate)

    # Stops draw() from running in an infinite loop (should be last line)
    if not animate:
        noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit) 

    background(0, 0, 25)
    stroke(60, 7, 86)
    fill(0, 0, 25, 0)
    
def draw():
    global t1
    global t2
    global t3
    global t4
    global t5
    global t6
    
    t1 = t1 + 0.01;
    t2 = t2 + 0.01;
    t3 = t3 + 0.01;
    t4 = t4 + 0.01;
    t5 = t5 + 0.01;
    t6 = t6 + 0.01;
  
    if frameCount > (steps * num_loops):
        exit()
    
    w_n = map(noise(t1), 0, 1, 0, w*0.3)
    h_n = map(noise(t2), 0, 1, 0, h*0.3)
    x, y = circle_point(w/2, h/2, w*0.4, frameCount*step)
    ellipse(x, y, w_n, h_n)
    
    if frameCount % 2 == 0:
        w_n = map(noise(t3), 0, 1, 0, w*0.2)
        h_n = map(noise(t4), 0, 1, 0, h*0.2)
        x, y = circle_point(w/2, h/2, w*0.25, frameCount*step)
        ellipse(x, y, w_n, h_n)
                    
    if frameCount % 3 == 0:
        w_n = map(noise(t5), 0, 1, 0, w*0.1)
        h_n = map(noise(t6), 0, 1, 0, h*0.1)
        x, y = circle_point(w/2, h/2, w*0.1, frameCount*step)
        ellipse(x, y, w_n, h_n)
        
    if record:
        save_frame_timestamp(filename, timestamp)

        
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.png'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)
    
def circle_point(cx, cy, r, a):
    x = cx + r * cos(a)
    y = cy + r * sin(a)
    return x, y

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

filename = 'geode'

record = False
animate = True
animate_mode = 'sinusoid'

# Canvas size
w = 800  # width
h = 800  # height

steps = 1000
num_loops = 1

frame_rate = 80

inc = 0.01
scl = 20
cols = floor(w/scl)
rows = floor(h/scl)
    
step = TAU/steps
t1 = 0
t2 = 1000
t3 = 100000

c_start = w/5
c_stop = 4*w/5
num_geodes = 1

c_points = [radians(x) for x in range(1, 361, 5)]
print(c_points)

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

    # background(0, 0, 25)
    # stroke(60, 7, 86)
    background(60, 7, 86)
    stroke(0, 0, 25)
    
def draw():

    # fill(0, 0, 25, 100)
    fill(60, 7, 86)
    
    global t1
    global t2
    global c_start
    global c_stop
    global num_geodes
    
    t1 = t1 + 0.012
    t2 = t2 + 0.02
    
    x_c = (frameCount) + c_start
    y_c = h/2 - 100 + map(noise(t2), 0, 1, -50, 50)
    
    r = h*0.03*sin(map(x_c, c_start, c_stop, 0, num_geodes*PI))
    
    if r>h*0.03:
        r = h*0.03
    
    if x_c > c_stop:
        noLoop()
        save_frame_timestamp(filename, timestamp)
    
    max_noise = 12
    
    # if (num_geodes == 1) & (x_c > w/2):
    #     y_c = y_c + 150
    # else:
        # draw_blob(x_c, y_c, r, t1, 1, max_noise)
    
    draw_blob(x_c, y_c, r, t1, 1, max_noise)
    
    
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

def draw_blob(x_c, y_c, r, n_start=0, min_noise=1, max_noise=2):    
    beginShape()
              
    # First 3 points of each blob line are explicitly set because 
    # they are needed at the end of the shape to close the loop
    a = c_points[0]
    n = map(noise(n_start, a), 0, 1, min_noise, max_noise)
    x0, y0 = circle_point(x_c, y_c, n*r, a)
    curveVertex(x0, y0)
    
    a = c_points[1]
    n = map(noise(n_start, a), 0, 1, min_noise, max_noise)
    x1, y1 = circle_point(x_c, y_c, n*r, a)
    curveVertex(x1, y1)
    
    a = c_points[2]
    n = map(noise(n_start, a), 0, 1, min_noise, max_noise)
    x2, y2 = circle_point(x_c, y_c, n*r, a)
    curveVertex(x2, y2)
    
    for i,a in enumerate(c_points):
        # Limiting which points get vertices makes the "floor"
        if i>=3:
            n = map(noise(n_start, a), 0, 1, min_noise, max_noise)
            x, y = circle_point(x_c, y_c, n*r, a)
            curveVertex(x, y)

    # The three first points are laid out again to smoothly close the loop
    curveVertex(x0, y0)
    curveVertex(x1, y1)
    curveVertex(x2, y2)
    
    
    endShape()
    

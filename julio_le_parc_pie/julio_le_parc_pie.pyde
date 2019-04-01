
import datetime
import helper
from random import shuffle, seed


################################################################################
# Global variables
################################################################################

# Get time 
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Set random seed value for both Python 'random' and Processing 'random'
rand_seed = helper.get_seed('circle')
print(rand_seed)
# Comment out seeds below to get new shape on every run
seed(rand_seed) # This only applys to the Python random functions
randomSeed(rand_seed) # This only applys to the Processing random functions


################################################################################
# Knobs to turn
################################################################################

animate = True

# Canvas size
w = 1000  # width
h = 1000  # height

pad = 2

x_spots = 10
y_spots = 10

frame_rate = 10

c_tan = (41, 13, 97) #f8eed9
c_red = (351, 95, 77) #c40926
c_blue = (245, 90, 59) #1b0f96



w_pad = w*0.15
h_pad = h*0.15

x_min = w_pad
x_max = w - w_pad
x_rad = (x_max - x_min)/10

y_min = h_pad
y_max = h - h_pad
y_rad = (y_max - y_min)/10

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

    
def draw():
    background(*c_tan)
    noStroke()
    
    up_start = (3*TAU/8) + sin(frameCount*TAU/100)
    up_stop = (7*TAU/8) - sin(frameCount*TAU/50)
    down_start = (3*TAU/8 - PI) + sin(frameCount*TAU/50)
    down_stop = (7*TAU/8 - PI) - sin(frameCount*TAU/100)

    # Set up first row
    top = [x/10.0 for x in range(10+1)]
    btm = [x/10.0 for x in range(10+1)]
    btm.reverse()
    
    print(top, btm)
    
    big = []
    for i in range(10+1):
        small = []
        for j in range(10+1):
            small.append(lerp(top[i], btm[i], j/10.0))
        print(small)
        big.append(small)

    
    for i_x in range(10+1):
        x = lerp(x_min, x_max, i_x/10.0)
        
        for i_y in range(10+1):
            y = lerp(y_min, y_max, i_y/10.0)
            
            pct = lerp(top[i_x], btm[i_x], i_y/10.0)
            draw_pies(x, y, pct, up_start, up_stop, down_start, down_stop)
            
    if not animate:
        save_frame_timestamp('parc_pie', timestamp)
    
def draw_pies(x, y, pct, up_start, up_stop, down_start, down_stop):
    d = pct * TAU/4
    fill(*c_blue)
    arc(x, y, x_rad, y_rad, up_start+d, up_stop-d, PIE)
    
    d = (1-pct) * TAU/4
    fill(*c_red)
    arc(x, y, x_rad, y_rad, down_start+d, down_stop-d, PIE)

    
def save_frame_timestamp(filename, timestamp='', output_dir='output'):
    '''Saves each frame with a structured filename to allow for tracking all output'''
    filename = filename.replace('\\', '')
    filename = filename.replace('/', '')
    output_filename = os.path.join(output_dir, '{}_{}_{}_####.tif'.format(timestamp, filename, rand_seed))
    saveFrame(output_filename)
    print(output_filename)

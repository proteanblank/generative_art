##########################################################################
# Aaron Penne
# https://github.com/aaronpenne
##########################################################################

import datetime
import string
import sys
from random import shuffle, seed

import helper
import bug_palette

##########################################################################
# Global variables
##########################################################################

random_seed = 0

# Get time
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Parameters for draw speed
frame_rate = 1

##########################################################################
# Knobs to turn
##########################################################################

# Canvas size
w = 2000  # width
h = 2000  # height

pal = bug_palette.pal        
            
            
##########################################################################
# setup()
# function gets run once at start of program
##########################################################################

def setup():

    # Sets size of canvas in pixels (must be first line)
    size(w, h)

    # Sets resolution dynamically (affects resolution of saved image)
    pixelDensity(displayDensity())  # 1 for low, 2 for high

    # Sets color space to Hue Saturation Brightness with max values of HSB
    # respectively
    colorMode(HSB, 360, 100, 100, 100)

    # Set the number of frames per second to display
    frameRate(frame_rate)

    background(0, 0, 100)

    rectMode(CORNER)

    # Stops draw() from running in an infinite loop (should be last line)
    #noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit)


##########################################################################
# draw()
##########################################################################

def draw():
    global random_seed
    random_seed = int(frameCount*second()*10000)
    #random_seed = 313
    random_seed = helper.get_seed(random_seed)
    helper.set_seed(random_seed)
    
    if frameCount == 500:
        exit()
    
    #palette = pal[int(random(0,len(pal)))]        
    #palette_bg_idx = int(random(0, len(palette)))
    
    background(g.backgroundColor)

    translate(width/2, height/2)
    
    palette = pal[int(random(0, len(pal)))]

    range_upper_angles = [x for x in range(int(random(0, 20)), int(random(50, 80)), int(random(7, 20)))]
    range_lower_angles = [x for x in range(int(random(0, 20)), int(random(50, 80)), int(random(7, 20)))]
    range_upper_radii = [width*0.2, width*0.45]
    range_lower_radii = [width*0.2, width*0.3]

    ##########################################################################
    # Upper Wings
    ##########################################################################
    stroke(0, 0, 0, 60)
    for i in range(10):
        p = palette[int(random(0, len(palette)))]     
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append([0, 0])
        for angle in range_upper_angles:
            wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.2, width*0.4), radians(random(angle-7, angle))))

        draw_wings(wing, True)
    
    for i in range(10):
        p = palette[int(random(0, len(palette)))]
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append([0, 0])
        for angle in range_upper_angles:
            wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.1, width*0.2), radians(random(angle-7, angle))))

        draw_wings(wing, True)
    

    ##########################################################################
    # Lower Wings
    ##########################################################################
    stroke(0, 0, 0, 60)
    for i in range(10):
        p = palette[int(random(0, len(palette)))]
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append([0, 0])
        for angle in range_lower_angles:
            wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.15, width*0.3), radians(random(angle-7, angle))))
        wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.15, width*0.3), radians(random(73, 87))))
            
        draw_wings(wing)
            
    for i in range(10):
        p = palette[int(random(0, len(palette)))]
        if (i==3) and (i==6):
            fill(0, 0, 100, 20)
        else:
            fill(p[0], p[1], p[2], 20)
        wing = []
        wing.append([0, 0])
        for angle in range_lower_angles:
            wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.05, width*0.2), radians(random(angle-7, angle))))
        wing.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.05, width*0.2), radians(random(73, 87))))
            
        draw_wings(wing)

    
    ##########################################################################
    # Antennae and body
    ##########################################################################
    body = get_16_points(-width*0.015, -height*0.05, width*0.03, height*0.35)
    angles, radii = get_angles_radii_antennae(10, width*0.1)
    
    x_ = random(-width*0.3, 0)
    y_ = random(-height*0.4, -height*0.3)
    
    curve_tightness = []
    for a in angles:
        curve_tightness.append(random(-2, 2))
    
    break_point = int(random(2, len(angles)))
    pushMatrix()
    noFill()
    strokeWeight(3)
    stroke(p[0], p[1], 30)
    beginShape()  
    curveTightness(curve_tightness[0])
    x, y = helper.circle_points(x_, y_, angles[-1], radii[-1])
    curveVertex(x, y)
    curveVertex(*body[0])
    # curveVertex(x_head-random(w_head*0.01, w_head*0.8), y_head-random(h_head*0.01, h_head*0.5))
    for i, (a, r, c) in enumerate(zip(angles, radii, curve_tightness)):  
        if i >= break_point:
            break
        curveTightness(c)
        x, y = helper.circle_points(x_, y_, r, radians(a))
        curveVertex(x, y)
    endShape()
    curveTightness(0)
    
    scale(-1, 1)
    noFill()
    beginShape()   
    curveTightness(curve_tightness[0])
    x, y = helper.circle_points(x_, y_, angles[-1], radii[-1])
    curveVertex(x, y)
    curveVertex(*body[0])
    # curveVertex(x_head-random(w_head*0.01, w_head*0.8), y_head-random(h_head*0.01, h_head*0.5))
    for i, (a, r, c) in enumerate(zip(angles, radii, curve_tightness)):    
        if i >= break_point:
            break
        curveTightness(c)
        x, y = helper.circle_points(x_, y_, r, radians(a))
        curveVertex(x, y)
    endShape()
    curveTightness(0)
    popMatrix()
    
    
    # Body
    fill(0, 0, 100)
    noStroke()
    draw_16_points(body)
    
    
    
    helper.save_frame_timestamp('butterballs', timestamp, random_seed)

    # Save memory by closing image, just look at it in the file system
    # if (w > 1000) or (h > 1000):
    #     exit()


##########################################################################
# Functions
##########################################################################

def draw_wings(wing, upper_wing=False):
    pushMatrix()
    if upper_wing:
        scale(1,-1)
    draw_curve_filled(wing)
    scale(-1,1)
    draw_curve_filled(wing)
    popMatrix()


def get_16_points(x, y, w, h):
    squeeze = random(-w*0.2, w*0.2)
    points = [0] * 16
    points[0] = [x, y]
    points[1] = [x + w * 0.25, y]
    points[2] = [x + w * 0.5, y-h*0.05]
    points[3] = [x + w * 0.75, y]
    points[4] = [x + w, y]
    points[5] = [x + w, y + h * 0.25]
    points[6] = [x + w + squeeze, y + h * 0.5]
    points[7] = [x + w, y + h * 0.75]
    points[8] = [x + w, y + h]
    points[9] = [x + w * 0.75, y + h]
    points[10] = [x + w * 0.5, y + h]
    points[11] = [x + w * 0.25, y + h]
    points[12] = [x, y + h]
    points[13] = [x, y + h * 0.75]
    points[14] = [x - squeeze, y + h * 0.5]
    points[15] = [x, y + h * 0.25]
    
    points.pop(12)
    points.pop(8)
    points.pop(4)
    points.pop(0)
    
    return points

def cvp(x, y):
    curveVertex(x, y)
    #ellipse(x, y, 5, 5)
    
def draw_16_points(points):
    beginShape()
    for p in points + points[0:3]:
        print(p)
        cvp(*p)
    endShape()


def draw_curve_filled(data):
    beginShape()
    for t in data+data[:3]:
        cvp(*t)
    endShape()

def get_angles_radii_antennae(angle_offset, r):                    
    angles = [0]*4
    angles[0] = helper.random_centered(180, angle_offset)
    angles[1] = helper.random_centered(90, angle_offset)
    angles[2] = helper.random_centered(30, angle_offset)
    angles[3] = helper.random_centered(300, angle_offset)
    
    radii = [0]*4
    radii[0] = random(r*0.45, r*0.75)
    radii[1] = random(r*0.25, r*0.5)
    radii[2] = random(r*0.15, r*0.3)
    radii[3] = random(r*0.1, r*0.15)

    return angles, radii

def mousePressed():
    helper.save_frame_timestamp('butterballs', timestamp, random_seed)

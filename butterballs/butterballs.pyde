##########################################################################
# Aaron Penne
# https://github.com/aaronpenne
##########################################################################

import datetime
import string
import sys
from random import shuffle, seed

import helper

##########################################################################
# Global variables
##########################################################################

random_seed = 0

# Get time
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Parameters for draw speed
frame_rate = 30

##########################################################################
# Knobs to turn
##########################################################################

# Canvas size
w = 1000  # width
h = 1000  # height

##########################################################################
# Knobs to turn
##########################################################################

# Bug Green Orange
pal = {0: [[26, 79, 78],  # orange    
           [107, 52, 31], # green
           [74, 62, 51],  # weirdgreen
           [197, 37, 38], # grayblue
           [39, 52, 87]],  # yellow
        # Bug Green Brown
        1: [[44, 53, 38], # brownish  
            [79, 40, 65], # lightgreen
            [83, 66, 38], # green
            [43, 42, 84], # tan
            [38, 65, 70], # tanbrown
            [78, 69, 19]], # darkgreen
        # Bug Red Orange
        2: [[14, 79, 93], # orange
            [5, 100, 55], # red
            [359, 100, 35], # darkred
            [37, 38, 87]], #tan
}
            
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

    background(0, 0, 95)

    rectMode(CORNER)

    # Stops draw() from running in an infinite loop (should be last line)
    #noLoop()  # Comment to run draw() infinitely (or until 'count' hits limit)


##########################################################################
# draw()
# function gets run repeatedly (unless noLoop() called in setup())
#
# 0--1--2--3--4
# |           |
# 15          5
# |           |
# 14          6
# |           |
# 13          7
# |           |
# 12-11-10--9-8
#
#
##########################################################################

def draw():
    global random_seed
    random_seed = int(random(0, 10000))
    #random_seed = 7900
    random_seed = helper.get_seed(random_seed)
    helper.set_seed(random_seed)
    
    
    palette = pal[int(random(0,len(pal)))]        
    palette_bg_idx = int(random(0, len(palette)))
    
    background(g.backgroundColor)

    translate(width / 2, height / 2)
    

    ##########################################################################
    # Upper Wings
    ##########################################################################
    noStroke()
    for i in range(10):
        if i % 2 == 0:
            fill(random(0, 15), random(70, 85), random(50, 70), random(10, 20))
        else:    
            fill(random(30, 45), random(35, 50), random(70, 90), random(10, 20))
        test = []
        test.append([0, 0])
        for angle in [10, 20, 30, 40]:
            test.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.2, width*0.4), radians(random(angle-7, angle))))

        pushMatrix()
        scale(1,-1)
        draw_curve_filled(test)
        scale(-1,1)
        draw_curve_filled(test)
        popMatrix()
    
    for i in range(15):
        if i % 2 == 0:
            fill(random(0, 15), random(70, 85), random(50, 70), random(10, 20))
        else:    
            fill(random(30, 45), random(35, 50), random(70, 90), random(10, 20))
        test = []
        test.append([0, 0])
        for angle in [10, 20, 30, 40]:
            test.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.1, width*0.2), radians(random(angle-7, angle))))

        pushMatrix()
        scale(1,-1)
        draw_curve_filled(test)
        scale(-1,1)
        draw_curve_filled(test)
        popMatrix()
    
    

    ##########################################################################
    # Lower Wings
    ##########################################################################
    noStroke()
    for i in range(20):
        if i % 2 == 0:
            fill(random(0, 15), random(70, 85), random(50, 70), random(10, 20))
        else:    
            fill(random(30, 45), random(35, 50), random(70, 90), random(10, 20))
        test = []
        test.append([0, 0])
        for angle in [10, 25, 40, 55, 70]:
            test.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.05, width*0.3), radians(random(angle-7, angle))))
        test.append(helper.circle_points_list(random(0, width*0.01), random(0, height*0.01), random(width*0.05, width*0.3), radians(random(73, 87))))
            
        pushMatrix()
        draw_curve_filled(test)
        scale(-1,1)
        draw_curve_filled(test)
        popMatrix()
        
        
    ##########################################################################
    # Body
    ##########################################################################

    fill(g.backgroundColor)
    ellipse(0, -20, random(20, 45), random(50, 60))
    ellipse(0, 0, random(20, 45), random(50, 60))
    ellipse(0, 100, random(40, 50), random(170, 250))
    
   
    ##########################################################################
    # Antennae
    ##########################################################################
    # stroke(0, 0, 0)
    # x1, y1 = [-10, 0]
    # x2, y2 = [x1-random(width*0.05, width*0.1), y1-random(width*0.05, height*0.1)]
    # x3, y3 = [x2+random(-width*0.1, width*0.1), y2+random(-height*0.1, height*0.1)]
    # x4, y4 = [x3+random(-width*0.1, width*0.1), y3+random(-height*0.1, height*0.1)]
    # x5, y5 = [x4+random(-width*0., width*0.), y4+random(-height*0.1, height*0.1)]

    # curveTightness(random(-0.9, 0.9))
    
    # pushStyle()
    # noFill()
    # strokeWeight(3)
    # ellipse(x1, y1, 3, 3)
    # beginShape()
    # cvp(x5, y5)
    # cvp(x1, y1)
    # cvp(x2, y2)
    # cvp(x3, y3)
    # cvp(x4, y4)
    # cvp(x5, y5)
    # cvp(x1, y1)
    # endShape()
    
    # pushMatrix()
    # scale(-1.0, 1.0)
    # ellipse(x1, y1, 3, 3)
    # beginShape()
    # cvp(x5, y5)
    # cvp(x1, y1)
    # cvp(x2, y2)
    # cvp(x3, y3)
    # cvp(x4, y4)
    # cvp(x5, y5)
    # cvp(x1, y1)
    # endShape()
    # popStyle()
    # popMatrix()
    
    # curveTightness(0)
    
    
    
    #helper.save_frame_timestamp('butterballs', timestamp, random_seed)

    # Save memory by closing image, just look at it in the file system
    # if (w > 1000) or (h > 1000):
    #     exit()


##########################################################################
# Functions
##########################################################################

def draw_curve_filled(data):
    beginShape()
    for t in data+data[:3]:
        cvp(*t)
    endShape()
    
    
def get_pattern(pattern_style, lightness_offset, palette, palette_bg_idx):
    bg_color = palette[palette_bg_idx]
    
    if pattern_style == 'dots':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.background(color(bg_color[0], bg_color[1], bg_color[2]*lightness_offset)) # mauve
        #pattern.translate(width/2, height/2)
        pattern.noStroke()
        for i in range(40):
            fg_color = palette[int(random(0, len(palette)))]
            pattern.fill(color(fg_color[0], fg_color[1], fg_color[2]*lightness_offset))
            r = random(5, 200)
            x = random(0, width)
            y = random(0, height)
            pattern.ellipse(x, y, r, r*random(1.2, 3))
        pattern.endDraw()
        pattern.popMatrix
        
    elif pattern_style == 'bg':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.background(color(bg_color[0], bg_color[1], bg_color[2]*lightness_offset)) # mauve
        pattern.endDraw()
        pattern.popMatrix
        
    elif pattern_style == 'gradient':
        pattern = createGraphics(width, height)
        pattern.beginDraw()
        pattern.pushMatrix()
        pattern.background(color(0, 100, 100*lightness_offset)) # mauve
        #pattern.translate(width/2, height/2)
        pattern.noStroke()
        for i in range(40):
            pattern.fill(color(random(0, 360), random(20,30), random(60,90), 50*lightness_offset)) # green
            r = random(200, 1000)
            x = random(0, width)
            y = random(0, height)
            print(x, y, r)
            pattern.ellipse(x, y, r, r)
        pattern.endDraw()
        pattern.popMatrix
        
    return pattern


def outline_wing(l_wing):
    pushStyle()
    noFill()
    stroke(0, 0, 20)
    
    pushMatrix()
    # rotate(PI/40)
    beginShape()
    cvp(*l_wing[0])
    cvp(*l_wing[2])
    cvp(l_wing[5][0], l_wing[5][1]-h*0.05)
    cvp(*l_wing[8])
    curveTightness(0.9)
    cvp(*l_wing[13])
    curveTightness(0)
    cvp(*l_wing[0])
    cvp(*l_wing[2])
    cvp(l_wing[5][0], l_wing[5][1]-h*0.05)
    endShape()
    popMatrix()
    popStyle()
    

def cvp(x, y):
    curveVertex(x, y)
    #ellipse(x, y, 5, 5)


def get_16_points(x, y, w, h):
    points = [0] * 16
    points[0] = [x, y]
    points[1] = [x + w * 0.25, y]
    points[2] = [x + w * 0.5, y]
    points[3] = [x + w * 0.75, y]
    points[4] = [x + w, y]
    points[5] = [x + w, y + h * 0.25]
    points[6] = [x + w, y + h * 0.5]
    points[7] = [x + w, y + h * 0.75]
    points[8] = [x + w, y + h]
    points[9] = [x + w * 0.75, y + h]
    points[10] = [x + w * 0.5, y + h]
    points[11] = [x + w * 0.25, y + h]
    points[12] = [x, y + h]
    points[13] = [x, y + h * 0.75]
    points[14] = [x, y + h * 0.5]
    points[15] = [x, y + h * 0.25]
    return points


def draw_16_points(points):
    beginShape()
    for p in points + points[0:3]:
        cvp(*p)
    endShape()


def draw_12_points(points):
    #points = [points[i] for i in [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15]]
    curveTightness(0.3)
    beginShape()
    for p in points + points[0:3]:
        cvp(*p)
    endShape()

def mousePressed():
    helper.save_frame_timestamp('butterballs', timestamp, random_seed)

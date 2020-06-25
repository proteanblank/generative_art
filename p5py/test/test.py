from p5 import *

def setup():
    size(1000,1000)
    no_stroke()
    background(0)

def draw():
    if mouse_is_pressed:
        fill(random_uniform(255), random_uniform(255), random_uniform(255), 150)
    else:
        fill(255, 15)
    
    circle_coords = (mouse_x, mouse_y)
    circle_size = random_uniform(low=10, high=80)

    circle(circle_coords, circle_size)

def key_pressed(event):
    backgroun(200)

run()

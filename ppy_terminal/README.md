# Generative art using Python from the command line

Making generative art with Processing is awesome. Making it with Python is even better, in my opinion. [Processing.py](https://py.processing.org/) makes that happen. 

All "normal" Processing features and methods that I've tried are available in Processing.py as well. The reference docs on the Processing.py site are lagging behind the Processing.org site, so just use the "normal" Processing docs and [API reference](https://processing.org/reference/).

## Motivation

My personal use case has evolved, and I want to be able to create artwork from the command line, outside of Processing's default IDE. This directory is the environment I'm using to accomplish the following requirements:
* Code from the command line, preferred text editor, or preferred Python IDE
* Execute from the command line
* Write images straight to disk without displaying them
* Use object oriented drawing and helper classes which can be imported like normal
* Use config files and configparser to control input parameters
* Curate and cull lots of images quickly

## Python 2.7 and Jython

As of this writing, *Python 2.7* is used in Processing.py, which is not ideal but has not been a blocker personally. 

"Normal" Processing uses Java, and Processing.py uses Jython to implement Python wrappers around the core Java functionality. The quirks are detailed [here](https://py.processing.org/tutorials/python-jython-java/). 

The Python used by Processing is part of the Processing jar file you will download, so there is no need to set up a virtual environment or install Python separately.

## Setup

This type of setup works for Mac OSX, Windows, and Linux. I use a Mac, so my setup reflects that. To get my environment setup I followed these steps: https://py.processing.org/tutorials/command-line/

The main steps are:
* Download jdk-8u202-macosx-x64.dmg and install it (must be this version) - [Download link](https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html)
* Download the standalone version of Processing.py - [Download link](http://py.processing.org/processing.py-macosx.tgz)
* Put `processing-py.jar` in ppy_terminal/exec/ 
* Write a basic Python sketch
* Run the sketch

## Running

As the [tutorial above](https://py.processing.org/tutorials/command-line/) states, you need to call the processing-py.jar file to run your sketches. Once the processing-py.jar lives somewhere (I prefer the exec dir) a sketch can be run like below. Note that you'll have to change the path to processing-py.jar to suite your setup:

'''
java -jar ~/github.com/generative_art/ppy_terminal/exec/processing-py.jar my_sketch.py
'''

This is a mouthful to type, so I alias it in my .zshrc and .bashrc files like this:

'''
alias ppy="java -jar ~/github.com/generative_art/ppy_terminal/exec/processing-py.jar"
'''

Now I can just run this command to run my sketch:

'''
ppy my_sketch.py
'''

## Directory structure

Directory structure on my laptop:
* ppy_terminal/
    * exec/
      * processing-py.jar
      * ffmpeg
      * jdk-8u202-macosx-x64.dmg
    * helpers/
      * <helper scripts>.sh
    * imports/
      * <python imports>.py
    * sketches/
      * sketch_a
        * sketch_a.py
        * config
        * output
          * sketch_a_1138_20200101_113328_001.png
        * images
          * sketch_a_1138_20200101_113328_001.png

## Writing straight to disk

To speed my development time, I prefer to write straight to disk instead of displaying the image in Processing's viewer. This reduces render time and allows me to use a preferred tool to view all the images together. 

The trick is to use [createGraphics()](https://processing.org/examples/creategraphics.html) as the buffer where all actions happen, then save the graphic instead of using image() to display it. There are some quirks:
* You must use beginDraw() and endDraw() at the start and end respectively. 
* A lot of setup functions like colorMode() must be done on the graphic. 
* To print just one image, use noLoop() in the setup() function and use exit() after saving

Here is a working example (also at templates/template_basic.py):

'''python
def setup():
  global pg
  pg = createGraphics(1000, 1000)
  
  noLoop()

def draw():
  pg.beginDraw()
  pg.colorMode(HSB, 360, 100, 100, 100)
  pg.background(0, 0, 25)
  pg.stroke(60, 7, 86, 100)
  pg.noFill()

  for i in range(200):
    pg.ellipse(random(pg.width), random(pg.height), 100, 100)

  pg.endDraw()
  pg.save('image.png')
  exit()
'''


## Nice to have tools

These are some free tools in my generative art environment/workflow that I prefer, but are not necessary:
* [iterm2](https://www.iterm2.com/)
    * Super powerful terminal replacement
    * Allows multiple panes so I can edit config, imports, and sketches at once
* [XnView MP](https://www.xnview.com/en/xnviewmp/)
    * Fast and feature rich curating/culling tool
    * Enables skimming of thousands of thumbnails, rating images, and bulk moving 
    * This is a personal favorite tool, I've tried several. Curating is a huge part of the creative process when it comes to generative art.

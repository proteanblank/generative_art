////////////////////////////////////////////////////////////////////////////////
// code and images by Aaron Penne
// https://github.com/aaronpenne/generative_art
//
// Uses OpenSimplexNoise.java in separate tab from:
//    https://gist.github.com/Bleuje/fce86ef35b66c4a2b6a469b27163591e
//
// released under the MIT license (https://opensource.org/licenses/MIT)
////////////////////////////////////////////////////////////////////////////////

boolean record = false;
boolean animate = false;
boolean seeded = true;

int stroke_weight = 1;
float z_off = 0;
float z_inc = 0.02;


float grid_step = 80;
float radius = 90;

float cols, rows;

color fg, bg;

int rand_seed = 1138;

OpenSimplexNoise noise;

color[] pal = new color[20];

String timestamp = String.format("%04d%02d%02d_%02d%02d%02d", year(), month(), day(), hour(), minute(), second());

void setup() {
  // Sets size of canvas in pixels (must be first line)
  size(800, 800);
    
  // Sets resolution dynamically (affects resolution of saved image)
  pixelDensity(displayDensity());  // 1 for low, 2 for high
    
  // Sets color space to Hue Saturation Brightness with max values of HSB respectively
  colorMode(HSB, 360, 100, 100, 100);
        
  // Set the number of frames per second to display
  frameRate(50);
    
  // Keeps text centered vertically and horizontally at (x,y) coords
  textAlign(CENTER, CENTER);
    
  rectMode(CORNERS);
    
  // Stops draw() from running in an infinite loop
  if (!animate) {
    noLoop();
  }
        
  // Sets random seed value for both Python and Processing 
  if (seeded) {
    randomSeed(rand_seed);  // Only applies to the random() Processing function
    noiseSeed(rand_seed);   // Only applies to the noise() Processing function
  }
  
  noise = new OpenSimplexNoise();
  
  pal[0] = color(0,0,100);
  pal[1] = color(0,0,25);
  // Fisk Map colors
  pal[2] = color(39, 16.9, 92.9);    // tan background
  pal[3] = color(48.8, 27, 92.9);    // yellowish
  pal[4] = color(152, 11, 76);       // blueish
  pal[5] = color(2.7, 40.3, 86.7);   // reddish
  pal[6] = color(60, 18.4, 80.8);    // greenish
  // Red/black shirt colors
  pal[7] = color(11, 50, 68);   // reddish
  pal[8] = color(207, 22, 20);  // blackish
         
  fg = pal[8];
  bg = pal[4];
  
  cols = floor(width/grid_step);
  rows = floor(height/grid_step);
        
  background(bg);
}

void draw() {
  background(bg);
  
  strokeWeight(stroke_weight);
  stroke(fg);
  //noStroke();
  
  fill(fg);
  noFill();
  

  float x_off = 0;
  for (float x=0; x<cols; x++) {
    float y_off = 0;
    for (float y=0; y<rows;y++) {
      float index = (x + y * width) * 4;
      float angle = map((float) noise.eval(x_off, y_off),-1,1,0,200);
      PVector v = PVector.fromAngle(angle);
      x_off += z_inc;
      push();
      translate(x*grid_step+grid_step/2, y*grid_step+grid_step/2);
      rotate(v.heading());
      ellipse(0, 0, radius, radius);
      pop();
    }
    y_off += z_inc;
  }





  
  z_off += z_inc;
  
  if (record) {
    save_frame_to_file();
  }
      
  // Stops draw() from running in an infinite loop
  if (!animate) {
    save_frame_to_file();
  }
        
}

void save_frame_to_file() {
    String output_filepath = "output/%s_####.png";
    println(String.format("Saving %04d to %s", frameCount, String.format(output_filepath, timestamp)));
    saveFrame(String.format(output_filepath, timestamp));
}

void mousePressed() {
  save_frame_to_file();
  noLoop();
}

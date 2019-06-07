////////////////////////////////////////////////////////////////////////////////
// code and images by Aaron Penne
// https://github.com/aaronpenne/generative_art
//
// released under the MIT license (https://opensource.org/licenses/MIT)
////////////////////////////////////////////////////////////////////////////////

boolean record = true;
boolean animate = true;
boolean seeded = true;

int stroke_weight = 20;
float z_off = 0;
float z_inc = 0.02;

NoiseLoop rNoise = new NoiseLoop(0.05, 40, 300, 1, 1);

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
         
  fg = pal[7];
  bg = pal[8];
        
  background(pal[7]);
}

void draw() {
  background(fg);
  translate(width/2, height/2);
  
  strokeWeight(stroke_weight);
  stroke(bg);
  //noStroke();
  
  fill(fg);
  noFill();
  
  for (int r_step=-80; r_step<=480; r_step+=40) {
    draw_blob(45, r_step);
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



void draw_blob(float a_step, float r_step) {
  float x, y;
  float r;
  
  beginShape();
  for(int a=0; a<=360+(2*a_step); a+=a_step) {
    r = rNoise.value(radians(a));
    x = (r_step + r) * cos(radians(a));
    y = (r_step + r) * sin(radians(a));
    curveVertex(x,y);
  }
  endShape();
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


// NoiseLoop by Daniel Shiffman
// Samples 2D perlin noise space in a circular fashion
// https://github.com/CodingTrain/website/tree/master/CodingChallenges/CC_136_Polar_Noise_Loop_2/Processing/CC_136_Polar_Noise_Loop_2
class NoiseLoop {
  float diameter;
  float min, max;
  float cx;
  float cy;

  NoiseLoop(float diameter, float min, float max, float cx, float cy) {
    this.diameter = diameter;
    this.min = min;
    this.max = max;
    if (cx != 1) {
      cx = random(1000);
    }
    if (cy != 1) {
      cy = random(1000);
    }
  }

  float value(float a) {
    float xoff = map(cos(a), -1, 1, cx, cx + diameter);
    float yoff = map(sin(a), -1, 1, cy, cy + diameter);
    float r = (float)noise.eval(xoff, yoff, z_off);
    return map(r, -1, 1, min, max);
  }
}

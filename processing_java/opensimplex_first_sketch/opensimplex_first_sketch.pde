////////////////////////////////////////////////////////////////////////////////
// code and images by Aaron Penne
// https://github.com/aaronpenne/generative_art
//
// https://www.youtube.com/watch?v=Lv9gyZZJPE0
//
// released under the MIT license (https://opensource.org/licenses/MIT)
////////////////////////////////////////////////////////////////////////////////

float step = 5;
int radius = 5;

float increment = 0.025;

float z_off = 0.0;

float z_increment = 0.02;

boolean record = true;
boolean animate = true;
boolean seeded = true;

int rand_seed = 1138;

OpenSimplexNoise noise;

float pal[][] = {{36, 16.9, 92.9}, 
                 {2.7, 40.3, 86.7}};
                 
String timestamp = String.format("%04d%02d%02dT%02d%02d%02d", year(), month(), day(), hour(), minute(), second());

void setup() {
  // Sets size of canvas in pixels (must be first line)
  size(700, 700);
    
  // Sets resolution dynamically (affects resolution of saved image)
  // pixelDensity(displayDensity());  // 1 for low, 2 for high
    
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
}

void draw() {
  background(pal[0][0], pal[0][1], pal[0][2]);
  stroke(pal[1][0], pal[1][1], pal[1][2]*0.6);
  draw_blobs(0, 0, z_off);
  stroke(pal[1][0], pal[1][1], pal[1][2]);
  draw_blobs(0.1, 0.1, z_off);
  
  z_off += z_increment;
  
  if (record) {
    String output_filepath = "output/%s_####.png";
    println(String.format("Saving %04d to %s", frameCount, String.format(output_filepath, timestamp)));
    saveFrame(String.format(output_filepath, timestamp));
  }
}

void draw_blobs(float x_extra, float y_extra, float z_off) {
  float x_off = 0.0;
  for (int x=radius/2; x<width; x+=step) {
    x_off += increment;
    
    float y_off = 0.0;
    for (int y=radius/2; y<height; y+=step) {
      y_off += increment;
      
      float h = 0;
      float s = 0;
      float b = (float) noise.eval(x_off+x_extra, y_off+y_extra, z_off);
      
      strokeWeight(radius);
      if (b > 0.1) {
        point(x, y);
      }
    }
  }  
  
  
}

////////////////////////////////////////////////////////////////////////////////
// code and images by Aaron Penne
// https://github.com/aaronpenne/generative_art
//
// released under the MIT license (https://opensource.org/licenses/MIT)
////////////////////////////////////////////////////////////////////////////////

int max_frames = 10;

float step = 5;
int radius = 5;

float increment = 0.025;

float z_off = 0.0;
float t_off = 0.0;

float z_increment = 0.02;

boolean record = false;
boolean animate = false;
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

  background(0, 0, 25);
  stroke(60, 7, 86);
  noFill();
  strokeWeight(10);
}

void draw() {

  float min = width*0.1;
  float max = width*0.9;

  beginShape();
  float y2 = height/2;
  float x2 = width/2;
  float test = width/0.2;
  print(min);
  for (float x=min; x>=max; x++) {
    print(y2);
    y2 += map((float) noise.eval(x, y2), 0, 1, -10, 20);
    print(x, y2);
    vertex(x, y2);
  }

  endShape();


  if (record) {
    String output_filepath = "output/%s_####.png";
    println(String.format("Saving %04d to %s", frameCount, String.format(output_filepath, timestamp)));
    saveFrame(String.format(output_filepath, timestamp));
  }
}

void draw_line(float min, float max, float thickness) {
}

var t1 = 0;
var t2 = 10;
var c1 = 0;

var w, h;
var x, y;

function setup() {
  colorMode(HSB, 360, 100, 100, 100);

  w = windowWidth*0.8;
  if (w > 1000) {
    w = 1000;
  }
  h = windowHeight*0.7;
  if (h > 1000) {
    h = 1000;
  }
  var canvas = createCanvas(w, h);
  canvas.parent('sketch-div');

  background(0, 0, 100);
  textFont('Monospace');
  textSize(12);
  textAlign(CENTER, CENTER);



  canvas.mousePressed(canvasMouseClicked);
}

function draw() {
  t1 = t1 + 0.005;
  t2 = t2 + 0.005;

  c1 = c1 + 0.5
  c = c1%360

  pn1 = map(noise(t1), 0, 1, 0, width*0.5);
  pn2 = map(noise(t2), 0, 1, 0, height*0.5);

  x = width/2;
  y = height/2;

  var min_r = map(noise(t1), 0, 1, width*0.05, width*0.5)

  stroke(210,	22,	18, 5);
  //fill(c, 50, 80);
  noFill()
  ellipse(x, y, pn1*abs(sin(frameCount*PI/400))+min_r, pn2*abs(sin(frameCount*PI/330))+min_r);
  noFill();
  rect(0, 0, w-1, h-1);
}

function windowResized() {
  w = windowWidth*0.8;
  if (w > 1000) {
    w = 1000;
  }
  h = windowHeight*0.7;
  if (h > 1000) {
    h = 1000;
  }
  resizeCanvas(w, h);
  background(0, 0, 100);
}

function canvasMouseClicked() {
  saveCanvas('sketch', 'png');
  noLoop();
  return false;
}

function keyPressed() {
  if (key == 's') {
    saveCanvas('sketch', 'png');
    noLoop();
    return false;
  }
}

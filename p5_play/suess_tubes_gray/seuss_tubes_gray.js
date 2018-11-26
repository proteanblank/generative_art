var t1 = 0;
var t2 = 10;
var x, y;

function setup() {
  colorMode(HSB, 360, 100, 100, 100);
  var canvas = createCanvas(windowWidth*0.8, windowHeight*0.7);
  canvas.parent('sketch-div');

  background('#e1e1e1');
  canvas.mousePressed(canvasMouseClicked);
}

function draw() {
  t1 = t1 + 0.005;
  t2 = t2 + 0.005;

  var A = width*0.2;
  if (A > 200) {
    A = 200;
  }
  if (A < 20) {
    A = 20;
  }

  pn1 = map(noise(t1), 0, 1, 5, A);
  pn2 = map(noise(t2), 0, 1, 5, A);

  if (mouseX==0 && mouseY==0) {
    x = -100000;
    y = -100000;
  } else {
    x = mouseX
    y = mouseY
  }

  stroke('#3f3f3f');
  fill('#cdcdcd');
  ellipse(x, y, pn1*sin(frameCount*PI/400), pn2*sin(frameCount*PI/330));
  noFill();
  rect(0, 0, windowWidth*0.8-1, windowHeight*0.7-1);
}

function windowResized() {
  resizeCanvas(windowWidth*0.8, windowHeight*0.7);
  background('#e1e1e1');
}

function canvasMouseClicked() {
  saveCanvas('sketch', 'png');
  noLoop();
  return false;
}

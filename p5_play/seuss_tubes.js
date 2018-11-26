var t1 = 0;
var t2 = 10;
var c1 = 0;

var w, h;
var x, y;

var drawing = 1;

function setup() {
  colorMode(HSB, 360, 100, 100, 100);

  w = windowWidth*0.8;
  if (w > 1100) {
    w = 1100;
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

  var A = width*0.2;
  if (A > 300) {
    A = 300;
  }
  if (A < 40) {
    A = 40;
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

  var min_r = 10;

  stroke(210,	22,	18, 40);
  fill(c, 50, 80);
  ellipse(x, y, pn1*abs(sin(frameCount*PI/400))+min_r, pn2*abs(sin(frameCount*PI/330))+min_r);
  noFill();
  push()
  stroke(0,	0, 30);
  rect(0, 0, w-1, h-1);
  pop()
}

function windowResized() {
  w = windowWidth*0.8;
  if (w > 1100) {
    w = 1100;
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
  drawing = 0;
  return false;
}

function keyPressed() {
  if (key == 's') {
    saveCanvas('sketch', 'png');
    noLoop();
    return false;
  } else if (key == 'q') {
    if (drawing == 1) {
      noLoop();
      drawing = 0;
    } else {
      loop();
      drawing = 1;
    }
  }
}

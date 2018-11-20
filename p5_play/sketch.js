function setup() {
  colorMode(HSB, 360, 100, 100, 100);
  var canvas = createCanvas(windowWidth*0.8, windowHeight*0.7);
  canvas.parent('sketch-div');

  background('#e1e1e1');
  textFont('Monospace');
  textSize(22);
  textAlign(CENTER, CENTER);
  text('draw here!', width/2, height/2);
}

function draw() {
  var A = width*0.2;
  if (A > 150) {
    A = 150;
  }
  stroke('#3f3f3f');
  fill('#e1e1e1');
  ellipse(mouseX, mouseY, A*sin(frameCount*PI/400), A*sin(frameCount*PI/200+PI/5));
  noFill();
  rect(0, 0, windowWidth*0.8-1, windowHeight*0.7-1);
}

function windowResized() {
  resizeCanvas(windowWidth*0.8, windowHeight*0.7);
  background('#e1e1e1');
  text('draw here!', width/2, height/2);
}

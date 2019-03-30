var t1 = 0;
var t2 = 10;
var x, y;

var drawing = 1;

var divisions = 10;

var a_step = PI/divisions;
var angles = ange_float(0, TWO_PI, a_step);

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

  var A = 10;

  pn1 = map(noise(t1), 0, 1, 0, A);
  pn2 = map(noise(t2), 0, 1, 0, A);

  if (mouseX==0 && mouseY==0) {
    x = -100000;
    y = -100000;
  } else {
    x = mouseX
    y = mouseY
  }

  var min_r = 10;
  strokeWeight(1)
  stroke('#3f3f3f');
  fill('#cdcdcd');
  ellipse(x, y, pn1*abs(sin(frameCount*PI/400))+min_r, pn2*abs(sin(frameCount*PI/330))+min_r);
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

function keyPressed() {
  if (key == 's') {
    saveCanvas('sketch', 'png');
    noLoop();
  } else if (key == 'q') {
    if (drawing == 1) {
      noLoop();
      drawing = 0;
    } else {
      loop();
      drawing = 1;
    }
  }
  return false;
}

function circle_points_list(origin_x, origin_y, r, a) (
    x = origin_x + (r * cos(a));
    y = origin_y + (r * sin(a));
    return [x, y];
)


function range(low, high, step) {
  //  discuss at: http://phpjs.org/functions/range/
  // original by: Waldo Malqui Silva

  var matrix = [];
  var inival, endval, plus;
  var walker = step || 1;
  var chars = false;

  if (!isNaN(low) && !isNaN(high)) {
    inival = low;
    endval = high;
  } else if (isNaN(low) && isNaN(high)) {
    chars = true;
    inival = low.charCodeAt(0);
    endval = high.charCodeAt(0);
  } else {
    inival = (isNaN(low) ? 0 : low);
    endval = (isNaN(high) ? 0 : high);
  }

  plus = ((inival > endval) ? false : true);
  if (plus) {
    while (inival <= endval) {
      matrix.push(((chars) ? String.fromCharCode(inival) : inival));
      inival += walker;
    }
  } else {
    while (inival >= endval) {
      matrix.push(((chars) ? String.fromCharCode(inival) : inival));
      inival -= walker;
    }
  }

  return matrix;
}

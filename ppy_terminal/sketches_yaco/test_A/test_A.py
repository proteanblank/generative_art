import test_import

def setup():
  size(200, 200)
  noLoop()

def draw():
  ellipse(50, 50, 50, 50)
  test_import.get_git_hash('/Users/apenne/github.com/generative_art/ppy_terminal/imports/test_import.py')

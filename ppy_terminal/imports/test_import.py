def print_something():
  print('something')

def git_stuff(filepath):
  import subprocess
  label = subprocess.check_output(["git", "rev-list", "-1", "HEAD", filepath]).strip()
  print(label)

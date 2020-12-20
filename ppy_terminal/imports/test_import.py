def print_something():
  print('something')

def get_git_hash(filepath):
  import subprocess
  return subprocess.check_output(["git", "rev-list", "-1", "--abbrev-commit", "HEAD", filepath]).strip()

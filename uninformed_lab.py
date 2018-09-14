import sys
import fileinput
from pprint import pprint

def create_containers(line, array):
  for container in line.split(';'):
    array.append(container.replace('(', '').replace(')', '').replace(' ', '').split(','))

def main():
  lines = []
  start = []
  goal = []
  for line in fileinput.input():
    lines.append(line.rstrip())

  height = int(lines[0])
  
  #Create start containers
  create_containers(lines[1], start)
  #Create goal containers
  create_containers(lines[2], goal)
  
  print(height)
  print(start)
  print(goal)
  pass

if __name__ == '__main__':
  main()
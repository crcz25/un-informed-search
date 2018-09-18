"""
  Moies Alexander Gama Espinosa
  Carlos Roberto Cueto Zumaya
  IA - (Un)informed Search Lab
"""
import sys
import fileinput
from pprint import pprint
from queue import PriorityQueue
from itertools import zip_longest

class PrioritizedState:
  def __init__(self, priority, cost, state, stack):
    self.priority = priority
    self.state = state
    self.cost = cost
    self.stack = stack
  
  def __cmp__(self,other):
      if self.priority < other.priority:
          return -1
      elif self.priority > other.priority:
          return 1
      else:return 0
      
  def __le__(self, other):
    return self.priority <= other.priority
    
  def __lt__(self, other):
    return self.priority < other.priority 

def create_containers(line, array):
  for container in line.split(';'):
    str_list = container.replace('(', '').replace(')', '').replace(' ', '').split(',')
    str_list = list(filter(None, str_list))

    
    array.append(str_list)

def generateStates(state, height):
  children = []
  #print(state, height)
  
  for pivot in range(len(state)):
    for dest in range(len(state)):
      if pivot != dest:
        if len(state[dest]) == height or len(state[pivot]) == 0:
          continue
        
        new_state = [x[:] for x in state]
  
        new_state[dest].append(new_state[pivot][-1])
        new_state[pivot] = new_state[pivot][:-1]
        
        new_cost = 1 + abs(pivot - dest)

        children.append( (new_cost, new_state, (pivot, dest)) )
        
        
  return children
        

def isGoal(state, goal):
  for i in range(len(state)):
    if len(goal[i]) > 0 and goal[i][0] == 'X':
      continue
    
    if(len(state[i]) != len(goal[i])):
      return False
      
    for j in range(len(state[i])):
      if state[i][j] != goal[i][j]:
        return False
  
  return True

def toHashable(mat):
  return "%s" % mat

def a_star(start, goal, max_height, heuristic):
  q = PriorityQueue()
  q.put(PrioritizedState(0, 0, start, []))
  
  visited = set()

  while not(q.empty()):
    s = q.get()
    
    h = toHashable(s.state)
    if h in visited:
      continue
    visited.add(h)
    
    if(isGoal(s.state, goal)):
      return (s.cost, s.stack)
    
    children = generateStates(s.state, max_height)
    #pprint(children)
    
    for child in children:
      new_cost = child[0] + s.cost
      new_state = child[1]
      new_stack = s.stack[:]
      new_stack.append(child[2])
      
      #print(new_state)
      ps = PrioritizedState(new_cost + heuristic(new_state), new_cost, new_state, new_stack)
      #print('consistent', heuristicConsistent(new_state, goal))
      #print('inconsistent', heuristicInconsistent(new_state, goal))
      
      q.put(ps)


  return None
  
def heuristicZero(state):
  return 0

# Calculate misplaced blocks
def heuristicConsistent(state, goal):
  #print('state:', state, 'goal:', goal)
  misplaced_blocks = 0
  for index, (stateElement, goalElement) in enumerate(zip_longest(state, goal)):
    #print(index, 'if', stateElement, '!=', goalElement)
    if stateElement != goalElement:
      misplaced_blocks = misplaced_blocks + 1
  
  #print('misplaced', misplaced_blocks)
  return misplaced_blocks

def heuristicInconsistent(state, goal):
  #print('state:', state, 'goal:', goal)
  misplaced_blocks = 0
  for index, (stateElement, goalElement) in enumerate(zip_longest(state, goal)):
    #print(index, 'if', stateElement, '!=', goalElement)
    if stateElement != goalElement:
      misplaced_blocks = misplaced_blocks + 1
  
  #print('misplaced', misplaced_blocks)
  return misplaced_blocks * 2

def main():
  lines = []
  start = []
  goal = []
  for line in fileinput.input():
    lines.append(line.rstrip())

  #Obtain max height of container
  height = int(lines[0])
  #Create start containers
  create_containers(lines[1], start)
  #Create goal containers
  create_containers(lines[2], goal)
  
  res = a_star(start, goal, height, heuristicZero)
  
  if res == None:
    print('No solution found')
  else:
    print(res[0])
    steps = map(str, res[1])
    print('; '.join(steps))

if __name__ == '__main__':
  main()
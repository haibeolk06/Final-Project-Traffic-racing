import collections
import heapq
import sys
import math
from termcolor import colored

class Queue:
  def __init__(self):
    self.queue = []
  
  def push(self, label):
    self.queue.append(label)

  def pop(self):
    return self.queue.pop(0)
  
  def is_empty(self):
    return len(self.queue) == 0

class Stack:
  def __init__(self):
    self.stack = []    

  def push(self, label):
    self.stack.append(label)

  def pop(self):
    return heapq.heappop(self.stack)

  def is_empty(self):
    return len(self.stack) == 0

class PriorityQueue:
  def __init__(self):
    self.priority_queue = []
  
  def push(self, value, label):
    heapq.heappush(self.priority_queue, (value, label))

  def pop(self):
    return heapq.heappop(self.priority_queue)
  
  def is_empty(self):
    return len(self.priority_queue) == 0
  
  def update_value(self, new_value, label):
    # (value, label) = self.queue[index] 
    # -> self.queue[index][0]: value
    # -> self.queue[index][1]: label = label 
 
    for i in range(len(self.queue)):
      if self.priority_queue[i][1] == label:
        self.priority_queue[i][0] == new_value
        return

class Grid:
  def __init__(self, size, impediment, gas):   
    self.m = size
    self.impediment = impediment
    self.gas = gas

  def in_bounds(self, pos):
    x, y  = pos
    # check if pos (x,y) is in maze matrix
    return x >=0 and x < self.m and y >= 0 and y < self.m

  def is_impediment(self, pos):
    for p in self.impediment:
      if pos == p:
        return False       
    return True 
  
  def is_gas(self, pos):
    for p in self.gas:
      if pos == p:
        return False
    return True 

  def neighbors(self, pos):
    # Return a list of positions are neighbors of pos
    x, y = pos
    neighbors = [(x,y+1),(x,y-1),(x+1,y),(x-1,y)]
    #neighbors = [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]

    valid_neighbors = []
    for p in neighbors:
      if self.in_bounds(p) and self.is_impediment(p):
        valid_neighbors.append(p)
    #print(self.impediment[0])
    #print(type(valid_neighbors[0]))
    return valid_neighbors

  def neighbors_DFS(self, pos):
    # Return a list of positions are neighbors of pos
    x, y = pos
   
    neighbors = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
    valid_neighbors = []
    for p in neighbors:
      if self.in_bounds(p) and self.is_impediment(p):
        valid_neighbors.append(p)
    #print(self.impediment[0])
    #print(type(valid_neighbors[0]))
    return valid_neighbors
                  
        
class SearchAlg:
  def __init__(self, grid, amountGas, start, goal):
    self.grid = grid
    self.start = start
    self.goal = goal
    self.amountGas = amountGas
    self.came_from = {}

  def trace_path(self):
    curr = self.goal
    path = []
    curr_gas = self.amountGas

    while curr != self.start:      
      path.append(curr)
      curr = self.came_from[curr]
    path.append(self.start)
    path.reverse()

    curr_gas += 1
    for v in path:
      curr_gas -= 1
      #print(self.amountGas)
      if(curr_gas == -1):
        path.clear()
      else:
        if(self.grid.is_gas(v) == False):
          curr_gas = self.amountGas     
    return path

  def heuristic(self, p1, p2, heu_type="Manhanttan"):
    if heu_type == "Manhanttan":
      return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
    elif heu_type == "Euclidean":
      return math.sqrt(pow(p2[0]-p1[0],2) + pow(p2[1]-p1[1],2))
    return sys.maxsize # return maximun number

  def BFS(self):
    openSet = Queue()
    openSet.push(self.start)
    
    self.came_from = {}
    visited = list(self.start)

    while not openSet.is_empty():
      curr_node = openSet.pop()          
      
      if curr_node == self.goal:            
        path = self.trace_path()
        return path
        
      for next_node in self.grid.neighbors(curr_node):        
        if next_node not in visited:          
          self.came_from[next_node] = curr_node
          visited.append(next_node)
          openSet.push(next_node)   
          
    print(colored("Can not find!!!", "red"))
    return False

  def DFS(self):
    openSet = Stack()
    openSet.push(self.start)

    self.came_from = {}
    visited = list(self.start)

    while not openSet.is_empty():
      curr_node = openSet.pop()     
      
      if curr_node == self.goal:
        path = self.trace_path()
        if not path:
          print(colored("Can not find!!!", "red"))
          return False
        # self.grid.draw(path=path)
        # print(colored("Finded goal.", "green"))  
        # return True

      for next_node in self.grid.neighbors_DFS(curr_node):        
        if next_node not in visited:
          self.came_from[next_node] = curr_node        
          visited.append(next_node)
          openSet.push(next_node)
          
    print(colored("Can not find!!!", "red"))
    return False

  def UCS(self):
    openSet = PriorityQueue()

    openSet.push(0, self.start)
    self.came_from = {}
    gScore = {self.start:0}

    while not openSet.is_empty():
      curr = openSet.pop()

      curr_cost, curr_node = curr
        
      if curr_node == self.goal:            
        path = self.trace_path()

        if not path:
          print(colored("Can not find!!!", "red"))
          print(gScore[0])
          return False

        # self.grid.draw(path=path)
        # print(colored("Finded goal.", "green"))  
        # return True
      
      for next_pos in self.grid.neighbors(curr_node):     
        new_g = gScore[curr_node] + 1
        if next_pos not in gScore or new_g < gScore[next_pos]:
          gScore[next_pos] = new_g
          openSet.push(new_g, next_pos)
          self.came_from[next_pos] = curr_node

    print(colored("Can not find!!!", "red"))
    return False 

  def a_star(self):
    openSet = PriorityQueue()
    # push a element to priority queue (F, label)
    openSet.push(0, self.start)
    self.came_from = {}
    gScore = {self.start:0}

    while not openSet.is_empty():
      curr = openSet.pop()
      curr_cost, curr_node = curr
     
      if curr_node == self.goal:            
        path = self.trace_path()

        if not path:
          print(colored("Can not find!!!", "red"))
          return False

        # self.grid.draw(path=path)
        # print(colored("Finded goal.", "green"))  
        # return True

      for next_pos in self.grid.neighbors(curr_node):
        new_g = gScore[curr_node] + 1
        if next_pos not in gScore or new_g < gScore[next_pos]:
          gScore[next_pos] = new_g
          new_f = new_g + self.heuristic(next_pos,self.goal)
          openSet.push(new_f, next_pos)
          self.came_from[next_pos] = curr_node

    print(colored("Can not find!!!", "red"))
    return False 
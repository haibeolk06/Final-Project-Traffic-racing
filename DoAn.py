import pygame
import random, time,os

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
    # print(neighbors)
    valid_neighbors = []
    for p in neighbors:
      if self.in_bounds(p) and self.is_impediment(p):
        valid_neighbors.append(p)
    #print(self.impediment[0])
    #print(type(valid_neighbors[0]))
    return valid_neighbors

  def draw(self, path=[]):
    for i in range(self.m):
      for j in range(self.m):
        if (i,j) in path:
          screen.blit(Flag,(50 + 40 , 50 + 40 ))    
    pygame.display.flip()       


class SearchAlg:
  def __init__(self, grid, start, goal):
    self.grid = grid
    self.start = start
    self.goal = goal
    self.came_from = {}

  def trace_path(self):
    curr = self.goal
    path = []
    while curr != self.start:
      path.append(curr)
      curr = self.came_from[curr]
    path.append(self.start)
    path.reverse()

    print(f"Duong di tu {self.start} -> {self.goal}: ", end="")
    for v in path:
      print(f"{v}", end=" ")
    return path

  def BFS(self):
    openSet = Queue()
    openSet.push(self.start)

    self.came_from = {}
    visited = list(self.start)

    while not openSet.is_empty():
      curr_node = openSet.pop()

      if curr_node == self.goal:
        print(colored("Finded goal.", "green"))       
        path = self.trace_path() # Remove path = None
        print()
        self.grid.draw(path=path)
        return True

      for next_node in self.grid.neighbors(curr_node):        
        if next_node not in visited:
          self.came_from[next_node] = curr_node
          visited.append(next_node)
          openSet.push(next_node)   
          
          
    print(colored("Can not find!!!", "red"))
    return False


#khoi tao game
pygame.init()
#mau nen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = ( 255, 255, 102)

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill(WHITE)

#tieu de
pygame.display.set_caption("Traffic racing")

done = False
#toa do
Destination=[] # vi tri dich den
AmountOfImpediment=0 #so luong vat can
Impediment=[] #toa do vat can
AmountOfGasStation=0 #so luong cay xang
GasStation=[] #toa do cay xang
AmountOfGas=0 #so lit xang
MatrixSize=0 #kích thước ma trận mXm

#tai anh len
GasStationImage=pygame.transform.scale(pygame.image.load(os.path.join('.\\gasstation.png')),(38,38))
Flag=pygame.transform.scale(pygame.image.load(os.path.join('.\\destination.png')),(38,38)) 
BarrierImage=pygame.transform.scale(pygame.image.load(os.path.join('.\\traffic-barrier.png')),(38,38)) 
Racer=pygame.transform.scale(pygame.image.load(os.path.join('.\\racer.png')),(38,38)) 

#doc file
f=open('.\\map.txt','r+')
Data=f.readlines()

AmountOfGas=int(Data[0])
MatrixSize=int(Data[1])

for i in range(2,len(Data)):    
    if(Data[i].strip().upper()=='BARRIER'):
        AmountOfImpediment=int(Data[i+1])
        for j in range(i+2,len(Data)):
            if Data[j].upper().strip() !='GAS STATION':
                Impediment.append(Data[j].strip().split())                
            else:
                break
    if(Data[i].upper().strip()=='GAS STATION'):
        AmountOfGasStation=int(Data[i+1])
        for j in range(i+2,len(Data)):
            if Data[j].upper().strip() !='BARRIER' and Data[j].upper().strip() !='DESTINATION':
                GasStation.append(Data[j].strip().split())
            else:
                break
    if(Data[i].upper().strip()=='DESTINATION'):
        Destination.append(Data[i+1].strip().split())
        break
f.close()





#hien du lieu
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.blit(Racer, [50, 50])

    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, BLACK, [50 + 40 * j, 50 + 40 * i, 40, 40], 1)

    for i in range(len(Impediment)):
        screen.blit(BarrierImage, [50 + 40 * int(Impediment[i][1]), 50 + 40 * int(Impediment[i][0])])
        Impediment[i][1] = int(Impediment[i][1])
        Impediment[i][0] = int(Impediment[i][0])
        

    for i in range(len(GasStation)):
        screen.blit(GasStationImage,(50 + 40 * int(GasStation[i][1]), 50 + 40 * int(GasStation[i][0])))
    
    screen.blit(Flag,(50 + 40 * int(Destination[0][1]), 50 + 40 * int(Destination[0][0])))
    
    pygame.display.flip()
#end
#pygame.quit()




#Impediment[0] = tuple(Impediment[0])
for i in range(len(Impediment)):
  Impediment[i] = tuple(Impediment[i])

g = Grid(MatrixSize, Impediment, GasStation)
#print(Impediment)
search = SearchAlg(g, (0,0), (9,9))
print("\n-------- BFS --------")
search.BFS()




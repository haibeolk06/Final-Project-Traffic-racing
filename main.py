import pygame
import random, time,os
import os
import collections
import sys
import math
from termcolor import colored

import search

#khoi tao game
pygame.init()
#mau nen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = ( 255, 255, 102)
GREY = (200, 207, 202)

size = (500, 500)
screen = pygame.display.set_mode(size)
screen.fill(WHITE)
font = pygame.font.SysFont('sans',22)
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

for i in range(len(Impediment)):
  Impediment[i][0] = int(Impediment[i][0])
  Impediment[i][1] = int(Impediment[i][1])
  Impediment[i] = tuple(Impediment[i])

for i in range(len(GasStation)):
  GasStation[i][0] = int(GasStation[i][0])
  GasStation[i][1] = int(GasStation[i][1])
  GasStation[i] = tuple(GasStation[i])

g = search.Grid(MatrixSize, Impediment, GasStation)
search = search.SearchAlg(g, AmountOfGas, (0,0), (9,9))
path = []

def draw():
  #for v in path:
  #screen.blit(Flag,(50 + 40 * v[1], 50 + 40 * v[0]))
  if(not path):
    return
  item = path.pop(0)
  screen.blit(Flag,(50 + 40 * item[1], 50 + 40 * item[0]))

FPS = 60
fpsClock = pygame.time.Clock()

#hien du lieu
while not done:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button==1 and mouse_x<95 and mouse_x>45 and mouse_y>5 and mouse_y<35:
            path = search.BFS()

          if event.button==1 and mouse_x<215 and mouse_x>165 and mouse_y>5 and mouse_y<35:
            path = search.DFS()

          if event.button==1 and mouse_x<335 and mouse_x>285 and mouse_y>5 and mouse_y<35:
            path = search.UCS() 

          if event.button==1 and mouse_x<450 and mouse_x>405 and mouse_y>5 and mouse_y<35:
            path = search.a_star()
            
          
          screen.fill(WHITE)
    draw()

    pygame.draw.rect(screen, GREY, [48,5,43,25])
    pygame.draw.rect(screen, GREY, [168,5,43,25])
    pygame.draw.rect(screen, GREY, [288,5,43,25])
    pygame.draw.rect(screen, GREY, [408,5,40,25])
    
    bfstext=font.render('BFS',True, BLACK)
    dfstext=font.render('DFS',True, BLACK)
    ucstext=font.render('UCS',True, BLACK)
    astarttext=font.render('A*',True, BLACK)
    
    screen.blit(bfstext,[51,5])
    screen.blit(dfstext,[170,5])
    screen.blit(ucstext,[290,5])
    screen.blit(astarttext,[410,5])
    
    screen.blit(Racer, [50, 50])
    

    for i in range(10):
        for j in range(10):
            pygame.draw.rect(screen, BLACK, [50 + 40 * j, 50 + 40 * i, 40, 40], 1)

    for i in range(len(Impediment)):
        screen.blit(BarrierImage, [50 + 40 * int(Impediment[i][1]), 50 + 40 * int(Impediment[i][0])])               

    for i in range(len(GasStation)):
        screen.blit(GasStationImage,(50 + 40 * int(GasStation[i][1]), 50 + 40 * int(GasStation[i][0])))      

    screen.blit(Flag,(50 + 40 * int(Destination[0][1]), 50 + 40 * int(Destination[0][0])))
    
    pygame.display.flip()
    fpsClock.tick(FPS)

#end
pygame.quit()
quit()





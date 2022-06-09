#from email.errors import FirstHeaderLineIsContinuationDefect
from math import dist
import pygame
import time
import numpy as np
import sys
import os, signal
import map
import random
import multiprocessing as mp
from commons import gameDisplay, green #carsManager, carsLock, cars, 
from car import car
pygame.init()


# carsManager = mp.Manager()
# carsLock = carsManager.Lock()
# cars = carsManager.list()
WIDTH, HEIGHT = 1920, 1080
carsPosManager = mp.Manager()
carsPosLock = carsPosManager.Lock()
carsPos = carsPosManager.list() #posX, posY, goingTo


num_of_intersections = 4
distance_between_intersections = 200
center_of_map = distance_between_intersections*num_of_intersections/2
offsetX = WIDTH/2 - center_of_map
offsetY = HEIGHT/2 - center_of_map #+ 100

map.map = map.generate_map(num_of_intersections, distance_between_intersections, offsetX, offsetY)
map.draw_map(map.map)
background = pygame.image.load("images/background.jpg")

# mapManager = mp.Manager()
# mapLock = mapManager.Lock()
Map = list() #mapManager.list(map.map)



def carProcess(fr,to, carsPosLoc, carsPosLockLoc, isPolice = False):
    redCar = car(fr,to, carsPosLoc, carsPosLockLoc, isPolice)
    while True:
        #gameDisplay.blit(redCar.image)
        #gameDisplay.blit(redCar.image, [redCar.posX, redCar.posY])
        redCar.move()
        time.sleep(0.015)

# def refreshScreenProcess():
#     while True:

def spawnCarsWithPolice():
    children = []
    for i in range(30):
        pid = os.fork()
        if pid == 0:
            f = random.randrange(len(map.map))
            print("f: ", f, " len(map.map): ", len(map.map))
            t = f
            while f == t:
                t = random.randrange(len(map.map))
            if i % 5 == 0:
                carProcess(f,t,carsPos,carsPosLock, True)
            else:
                carProcess(f,t, carsPos, carsPosLock)    #100,100,[Map[0], Map[2], Map[3], Map[1]])
            
            return
        children.append(pid)
    return children

def spawnCarsFrom1toN():
    children = []
    for i in range(30):
        time.sleep(0.3)
        pid = os.fork()
        if pid == 0:
            carProcess(0,len(map.map)-1, carsPos, carsPosLock)
            return
        children.append(pid)
    return children

def spawnCarsRightFree():
    children = []
    for i in range(2):
        time.sleep(0.2)
        pid = os.fork()
        if pid == 0:
            if(i == 0):
                carProcess(3,1, carsPos, carsPosLock)  
            elif(i == 1):
                carProcess(4,0, carsPos, carsPosLock)  
            # elif(i == 2):
            #     carProcess(0,4, carsPos, carsPosLock)  
            return
        children.append(pid)
    return children
def spawnCarsRightFree2():
    children = []
    for i in range(3):
        # time.sleep(0.1)
        pid = os.fork()
        if pid == 0:
            if(i == 0):
                carProcess(4,3, carsPos, carsPosLock)  
            elif(i == 1):
                carProcess(0,4, carsPos, carsPosLock)  
            elif(i == 2):
                carProcess(0,1, carsPos, carsPosLock)  
            return
        children.append(pid)
    return children
def spawnCarsNoLeftLock():
    children = []
    for i in range(2):
        # time.sleep(0.1)
        pid = os.fork()
        if pid == 0:
            if(i == 0):
                carProcess(1,4, carsPos, carsPosLock)  
            elif(i == 1):
                carProcess(3,0, carsPos, carsPosLock)  
            # elif(i == 2):
            #     carProcess(0,1, carsPos, carsPosLock)  
            return
        children.append(pid)
    return children
def spawnCarsNoLock():
    children = []
    for i in range(4):
        time.sleep(0.1)
        pid = os.fork()
        if pid == 0:
            if(i == 0):
                carProcess(1,3, carsPos, carsPosLock)  
            elif(i == 1):
                carProcess(0,4, carsPos, carsPosLock)  
            elif(i == 2):
                carProcess(3,1, carsPos, carsPosLock)  
            elif(i == 3):
                carProcess(4,0, carsPos, carsPosLock)  
            return
        children.append(pid)
    return children
def spawnCarsOneRoad():
    children = []
    for i in range(10):
        time.sleep(1)
        pid = os.fork()
        if pid == 0:
            carProcess(0,1,carsPos,carsPosLock)
            
            return
        children.append(pid)
    return children
def mapForShowcase():
    map.map = [
    #            name   position    neighbors    weights
    map.intersection("v0",  (50, 150),  [2],      [1]),
    map.intersection("v1",  (150, 50),  [2],      [1]),
    map.intersection("v2",  (150, 150),  [0, 1, 3, 4],[1,1,1,1]),
    map.intersection("v3",  (150, 250),  [2],      [1]),
    map.intersection("v4",  (250, 150),  [2],      [1]),

    ]

def mapForShowcase2():
    map.map = [
    #            name   position    neighbors    weights
    map.intersection("v0",  (50, 500),  [1],      [1]),
    map.intersection("v1",  (950, 500),  [0],      [1]),

    ]
    
    

def Main():
    print ("Kinga :)")
    print("map length: ", len(map.map))
    children = []
    scenario = 9
#   1 for showcase of police
#   2 for showcase of road weight update

#   4 for showcase of right free 1
#   5 for showcase of right free 2
#   6 for showcase of no blocking of left turns
#   7 for showcase of no blocking of 4 cars going straight

#   9 for one road showcase     
    if scenario == 1 or scenario == 2:
        map.map = map.generate_map(5, 200, 40, 40)
    elif scenario < 9:
        mapForShowcase()
    else:
        mapForShowcase2()

    map.draw_map(map.map)
    if scenario == 1:
        children.extend(spawnCarsWithPolice())
    elif scenario == 2:
        children.extend(spawnCarsFrom1toN())
    elif scenario == 4:
        children.extend(spawnCarsRightFree())
    elif scenario == 5:
        children.extend(spawnCarsRightFree2())
    elif scenario == 6:
        children.extend(spawnCarsNoLeftLock())
    elif scenario == 7:
        children.extend(spawnCarsNoLock())
    elif scenario == 9:
        children.extend(spawnCarsOneRoad())

    background = pygame.image.load("images/background.jpg")
    iterator = 0
    while True:
        iterator += 1
        # print(iterator)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for child in children:
                    os.kill(child, signal.SIGSTOP)
                sys.exit()
        if scenario == 9:
            # print ("a")
            if iterator == 300:
                # print("b")
                carsPosLock.acquire()
                temp = carsPos[1]
                temp[5] = 1 
                carsPos[1] = temp
                print("carsPos[0][5] ",carsPos[0][5])
                carsPosLock.release()
            elif iterator == 320:
                carsPosLock.acquire()
                temp = carsPos[1]
                temp[5] = 0
                carsPos[1] = temp
                carsPosLock.release()
                iterator = 0
        pygame.display.update()
        gameDisplay.blit(background, [0,0])
        #map.map.update_weights_of(map.map)
        # for child in children:
        #     signal.pidfd_send_signal(child, signal.SIGUSR1)
        time.sleep(0.04)
Main()
    
    
    
    

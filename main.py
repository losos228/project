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

def spawnCars():
    children = []
    for i in range(20):
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

def spawnCars2():
    children = []
    for i in range(10):
        time.sleep(0.5)
        pid = os.fork()
        if pid == 0:
            carProcess(0,len(map.map)-1, carsPos, carsPosLock)
            return
        children.append(pid)
    return children

def Main():
    print ("Kinga :)")
    print("map length: ", len(map.map))
    # pid = os.fork
    # if pid == 0:
    #     refreshScreenProcess()
    children = []
    # children.append(pid)
    children.extend(spawnCars2())
    

    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for child in children:
                    os.kill(child, signal.SIGSTOP)
                sys.exit()
        pygame.display.update()
        gameDisplay.blit(background, [0,0])
        #map.map.update_weights_of(map.map)
        # for child in children:
        #     signal.pidfd_send_signal(child, signal.SIGUSR1)
        time.sleep(0.02)
Main()
    
    
    
    

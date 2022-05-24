from email.errors import FirstHeaderLineIsContinuationDefect
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


carsManager = mp.Manager()
carsLock = carsManager.Lock()
cars = carsManager.list()

carsPosManager = mp.Manager()
carsPosLock = carsPosManager.Lock()
carsPos = carsPosManager.list() #posX, posY, goingTo

map.draw_window()
background = pygame.image.load("images/background.jpg")

# mapManager = mp.Manager()
# mapLock = mapManager.Lock()
Map = list() #mapManager.list(map.map)



def carProcess(fr,to, carsLoc, carsLockLoc, carsPosLoc, carsPosLockLoc):
    redCar = car(fr,to, carsLoc, carsLockLoc, carsPosLoc, carsPosLockLoc)
    while True:
        #gameDisplay.blit(redCar.image)
        #gameDisplay.blit(redCar.image, [redCar.posX, redCar.posY])
        redCar.move()
        time.sleep(0.02)


def Main():
    #pygame.display.update()
    print("map length: ", len(map.map))
    #redCar = car(100,100,[Map[0], Map[2], Map[3], Map[1]])
    children = []
    for i in range(10):
        pid = os.fork()
        if pid == 0:
            if i != 10:
                carProcess(i,10, cars, carsLock, carsPos, carsPosLock)    #100,100,[Map[0], Map[2], Map[3], Map[1]])
            else:
                carProcess(10,5, cars, carsLock, carsPos, carsPosLock)
            return
        children.append(pid)
    # pid = os.fork()
    # if pid == 0:
    #     carProcess(400,100,[Map[2], Map[3], Map[1], Map[0]])
    #     return
    # children.append(pid)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for child in children:
                    os.kill(child, signal.SIGSTOP)
                sys.exit()
        pygame.display.update()
        gameDisplay.blit(background, [0,0])
        # for child in children:
        #     signal.pidfd_send_signal(child, signal.SIGUSR1)
        time.sleep(0.02)
Main()
    
    
    
    

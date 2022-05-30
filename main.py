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


# carsManager = mp.Manager()
# carsLock = carsManager.Lock()
# cars = carsManager.list()

carsPosManager = mp.Manager()
carsPosLock = carsPosManager.Lock()
carsPos = carsPosManager.list() #posX, posY, goingTo

map.map = map.generate_map(3, 200, 40, 40)
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
        time.sleep(0.019)


def Main():
    #pygame.display.update()
    print("map length: ", len(map.map))
    #redCar = car(100,100,[Map[0], Map[2], Map[3], Map[1]])
    children = []
    for i in range(10):
        pid = os.fork()
        if pid == 0:
            f = random.randrange(len(map.map))
            print("f: ", f, " len(map.map): ", len(map.map))
            t = f
            while f == t:
                t = random.randrange(len(map.map))
            # if (i == 0):
            #     f = 6
            #     t = 2
            # if (i == 1):
            #     f = 0
            #     t = 2
            if i == 8:
                carProcess(f,t,carsPos,carsPosLock, True)
            else:
                carProcess(f,t, carsPos, carsPosLock)    #100,100,[Map[0], Map[2], Map[3], Map[1]])
            
            return
        children.append(pid)
    # pid = os.fork()
    # if pid == 0:
    #     carProcess(400,100,[Map[2], Map[3], Map[1], Map[0]])
    #     return
    # children.append(pid)
    # pid = os.fork()
    # if pid == 0:
    #     f = random.randrange(len(map.map))
    #     print("f: ", f, " len(map.map): ", len(map.map))
    #     t = f
    #     p = car(f,t, carsPos, carsPosLock, True)
    #     while True:
    #         p.move()
    #         time.sleep(0.19)

    
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
    
    
    
    

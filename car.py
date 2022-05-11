from math import dist
import pygame
import time
import numpy as np
import sys
import os, signal
import map
pygame.init()

green = (34,139,34)
#red = (255,0,0)
gameDisplay = pygame.display.set_mode((900,500))

map.draw_window()
background = pygame.image.load("images/background.jpg")


def distance(fr, to):
    return np.sqrt((fr[0]-to[0])**2+(fr[1]-to[1])**2)

def diffWithin(a, b, maxDif):
    return np.abs(a-b) <= maxDif

class car(pygame.sprite.Sprite):
    def __init__(self, posX, posY, road):
        self.image = pygame.image.load("images/redCar.png")
        self.posX = posX
        self.posY = posY
        self.road = road
        self.roadStep = 0
        self.nextStep = road[0]
        self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
        self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
        self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])

        #super().__init__(*groups)
    def render(self, screen):
        screen.blit(self.image, (self.posX, self.posY))
    
    def move(self):
        if(self.roadStep > len(self.road)-1):
            print("finished pid: ",os.getpid())
            self.roadStep = 0
            self.nextStep = self.road[0]
            self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
            self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
            
        else:
            #moved = 0
            # print("posX: ",self.posX)
            # print("posY: ",self.posY)
            # print("dirX: ",self.dirX)
            # print("dirY: ",self.dirY)
            #pygame.draw.rect(gameDisplay, green, pygame.Rect(self.posX, self.posY, 50, 20))
            if(not diffWithin(self.posX, self.nextStep["position"][0], self.currRoadLen*0.05)):
                # print ("a")
                self.posX = self.posX+self.dirX
                #moved = 1
            if(not diffWithin(self.posY, self.nextStep["position"][1], self.currRoadLen*0.05)):
                # print ("b")
                self.posY = self.posY+self.dirY
                #moved = 1
            if(diffWithin(self.posY, self.nextStep["position"][1], self.currRoadLen*0.05) and diffWithin(self.posX, self.nextStep["position"][0], self.currRoadLen*0.05)):
                # print("c")
                self.posX = self.nextStep["position"][0]
                self.posY = self.nextStep["position"][1]
                self.roadStep = self.roadStep+1
                self.nextStep = self.road[self.roadStep]
                if(self.roadStep <= len(self.road)-1):
                    # print("d")
                    self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            gameDisplay.blit(self.image, [self.posX, self.posY])
def carProcess(posX,posY,road):
    redCar = car(posX,posY,road)
    while True:
        #gameDisplay.blit(redCar.image)
        #gameDisplay.blit(redCar.image, [redCar.posX, redCar.posY])
        redCar.move()
        time.sleep(0.05)


def Main():
    #pygame.display.update()
    children = []
    pid = os.fork()
    if pid == 0:
        carProcess(100,100,[map.map["v1"], map.map["v3"], map.map["v4"], map.map["v2"]])
        return
    children.append(pid)
    pid = os.fork()
    if pid == 0:
        carProcess(400,100,[map.map["v3"], map.map["v4"], map.map["v2"], map.map["v1"]])
        return
    children.append(pid)
    
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
        time.sleep(0.05)
Main()
    
    
    
    

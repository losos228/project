from email.errors import FirstHeaderLineIsContinuationDefect
from math import dist
import pygame
import time
import numpy as np
import sys
import os, signal
import map
import random
pygame.init()

cars = []

green = (34,139,34)
#red = (255,0,0)
gameDisplay = pygame.display.set_mode((900,500))

map.draw_window()
background = pygame.image.load("images/background.jpg")


def distance(fr, to):
    dist = np.sqrt((fr[0]-to[0])**2+(fr[1]-to[1])**2)
    if dist != 0:
        return dist
    else:
        return 0.001

def diffWithin(a, b, maxDif):
    return np.abs(a-b) <= maxDif

class car(pygame.sprite.Sprite):
    def __init__(self, fr, to):
        self.id = len(cars)
        cars.append(self)
        self.calculateRoute(fr, to)
        self.image = pygame.image.load("images/redCar.png")
        self.posX = self.road[0]["position"][0]
        self.posY = self.road[0]["position"][1]
       # self.road = road
        self.roadStep = 1
        self.nextStep = self.road[1]
        self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
        self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
        self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])

        #super().__init__(*groups)
    def render(self, screen):
        screen.blit(self.image, (self.posX, self.posY))
    
    def calculateRoute(self, fr, to):
        self.destination = to
        #dijkstra's algorithm
        #map.map[fr]

        table = [[0 for x in range(4)] for y in range(len(map.map))] #vertex, cost, previous, visited

        for i in range(len(map.map)):
            table[i][0] = i
            table[i][1] = 99999999999#np.Infinity
            table[i][2] = -1
            table[i][3] = 0
        table[fr][1] = 0
        curr = fr
        next = fr
        routeFound = 0
        print("route for: ",os.getpid())
        print("fr: ",fr)
        print("to: ", to)
        # print("first table:")
        # print(table)
        while not routeFound:
            table[curr][3] = 1
            minDist = np.Infinity
            # currentIntersection = map.map[curr]
            for neighbour in map.map[curr]["neighbors"]:
                dist = distance(map.map[curr]["position"], map.map[neighbour]["position"])
                if(table[neighbour][1] > table[curr][1]+dist and table[neighbour][3]!= 1):
                    if neighbour == to:
                        routeFound = 1
                    table[neighbour][1] = table[curr][1]+dist
                    table[neighbour][2] = curr
            for int in range(len(map.map)):
                # dist = intersection[1]
                if table[int][1] < minDist and table[int][3] != 1:
                    minDist = table[int][1]
                    next = int
            curr = next
            # print("table:")
            # print(table)
        curr = to
        self.road = []
        while curr != -1:
            self.road.insert(0,map.map[curr])
            curr = table[curr][2]
        #self.road = self.road.reverse()
        self.roadStep = 0
        self.nextStep = self.road[1]

        

    def move(self):
        if(self.roadStep > len(self.road)-1):
            # print("finished pid: ",os.getpid())
            # self.nextStep = self.road[0]
            to = random.randrange(len(map.map))
            while to == self.destination:
                to = random.randrange(len(map.map))
            self.calculateRoute(self.destination, to)
            self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            print("distance ", distance((self.posX, self.posY), self.nextStep["position"]))
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
                if(self.roadStep <= len(self.road)-1):
                    self.nextStep = self.road[self.roadStep]
                    #self.road[self.roadStep-1].removeFromOutgoing(self.id, )
                    # print("d")
                    self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            gameDisplay.blit(self.image, [self.posX, self.posY])

def carProcess(fr,to):
    redCar = car(fr,to)
    while True:
        #gameDisplay.blit(redCar.image)
        #gameDisplay.blit(redCar.image, [redCar.posX, redCar.posY])
        redCar.move()
        time.sleep(0.02)


def Main():
    #pygame.display.update()
    print("map length: ", len(map.map))
    #redCar = car(100,100,[map.map[0], map.map[2], map.map[3], map.map[1]])
    children = []
    for i in range(5):
        pid = os.fork()
        if pid == 0:
            if i != 4:
                carProcess(i,4)    #100,100,[map.map[0], map.map[2], map.map[3], map.map[1]])
            else:
                carProcess(5,4)
            return
        children.append(pid)
    # pid = os.fork()
    # if pid == 0:
    #     carProcess(400,100,[map.map[2], map.map[3], map.map[1], map.map[0]])
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
    
    
    
    

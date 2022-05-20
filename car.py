#from math import dist
from commons import distance, diffWithin, gameDisplay
import pygame
# import time
import numpy as np
# import sys
import os#,signal
import map
import random
import multiprocessing as mp


class car(pygame.sprite.Sprite):
    def __init__(self, fr, to, cars, carsLock):
        with carsLock:
            self.id = len(cars)
            print("\nid: ", self.id)
            cars.append(self)
            
       # print("cars len: ", len(cars))
   #     print("cars: ", cars)
        #with mapLock: 
        # while True:
        #     try:
        #         print("a")
        #         mapLock.acquire()
        #         self.calculateRoute(fr, to, Map, mapLock)
        #         mapLock.release()
        #         print("b")
        #         break
        #     except:
        #         pass
        
        self.calculateRoute(fr, to)
        
        #mapLock = mapLock
        #self.Map = Map
        self.image = pygame.image.load("images/redCar.png")
        self.posX = map.map[self.road[0]]["position"][0]
        self.posY = map.map[self.road[0]]["position"][1]
       # self.road = road
        self.roadStep = 1
        self.nextStep = map.map[self.road[1]]
        self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
        self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
        self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
        self.addedToOutgoing = 0
        print("init finished")

        #super().__init__(*groups)
    def render(self, screen):
        screen.blit(self.image, (self.posX, self.posY))
    
    def calculateRoute(self, fr, to):
        self.destination = to
        #dijkstra's algorithm
        #Map[fr]

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
            # with map.mapLock:
            for neighbour in range(len(table)):
                #print("neighbour: ",neighbour )
                #if(table[neighbour][1]!= 99999999999):
                if neighbour in map.map[curr]["neighbors"]:
                    dist = distance(map.map[curr]["position"], map.map[table[neighbour][0]]["position"])
                    if(table[neighbour][1] > table[curr][1]+dist and table[neighbour][3]!= 1):
                        if neighbour == to:
                            routeFound = 1
                        table[neighbour][1] = table[curr][1]+dist
                        table[neighbour][2] = curr
            # print("curr: ", curr)
            # print("curr neighbors: ", map.map[curr]["neighbors"])
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
            self.road.insert(0,curr)
            curr = table[curr][2]
        #self.road = self.road.reverse()
        self.roadStep = 1
        self.nextStep = map.map[self.road[1]]
        print("calculate route finished")
        print(self.road)

        

    def move(self):
        if(self.roadStep > len(self.road)-1):
            # print("a")
            # print("finished pid: ",os.getpid())
            # self.nextStep = self.road[0]
            to = random.randrange(len(map.map))
            while to == self.destination:
                to = random.randrange(len(map.map))
            #with mapLock:
            # while True:
            #     try:
            #         mapLock.acquire()
            #         self.calculateRoute(self.destination, to, Map, mapLock)
            #         mapLock.release()
            #         break
            #     except:
            #         pass
            
            self.calculateRoute(self.destination, to)
                       
            
            self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            print("distance ", distance((self.posX, self.posY), self.nextStep["position"]))
            self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
            self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
            
        else:

            if not self.addedToOutgoing:
                map.map[self.road[self.roadStep-1]].addOutgoing(self.id, self.road[self.roadStep])
                self.addedToOutgoing = 1
            #moved = 0
            # print("posX: ",self.posX)
            # print("posY: ",self.posY)
            # print("dirX: ",self.dirX)
            # print("dirY: ",self.dirY)
            #pygame.draw.rect(gameDisplay, green, pygame.Rect(self.posX, self.posY, 50, 20))
            # if not self.addedToOutgoing:
            #     Map[self.roadStep].addOutgoing(self.id, self.road[self.roadStep])
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
                print("aaa")

                if self.addedToOutgoing:
                    map.map[self.road[self.roadStep-1]].removeFromOutgoing(self.id, self.road[self.roadStep])
                    self.addedToOutgoing = 0
                print("bbbb")
                self.posX = self.nextStep["position"][0]
                self.posY = self.nextStep["position"][1]
                self.roadStep = self.roadStep+1
                    #         pass
                if(self.roadStep <= len(self.road)-1):
                    
                    # while True:
                    #     try:
                    #         with mapLock:
                    #             self.nextStep = Map[self.road[self.roadStep]]
                    #             mapLock.release()
                    #             break
                    #     except:
                    #         pass
                    self.nextStep = map.map[self.road[self.roadStep]]
                    # print("d")
                    self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])
                    self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            gameDisplay.blit(self.image, [self.posX, self.posY])

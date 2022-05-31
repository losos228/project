#from math import dist
from commons import distance, diffWithin, gameDisplay
import pygame
# import time
import numpy as np
# import sys
from math import sqrt
import os#,signal
import map
import random
import multiprocessing as mp


class car(pygame.sprite.Sprite):
    def __init__(self, fr, to, carsPos, carsPosLock, isPolice):
        # carsLock.acquire()
        # self.id = len(cars)
        #     # print("\nid: ", self.id)
        # cars.append(self)
        # carsLock.release()
        carsPosLock.acquire()
        self.id = len(carsPos)
        carsPos.append([0,0,0,0,[]]) #posX, posY, next, stoppedByPolice
            # print("carsPos at start: ", carsPos)
        carsPosLock.release()
        

        self.isPolice = isPolice
        print("self.isPolice: ", self.isPolice)
        
        self.calculateRoute(fr, to)
        
        self.carsPosLock = carsPosLock
        self.carsPos = carsPos

        self.length = 30
        self.height = 15 

        self.posX = map.map[self.road[0]]["position"][0]
        self.posY = map.map[self.road[0]]["position"][1]

        self.carsPosLock.acquire()
        temp = self.carsPos[self.id]
        temp[0] = self.posX
        temp[1] = self.posY
        temp[2] = self.road[self.roadStep]
        temp[3] = 0
        temp[4] = []
        self.carsPos[self.id] = temp
        self.carsPosLock.release()

        self.roadStep = 1
        self.nextStep = map.map[self.road[1]]
        
        self.FONT = pygame.font.SysFont('arial', 10)

        self.changeDirection()
        
        self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
        self.addedToOutgoing = 0
        self.prev = None


        self.stoppedByRightBusy = False
        self.stoppedByNoLeaveSpace = False
        self.stoppedByNoMoveSpace = False
        self.stoppedByPolice = False

        self.count = 5
        print("init finished")

        #renders the car with an offset as to be placed in the apropriate place
    def render(self):
        """
        ----------------------------------------------------
        Function to:
        Render the car on the screen
        ----------------------------------------------------
        Parameters:
        None
        ----------------------------------------------------
        Returns:
        None
        ----------------------------------------------------
        """
        # if not self.isPolice:
        if not self.stoppedByPolice:
            gameDisplay.blit(self.surf, [self.posX-(self.height*0.5*self.dirY)-0.4*self.height, self.posY+(self.height*0.5*self.dirX)-0.4*self.height])
        else:
            gameDisplay.blit(self.surf, [self.posX-(self.height*1.5*self.dirY)-0.4*self.height, self.posY+(self.height*1.5*self.dirX)-0.4*self.height])
        # else:
        #     gameDisplay.blit(self.surf, [self.posX-(self.height*0.5*self.dirY)-0.4*self.height, self.posY+(self.height*0.5*self.dirX)-0.4*self.height])


    def stopOtherCars(self):
        

        if self.roadStep < len(self.road) and self.roadStep > 0:
            self.carsPosLock.acquire()
            toStop = map.map[self.road[self.roadStep-1]].getAllOnRoadTo(self.road[self.roadStep])
            print("toStop: ", toStop)
            for c in range(len(toStop)):
                # print("toStop[c] {",toStop[c][0],"}")
                if toStop[c][0] != self.id:
                    toSet = toStop[c][0]
                    # print("A police stopping {",toSet,"} self.carsPos[",toSet,"][3] is {", self.carsPos[toSet][3], "} toSet is {", toSet,"}")
                    temp = self.carsPos[toSet]
                    temp[3] = 1 #not self.carsPos[toSet][4]
                    self.carsPos[toSet] = temp
                    # self.carsPos[toSet][2] = self.carsPos[toSet][2] +len(map.map)
                    # print("self.carsPos[toSet] {",self.carsPos[toSet],"}")
                    # print("B police stopping {",toSet,"} self.carsPos[",toSet,"][3] is {", self.carsPos[toSet][3], "} toSet is {", toSet,"}")


            self.carsPosLock.release()
    def startOtherCars(self):
        if self.roadStep > 0:
            self.carsPosLock.acquire()
            toStart = map.map[self.road[self.roadStep-1]].getAllOnRoadTo(self.road[self.roadStep])
            # print("toStart: ", toStart)
            for c in range(len(toStart)):
                # print("toStart[c] {",toStart[c][0],"}")
                if toStart[c][0] != self.id:
                    toSet = toStart[c][0]
                    # print("A police stopping {",toSet,"} self.carsPos[",toSet,"][3] is {", self.carsPos[toSet][3], "} toSet is {", toSet,"}")
                    temp = self.carsPos[toSet]
                    temp[3] = 0 #not self.carsPos[toSet][4]
                    self.carsPos[toSet] = temp
                    # self.carsPos[toSet][2] = self.carsPos[toSet][2] +len(map.map)
                    # print("self.carsPos[toSet] {",self.carsPos[toSet],"}")
                    # print("B police stopping {",toSet,"} self.carsPos[",toSet,"][3] is {", self.carsPos[toSet][3], "} toSet is {", toSet,"}")
            self.carsPosLock.release()


    def changeDirection(self):
        """
        ----------------------------------------------------
        Function to:
        Change the direction of movement and rotate the car 
            surface in the apropriate direction 
        ----------------------------------------------------
        Parameters:
        None
        ----------------------------------------------------
        Returns:
        None
        ----------------------------------------------------
        """

        if self.isPolice:
                    self.stopOtherCars()
        self.posX = map.map[self.road[self.roadStep-1]]["position"][0]
        self.posY = map.map[self.road[self.roadStep-1]]["position"][1]

        self.carsPosLock.acquire()
        temp = self.carsPos[self.id]
        temp[0] = self.posX
        temp[1] = self.posY
        temp[2] = self.road[self.roadStep]
        self.carsPos[self.id] = temp
        self.carsPosLock.release()


        self.dirX = (self.nextStep["position"][0]-self.posX)/distance((self.posX, self.posY), self.nextStep["position"])
        self.dirY = (self.nextStep["position"][1]-self.posY)/distance((self.posX, self.posY), self.nextStep["position"])

        angle = np.angle(self.dirX-self.dirY*1.0j, deg=True)

        if not self.isPolice:
            self.surf = pygame.Surface((self.length, self.height))
        else:
            self.surf = pygame.Surface((self.length/2, self.height))
        self.surf.set_colorkey((0,0,0)) 
        self.surf.fill(self.color)
        self.surf.blit(self.FONT.render(str(self.id), True, (255-self.color[0], 255-self.color[1], 255-self.color[2]) ), (0,0))
        self.surf = pygame.transform.rotate(self.surf, angle)

    def calculateRoute(self, fr, to):
        """
        ----------------------------------------------------
        Function to:
        Caclulate the best route from point A (fr) to 
        point B (to). Uses Dikstra's algorithm.
        ----------------------------------------------------
        Parameters:
        fr(int): the intersection from which to start from
        to(int): the intersection on which to end at
        ----------------------------------------------------
        Returns:
        None, the route is saved in self.road
        ----------------------------------------------------
        """
        self.destination = to
        #dijkstra's algorithm
        #Map[fr]

        table = [[0 for x in range(4)] for y in range(len(map.map))] #vertex, cost, previous, visited

        for i in range(len(map.map)):
            # table.append([i,99999999999,-1,0])
            table[i][0] = i
            table[i][1] = 99999999999#np.Infinity
            table[i][2] = -1
            table[i][3] = 0
        # print("fr: ",fr, " table len: ", len(table))
        table[fr][1] = 0
        curr = fr
        next = fr
        routeFound = 0
        # print("route for: ",os.getpid())
        # print("fr: ",fr)
        # print("to: ", to)
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
                    weight = map.map[curr].getWeight(neighbour)#distance(map.map[curr]["position"], map.map[table[neighbour][0]]["position"])
                    if(table[neighbour][1] > table[curr][1]+weight and table[neighbour][3]!= 1):
                        if neighbour == to:
                            routeFound = 1
                        table[neighbour][1] = table[curr][1]+weight
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
        # print("calculate route finished")
        # print(self.road)
        self.color = map.map[to].color

    def checkRightFree(self, roadStep): #returns True if the carr should stop, false if it should keep going
        """
        ----------------------------------------------------
        Function to:
        Check whether to stop the car from going on the 
        intersection based on the right hand free rule.
        ----------------------------------------------------
        Parameters:
        roadStep(int): the roadStep which to check.
        ----------------------------------------------------
        Returns:
        bool: if True the car can't enter the intersection
        if False the car can enter the intersection.
        ----------------------------------------------------
        """
        distanceVar = distance(map.map[self.road[roadStep-1]]["position"],map.map[self.road[roadStep]]["position"])
        Xdif = (map.map[self.road[roadStep-1]]["position"][0]-map.map[self.road[roadStep]]["position"][0])/distanceVar
        Ydif = (map.map[self.road[roadStep-1]]["position"][1]-map.map[self.road[roadStep]]["position"][1])/distanceVar
        angleFrom = np.angle(Xdif-Ydif*1.0j, deg=True)
        if angleFrom < 0:
            angleFrom += 360

        distanceVar = distance(map.map[self.road[roadStep-1]]["position"],map.map[self.road[roadStep]]["position"])
        Xdif = (map.map[self.road[roadStep+1]]["position"][0]-map.map[self.road[roadStep]]["position"][0])/distanceVar
        Ydif = (map.map[self.road[roadStep+1]]["position"][1]-map.map[self.road[roadStep]]["position"][1])/distanceVar
        angleTo = np.angle(Xdif-Ydif*1.0j, deg=True)
        if angleTo < 0:
            angleTo += 360
        # print("angleFrom: ", angleFrom)
        # print("angleTo: ", angleTo)
        # print(self.road[roadStep], ":")
        for neighbor in map.map[self.road[roadStep]].neighborsFrom:
            check = False
            distanceVar = distance(map.map[neighbor]["position"],self.nextStep["position"])
            Xdif = (map.map[neighbor]["position"][0]-map.map[self.road[roadStep]]["position"][0])/distanceVar# formula for x difference
            Ydif = (map.map[neighbor]["position"][1]-map.map[self.road[roadStep]]["position"][1])/distanceVar# forumla for y difference
            angle = np.angle(Xdif-Ydif*1.0j, deg = True)
            if angle < 0: #if the angle is bigger than 180 it will be negative
                angle += 360
            # print(" ", neighbor, " : ", angle)
            if neighbor != self.road[roadStep-1]:
                if neighbor != self.road[roadStep+1]:
                    if(angleFrom < angleTo):
                        if(angle > angleFrom and angle < angleTo):
                            # print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep]," checkA ", neighbor)
                            # print("         angleFrom: ", angleFrom, " angleTo: ", angleTo, " angle: ", angle)
                            check = True
                        # else:
                        #     print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep]," not checkA ", neighbor)
                        #     print("         angleFrom: ", angleFrom, " angleTo: ", angleTo, " angle: ", angle)
                    else:
                        if(angle > angleFrom or angle < angleTo):
                            # print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep]," checkB ", neighbor)
                            # print("         angleFrom: ", angleFrom, " angleTo: ", angleTo, " angle: ", angle)
                            check = True
                        # else:
                        #     print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep]," not checkB ", neighbor)
                        #     print("         angleFrom: ", angleFrom, " angleTo: ", angleTo, " angle: ", angle)
            #     else:
            #         print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep], " ", neighbor, " equal ", self.road[roadStep+1])
            # else:
            #     print("     going from: ", self.road[roadStep-1], " to: ", self.road[roadStep+1], " through: ",self.road[roadStep], " ", neighbor, " equal ", self.road[roadStep-1])
            if check:
                car = map.map[neighbor].getFirstOnRoadTo(self.road[roadStep])
                if car != None:
                    self.carsPosLock.acquire()
                    if distance(self.carsPos[car], map.map[self.road[roadStep]]["position"]) < self.length * 6:

                        if self.carsPos[car][4].count(self.id) > 0:
                            print (self.id, " blocking car (by right hand rule) ",car," blocked by me ")
                            return False
                        temp = self.carsPos[self.id]
                        temp[4].append(car)
                        self.carsPos[self.id] = temp
                        self.carsPosLock.release()
                        # print("Id: ",self.id, " Stoping because right hand not free"," self.prev: ",self.prev)
                        return True
                    # else:
                        # print("aaaa")
                        # print("distance of the car on the right to the intersection",distance(self.carsPos[car], map.map[self.road[roadStep]]["position"]))
                    self.carsPosLock.release()
                # else:
                    # print("Id: ",self.id," no car on right")
        # print(map.map[self.road[roadStep]].neighborsFrom)
        return False

    def checkLeaveSpace(self, roadStep):
        """
        ----------------------------------------------------
        Function to:
        Check wether there is suitable space to leave the 
        intersection
        ----------------------------------------------------
        Parameters:
        roadStep(int): the roadStep which to check.
        ----------------------------------------------------
        Returns:
        bool: if True the car can't enter the intersection
        if False the car can enter the intersection.
        ----------------------------------------------------
        """
        if roadStep >= 0 and roadStep < len(self.road)-1:
            lastOn = map.map[self.road[roadStep]].getLastOnRoadTo(self.road[roadStep+1], self.id)
            # self.prev = lastOn
            self.carsPosLock.acquire()
            if lastOn != None and distance(self.carsPos[lastOn], map.map[self.road[roadStep]]["position"]) < self.length *1.2:
                if self.carsPos[lastOn][4].count(self.id) > 0:
                    
                    self.carsPosLock.release()
                    print ("\n",self.id, " blocking car ",lastOn," blocked by me")
                    return False
                temp = self.carsPos[self.id]
                temp[4].append(lastOn)
                self.carsPos[self.id] = temp
                self.carsPosLock.release()
                # print("Id: ",self.id, " No space to leave intersection! intersection: ", self.road[roadStep] ,
                # "\n lastOn: ", lastOn, " distance to intersecton: ",distance(self.carsPos[lastOn], map.map[self.road[roadStep]]["position"]))
                print( self.id, " LastOn: ", lastOn)
                return True
            temp = self.carsPos[self.id]
            temp[4] = []
            self.carsPos[self.id] = temp
            self.carsPosLock.release()
        return False

    def checkMoveSpace(self):
        # if self.isPolice and self.roadStep >= 1:
        #     self.prev = map.map[self.road[self.roadStep-1]].getLastOnRoadToBefore(self.road[self.roadStep], self.id)
        if self.roadStep < len(self.road) and self.prev!= None:
            if self.road[self.roadStep] != self.carsPos[self.prev][2]:
                self.prev = None
        if self.prev != None:
            self.carsPosLock.acquire()
            if distance([self.posX, self.posY], self.carsPos[self.prev])<self.length*1.2:
                if self.carsPos[self.prev][4].count(self.id)>0:
                    print(self.id, " blocking car (no move space) ",self.prev," blocked by me")
                    self.carsPosLock.release()

                    return False
                # if self.isPolice:
                #     if self.carsPos[self.prev][3] == 0:
                #         pass
                #         # self.stopOtherCars()
                #     else:
                #         self.carsPosLock.release()
                #         return False
                self.carsPosLock.release()
                return True
            # print(self.id, " not stopped by no move space\n",
            # "self.prev: ", self.prev, " distance: ", distance([self.posX, self.posY], self.carsPos[self.prev]),
            # " carLength*1.2: ", self.length*1.2)
            self.carsPosLock.release()
        # print("self.prev == None")
        return False

    def move(self):
        """
        ----------------------------------------------------
        Function to:
        the main loop function, that's the only function 
        called from outside. Coordinates the movement of 
        the car, using most if not all othe functions of the
        class
        ----------------------------------------------------
        Parameters:
        none
        ----------------------------------------------------
        Returns:
        none
        ----------------------------------------------------
        """

        
        if not self.isPolice:
            self.carsPosLock.acquire()
            self.stoppedByPolice = self.carsPos[self.id][3] == 1
            self.carsPosLock.release()
            self.stoppedByNoMoveSpace = self.checkMoveSpace()
        # else:
        #     self.stopOtherCars()
        if not self.stoppedByRightBusy and not self.stoppedByNoLeaveSpace and not self.stoppedByNoMoveSpace and not self.stoppedByPolice:
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
                
                # self.posX = self.nextStep["position"][0]
                # self.posY = self.nextStep["position"][1]
                self.calculateRoute(self.destination, to)
                        
                self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
                # print("distance ", distance((self.posX, self.posY), self.nextStep["position"]))
                self.changeDirection()
                
            else:
                
                if not self.addedToOutgoing:
                    map.map[self.road[self.roadStep-1]].outgoingLock.acquire()
                    map.map[self.road[self.roadStep-1]].addOutgoing(self.id, self.road[self.roadStep], False)
                    self.prev = map.map[self.road[self.roadStep-1]].getLastOnRoadTo(self.road[self.roadStep], self.id, False)
                    map.map[self.road[self.roadStep-1]].outgoingLock.release()
                    # if self.prev != None:
                    #     print("id: ", self.id, " prev: ", self.prev)
                    # print("road: ", self.road, " road step: ", self.roadStep, " self.road[self.roadStep] ", self.road[self.roadStep])
                    self.addedToOutgoing = 1

                # if self.prev != None:
                #     self.carsPosLock.acquire()
                #     if distance(self.carsPos[self.prev], [self.posX, self.posY])  < self.length*1.2:
                #         # if self.road[self.roadStep] != self.carsPos[self.prev][2] and :
                #         #     self.prev = None
                #         # else:
                #             self.carsPosLock.release()
                #             print("Id: ",self.id, " breaking")
                #             self.render()
                #             return
                #     # else:
                #     #     print("")
                #     #     print("Id: ",self.id, " distance to ", self.prev, " ", distance(self.carsPos[self.prev], [self.posX, self.posY]), " position previous: ", self.carsPos[self.prev])
                #     #     print("")   
                #     self.carsPosLock.release()

                #moved = 0
                # print("posX: ",self.posX)
                # print("posY: ",self.posY)
                # print("dirX: ",self.dirX)
                # print("dirY: ",self.dirY)
                #pygame.draw.rect(gameDisplay, green, pygame.Rect(self.posX, self.posY, 50, 20))
                # if not self.addedToOutgoing:
                #     Map[self.roadStep].addOutgoing(self.id, self.road[self.roadStep])
                if distance([self.posX,self.posY], self.nextStep["position"]) > self.length * 1.2:
                    if(not diffWithin(self.posX, self.nextStep["position"][0], self.currRoadLen*0.05)):
                        
                        # print ("a")
                        if self.isPolice:
                            self.posX = self.posX+2*self.dirX
                        else:
                            self.posX = self.posX+self.dirX
                        self.carsPosLock.acquire()
                        a = self.carsPos[self.id]
                        a[0] = self.posX
                        a[1] = self.posY
                        a[2] = self.road[self.roadStep]
                        self.carsPos[self.id] = a
                            # if(self.id == 1):
                            #     print("id: ",self.id )
                            #     print("car positions(after x): ", self.carsPos)
                            #     print("my position: ", [self.posX, self.posY])
                        self.carsPosLock.release()
                        #moved = 1
                    if(not diffWithin(self.posY, self.nextStep["position"][1], self.currRoadLen*0.05)):
                        # print ("b")
                        if self.isPolice:
                            self.posY = self.posY+2*self.dirY
                        else:
                            self.posY = self.posY+self.dirY
                        self.carsPosLock.acquire()
                        a = self.carsPos[self.id]
                        a[0] = self.posX
                        a[1] = self.posY
                        a[2] = self.road[self.roadStep]
                        self.carsPos[self.id] = a
                            # print("id: ",self.id )
                            # print("car positions(after y): ", self.carsPos)
                        self.carsPos.append([0,0,-1,0])
                        self.carsPosLock.release()
                        # moved = 1
                else:
                    # print("c")
                    if self.isPolice:
                        self.startOtherCars()
                    if self.addedToOutgoing:
                        map.map[self.road[self.roadStep-1]].removeFromOutgoing(self.id, self.road[self.roadStep])
                        self.addedToOutgoing = 0
                    self.posX = self.nextStep["position"][0] - self.length * self.dirX
                    self.posY = self.nextStep["position"][1] - self.length * self.dirY
                    self.carsPosLock.acquire()
                    a = self.carsPos[self.id]
                    a[0] = self.dirX
                    a[1] = self.dirY
                    a[2] = self.road[self.roadStep]
                    self.carsPos[self.id] = a
                    self.carsPosLock.release()

                    self.roadStep = self.roadStep+1
                        #         pass
                    if(self.roadStep <= len(self.road)-1):
                        
                        self.nextStep = map.map[self.road[self.roadStep]]
                        if not self.isPolice:
                            self.stoppedByRightBusy = self.checkRightFree(self.roadStep-1)
                            self.stoppedByNoLeaveSpace = self.checkLeaveSpace(self.roadStep-1)
                        
                        # self.posX = self.nextStep["position"][0]
                        # self.posY = self.nextStep["position"][1]
                        # print(self.road[self.roadStep]," NeighborsFrom: ", map.map[self.road[self.roadStep]].neighborsFrom)
                        
                        # print("d")
                        if not self.stoppedByRightBusy and not self.stoppedByNoLeaveSpace:
                            
                            self.changeDirection()
                            
                            self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
                self.render()
        else:
            if self.stoppedByRightBusy:
                check = self.checkRightFree(self.roadStep-1)
                if not check:
                    self.count -= 1
                else:
                    self.count = 5
                if self.count == 0:
                    self.stoppedByRightBusy = False
                # print("Id: ",self.id," stopped by right")
            
            if self.stoppedByNoLeaveSpace:
                self.stoppedByNoLeaveSpace = self.checkLeaveSpace(self.roadStep-1)
                # print("Id: ",self.id," stopped by no leave space, self.road[self.roadStep]: ", self.road[self.roadStep], " self.road[self.roadStep-1]: ", self.road[self.roadStep-1] , " self.prev: ", self.prev)
            else:
                self.stoppedByNoLeaveSpace = self.checkLeaveSpace(self.roadStep-1)

            if self.stoppedByNoMoveSpace:
                self.stoppedByNoMoveSpace = self.checkMoveSpace()
                print("Id: ", self.id, " stopped by no move space, self.prev: ", self.prev)
            else:
                self.stoppedByNoMoveSpace = self.checkMoveSpace()

            if self.stoppedByPolice:
                self.carsPosLock.acquire()
                self.stoppedByPolice = self.carsPos[self.id][3] == 1
                self.carsPosLock.release()
                # print("Id: ", self.id, " stopped by police")
            
            if not self.stoppedByRightBusy and not self.stoppedByNoLeaveSpace and not self.stoppedByNoMoveSpace and not self.stoppedByPolice:
                # self.roadStep = self.roadStep+1
                self.changeDirection()
                # self.nextStep = map.map[self.road[self.roadStep]]
                self.currRoadLen = distance((self.posX, self.posY), self.nextStep["position"])
            self.render()



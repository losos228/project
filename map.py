
from random import randrange
import pygame
import os
import multiprocessing as mp

#import networkx as nx

FPS = 60
WIDTH, HEIGHT = 1920, 1080
# Nodes radius
RADIUS = 35
# Distance between intersections
WHITE = (255, 255, 255)
DEEPBLUE = (0, 191, 255)
GREEN = (0, 250, 80)
DARK = (0, 0, 0)
DIMGRAY = (105, 105, 105)
FLAGS = pygame.FULLSCREEN | pygame.SCALED
#FLAGS,
WIN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("Simulation")

pygame.init()
FONT = pygame.font.SysFont('arial', 40)

class intersection(pygame.sprite.Sprite):
  def addOutgoing(self, car, goingTo, acquireLock = True):
    # print("adding: ", car)
    if acquireLock:
      self.outgoingLock.acquire()
    self.outgoing.append((car, goingTo))
    if acquireLock:
      self.outgoingLock.release()
    # print("to ",self.name)
    # print(self.name, self.outgoing)
  def removeFromOutgoing(self, car, goingTo):
    # print("removing ", car)
    # print("goingTo ", goingTo)
    self.outgoingLock.acquire()
    self.outgoing.remove((car, goingTo))
    self.outgoingLock.release()
    # print("removing finished ", car)

  def getLastOnRoadTo(self, dest, ignore = -1, acquireLock = True):
    if acquireLock:
      self.outgoingLock.acquire()
    if len(self.outgoing) > 0:
      for i in range(len(self.outgoing)-1, -1, -1):
        # print(ignore, " checking: ", i)
        if(self.outgoing[i][1] == dest and self.outgoing[i][0] != ignore):
          if acquireLock:
            self.outgoingLock.release()
          print(" found: ", self.outgoing[i][0])
          return self.outgoing[i][0]
      # if(self.outgoing[0][1] == dest and self.outgoing[0][0] != ignore):
      #   if acquireLock:
      #     self.outgoingLock.release()
      #   print("found in first place: ", self.outgoing[0][0])
      #   return self.outgoing[0][0]
    if acquireLock:
      self.outgoingLock.release()
    print("didn't find anything, going to ", dest, " Outgoing: ", self.outgoing, " Ignore: ", ignore)
    return None

  def getFirstOnRoadTo(self, dest, acquireLock = True):
    if acquireLock:
      self.outgoingLock.acquire()
    for i in range(len(self.outgoing)):
      if(self.outgoing[i][1] == dest):
        if acquireLock:
          self.outgoingLock.release()
        return i
    if acquireLock:
      self.outgoingLock.release()
    return None

  def __init__(self, name, position, neighbors, weights):

    self.name = name
    self.position = position
    self.neighbors = neighbors
    self.neighborsAngles = [len(self.neighbors)]
    #self.font = FONT
<<<<<<< HEAD
=======
    self.color = [randrange(255), randrange(255), randrange(255)]
    while self.color == [0,0,0]:
      self.color = [randrange(255), randrange(255), randrange(255)]

>>>>>>> origin
    self.outgoingManager = mp.Manager()
    self.outgoingLock = self.outgoingManager.Lock()
    self.outgoing = self.outgoingManager.list() #car, going to
  def __getitem__ (self, key):
    return getattr(self, key)
  #def add_text_to_map(self):


def map_helper(__map, __name, __position, __neighbors, __weights, __node_name):
  __map.append(intersection(__name, __position, __neighbors, __weights))
  __node_name = __node_name + 1
  return __map, __node_name

# distance_between_intersections -> dbi
# num_of_intersections -> noi
def generate_map(noi, dbi, offsetX = 0, offsetY = 0, is_fully_connected = True):
  __map = []
  __node_name = 0
  __current_pos = 0
  for idx in range(noi):
    for idy in range(noi):
      __current_pos = idx*noi + idy
      __name = f"v{__node_name}"
      __position = (dbi*idx + offsetX, dbi*idy + offsetY)

      #is_border_intersection = False
      __neighbors = []
      __weights = []

      # Corners

      if(idx == 0 and idy == 0):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([1, noi])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == 0 and idy == noi-1):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi-2, 2*noi-1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == noi-1 and idy == 0):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi*(noi-2), noi*(noi-1)+1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == noi-1 and idy == noi-1):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi*(noi-1)-1, noi**2-2])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      # Other borders
      #elif(idx == 0 and 1 <= idy <= noi-2):
      #  __neighbors.extend([idy-1, idy+1, idy+noi])
      #  __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      #elif(1 <= idx <= noi-2 and idy == 0):
      #  print(f"X {idx}, Y {idy}")
        #__neighbors.extend([])
        #__map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)
      #elif(1 <= idx <= noi-2 and idy == noi-2):
      #elif(idx == noi-2 and 1 <= idy <= noi-2):

      else:
      #if(idx*noi):
        print(f"current position {__current_pos}")
        if(__current_pos%noi == noi-1):
          __neighbors.extend([__current_pos-noi,
                              __current_pos+noi,
                              __current_pos-1])
          __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

        elif(__current_pos%noi == 0):
          __neighbors.extend([__current_pos-noi,
                              __current_pos+noi,
                              __current_pos+1])
          __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

        else:
          __neighbors.extend([__current_pos-noi if __current_pos-noi > 0 else 0,
                              __current_pos-1 if __current_pos-1 > 0 else 0,
                              __current_pos+1,
                              __current_pos+noi])
          #print(f"neighbors are {__neighbors}")
          __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

  return __map
# x->
#y# "v00", "v10",
#|# "v01", "v11"
#v
map = [
  #            name   position    neighbors    weights
  intersection("v0",  (50, 50),   [1, 4],      [2, 3]),
  intersection("v1",  (50, 150),  [0, 2],      [1, 3]),
  intersection("v2",  (50, 250),  [1, 3, 7],   [1, 3]),
  intersection("v3",  (50, 350),  [2],         [1]),
  intersection("v4",  (150, 50),  [0, 5],      [1, 1]),
  intersection("v5",  (250, 50),  [4],      [ 1]),
  intersection("v6",  (150, 150), [1, 4],      [1, 1]),
  intersection("v7",  (150, 250), [2, 6, 8, 15, 9],   [1, 1, 1, 1, 1]),
  intersection("v8",  (150, 350), [3, 13, 15],         [1, 1, 1]),
  intersection("v9",  (350, 50),  [5,14,7],      [1, 1, 1]),

  intersection("v10",  (450, 50),  [9, 11],    [1, 1]),
  intersection("v11",  (450, 150), [10],       [1, 1]),
  intersection("v12",  (450, 250), [11, 13],   [1, 1]),
  intersection("v13",  (450, 350), [12, 8],    [1, 1]),
  intersection("v14",  (350, 150), [9, 15],    [1, 1]),
  intersection("v15",  (350, 250), [14,  12],  [1, 1]),
]

def draw_map(map_):
  WIN.fill(GREEN)
  pygame.display.flip()
  __visited = []
  print(f"map = {len(map_)}")
  for i in range(len(map_)):
    print(f"i = {i}")
    #font = pygame.font.sysFont(map["name"], 30)
    # Get node position and draw
    x, y = map_[i]["position"]
    print(f"x = {x} and y = {y}")
    WIN.blit(FONT.render(map_[i].name, True, (WHITE)), (x+10, y+10))
    # Draw Nodes
    # pygame.draw.circle(WIN, DEEPBLUE,
    #                   (x, y), RADIUS)



    for neighbor in map_[i]["neighbors"]:
      __edge = []
      #print(f"i, before added to edge = {i}")
      __edge.append(i)
      __edge.append(neighbor)
      __edge = sorted(__edge)
      #print(f"edge = {__edge}")
      __visited.append(__edge)
      #print(f"visited = {__visited}")
      if(__visited.count(__edge) > 1):
        print("here")
        pygame.draw.line(WIN, DIMGRAY, map_[i]["position"],
                                       map_[neighbor]["position"],
                                       30)
        pygame.draw.line(WIN, WHITE, map_[i]["position"],
                                     map_[neighbor]["position"],
                                     2)
        #print(f"[{i}] and [{neighbor}] DOUBLE EDGE")
      """
      else:
        print("here2")
        pygame.draw.line(WIN, DIMGRAY, map_[i]["position"],
                                       map_[neighbor]["position"],
                                       30)
      """
        #print(f"[{i}] and [{neighbor}] SINGLE EDGE")
    WIN.blit(FONT.render(map_[i].name, True, (map_[i].color)), (x+10, y+10))
    # Update screen
    pygame.display.update()
    pygame.image.save(WIN, "images/background.jpg")

def main():




  #pygame.init()
  clock = pygame.time.Clock()
  run = True

  new_map = []

  num_of_intersections = 4
  distance_between_intersections = 250
  center_of_map = distance_between_intersections*num_of_intersections/2
  offsetX = WIDTH/2 - center_of_map
  offsetY = HEIGHT/2 - center_of_map #+ 100

  new_map = generate_map(num_of_intersections, distance_between_intersections, offsetX, offsetY)
  draw_map(new_map)

  #draw_window()

  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        run = False



  #pygame.quit()






if __name__ == '__main__':

  main()
  # Draw all is



    #print(node)
  ##print(map[1]["position"][0])
  #main()

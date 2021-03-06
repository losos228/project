
from random import randrange
import pygame
import os
import multiprocessing as mp
from commons import distance

#import networkx as nx

FPS = 60
WIDTH, HEIGHT = 1080, 1080
# Nodes radius
RADIUS = 35
# Distance between intersections
WHITE = (255, 255, 255, 255)
DEEPBLUE = (0, 191, 255, 255)
GREEN = (0, 250, 80, 255)
DARK = (0, 0, 0, 255)
DIMGRAY = (105, 105, 105, 255)
FLAGS = pygame.FULLSCREEN | pygame.SCALED
#FLAGS,
WIN = pygame.display.set_mode((WIDTH, HEIGHT), vsync=1)
pygame.display.set_caption("Simulation")

pygame.init()
FONT = pygame.font.SysFont('arial', 40)

class intersection(pygame.sprite.Sprite):
  """
  Class implementing intersection of roads
  """
  def addOutgoing(self, car, goingTo, acquireLock = True):
    """
    ----------------------------------------------------
    Function to:
    Add a car to the outgoing table
    ----------------------------------------------------
    Parameters:
    car(int): the position of the car in the cars table
    goingTo(int): the intersection on road to which the car is
    acquireLock(bool, optional): whether or not to acquire the lock to the outgoing table
    ----------------------------------------------------
    Returns:
    Doesn't return anything
    ----------------------------------------------------
    """
    # print("adding: ", car, " going to: ",goingTo)
    if acquireLock:
      self.outgoingLock.acquire()
    self.outgoing.append((car, goingTo))
    if acquireLock:
      self.outgoingLock.release()
    # print("to ",self.name)
    # print(self.name, self.outgoing)

  def removeFromOutgoing(self, car, goingTo, acquireLock = True):
    """
    ----------------------------------------------------
    Function to:
    Remove a car from the outgoing table
    ----------------------------------------------------
    Parameters:
    car(int): the position of the car in the cars table
    goingTo(int): the position in the map of the intersection on
      road to which the car is
    acquireLock(bool, optional): whether or not to acquire the
      lock to the outgoing table
    ----------------------------------------------------
    Returns:
    Doesn't return anything
    ----------------------------------------------------
    """
    # print("removing ", car," goingTo ", goingTo)
    if acquireLock:
      self.outgoingLock.acquire()
    self.outgoing.remove((car, goingTo))
    if acquireLock:
      self.outgoingLock.release()
    # print("removing finished ", car)

  def getLastOnRoadTo(self, dest, ignore = -1, acquireLock = True):
    """
    ----------------------------------------------------
    Function to:
    Get the last car on road to a specified intersection
    ----------------------------------------------------
    Parameters:
    dest(int): the position in the map of the intersection on
      road to which the desired car is
    ignore(int, optional): a car to ignore
    acquireLock(bool, optional): whether or not to acquire the
      lock to the outgoing table
    ----------------------------------------------------
    Returns:
    (int) the position in the cars table of the car that's the
      last on the road from the intersection to dest
    None if there is no suitable car on the road
    ----------------------------------------------------
    """
    if acquireLock:
      self.outgoingLock.acquire()
    if len(self.outgoing) > 0:
      for i in range(len(self.outgoing)-1, -1, -1):
        # print(ignore, " checking: ", i)
        if(self.outgoing[i][1] == dest):
          if self.outgoing[i][0] != ignore:
            found = self.outgoing[i][0]
            if acquireLock:
              self.outgoingLock.release()
            # print(" found: ", found)
            return found
          # else:
          #   return None
      # if(self.outgoing[0][1] == dest and self.outgoing[0][0] != ignore):
      #   if acquireLock:
      #     self.outgoingLock.release()
      #   print("found in first place: ", self.outgoing[0][0])
      #   return self.outgoing[0][0]
    if acquireLock:
      self.outgoingLock.release()
    # print("didn't find anything, going to ", dest, " Outgoing: ", self.outgoing, " ignore: ", ignore)
    return None

  def getLastOnRoadToBefore(self, dest, before, acquireLock = True):
    """
    ----------------------------------------------------
    Function to:
    Get the last car on road to a specified intersection
    ----------------------------------------------------
    Parameters:
    dest(int): the position in the map of the intersection on
      road to which the desired car is
    before(int): a car before whitch to find the other car
    acquireLock(bool, optional): whether or not to acquire the
      lock to the outgoing table
    ----------------------------------------------------
    Returns:
    ----------------------------------------------------
    """
    if acquireLock:
      self.outgoingLock.acquire()
    if len(self.outgoing) > 0:
      foundBefore = 0
      for i in range(len(self.outgoing)-1, -1, -1):
        # print(ignore, " checking: ", i)
        if(self.outgoing[i][1] == dest):
          if self.outgoing[i][0] == before:
            foundBefore = 1
          if foundBefore:
            found = self.outgoing[i][0]
            if acquireLock:
              self.outgoingLock.release()
            # print(" found: ", found)
            return found
          # else:
          #   return None
      # if(self.outgoing[0][1] == dest and self.outgoing[0][0] != ignore):
      #   if acquireLock:
      #     self.outgoingLock.release()
      #   print("found in first place: ", self.outgoing[0][0])
      #   return self.outgoing[0][0]
    if acquireLock:
      self.outgoingLock.release()
    # print("didn't find anything, going to ", dest, " Outgoing: ", self.outgoing, " ignore: ", ignore)
    return None

  def getFirstOnRoadTo(self, dest, ignore = -1,acquireLock = True):
    """
    ----------------------------------------------------
    Function to:
    Get the first car on road to a specified intersection
    ----------------------------------------------------
    Parameters:
    dest(int): the position in the map of the intersection on
      road to which the desired car is
    ignore(int, optional): a car to ignore
    acquireLock(bool, optional): whether or not to acquire the
      lock to the outgoing table
    ----------------------------------------------------
    Returns:
    (int) the position in the cars table of the car that's the
      first on the road from the intersaction to dest
    None if there is no suitable car on the road
    ----------------------------------------------------
    """
    if acquireLock:
      self.outgoingLock.acquire()
    for i in range(len(self.outgoing)):
      if(self.outgoing[i][1] == dest and self.outgoing[i][0] != ignore):
        found = self.outgoing[i][0]
        if acquireLock:
          self.outgoingLock.release()
        return found
    if acquireLock:
      self.outgoingLock.release()
    return None

  def getAllOnRoadTo(self, dest):
    """
    ----------------------------------------------------
    Function to:
    Get all the cars going to a specified intersection
    ----------------------------------------------------
    Parameters:
    dest(int): the position in the map of the intersection on
      road to which to get all the cars
    ----------------------------------------------------
    Returns:
    (int array) the position in the cars table of all the
    cars on the road
    None if there is no car on the road
    ----------------------------------------------------
    """
    toReturn = []
    self.outgoingLock.acquire()
    # print("outgoing: ", self.outgoing)
    for i in range(len(self.outgoing)):
      if self.outgoing[i][1] == dest:
        toReturn.append(self.outgoing[i])
    self.outgoingLock.release()
    return toReturn

  def set_weight(self, __weight):
    pass

  def get_weight(self, dest):
    """
    ----------------------------------------------------
    Function to:
    Get weight of the road to a specific intersection
    ----------------------------------------------------
    Parameters:
    dest(int): the position in the map of the intersection 
      at the end of the road which weight is desired 
    ----------------------------------------------------
    Returns:
    (int) the wieght of the specified road
    ----------------------------------------------------
    """
    print(f"here ->>>>>>>>>>>>>>>>>>>>>>>>>>>>. {map[1].name} - {map[1].position} - {map[1].weights}")
    i = 0
    found = -1
    for i in range(len(self.neighbors)):
      if self.neighbors[i] == dest:
        found = i
    if found != -1:
      dist = 1 #distance(map[found]["position"], self["position"])
      onRoad = len(self.getAllOnRoadTo(dest))
      if onRoad == 0:
        weight = dist
      else:
        weight = dist * (onRoad+1)
    else:
      weight = 99999999999


    return weight

  def __init__(self, name, position, neighbors, weights):
    self.name = name
    self.position = position
    self.neighbors = neighbors
    self.weights = weights
    self.neighborsAngles = [len(self.neighbors)]
    self.neighborsFrom = []
    #self.font = FONT
    self.color = [randrange(255), randrange(255), randrange(255)]
    while self.color == [0,0,0]:
      self.color = [randrange(255), randrange(255), randrange(255)]

    self.outgoingManager = mp.Manager()
    self.outgoingLock = self.outgoingManager.Lock()
    self.outgoing = self.outgoingManager.list() #car, going to
  def __getitem__ (self, key):
    return getattr(self, key)
  #def add_text_to_map(self):


def map_helper(__map, __name, __position, __neighbors, __weights, __node_name):
  """
  ----------------------------------------------------
  Function to help generate_map
  to keep the code cleaner
  ----------------------------------------------------
  Parameters:
    __map(list): Current map
    __name(str): Name of current intersection
    __position(int, int): Position of current intersection - (x, y)
    __neighbors(list): Neighbors of current intersection
    __weights(list): Weights for edges between current intersection and Neighbors
    __node_name(int): helper intersection name to easier handle __name
  ----------------------------------------------------
  Returns:
    __map(list): Map with all the intersections
    __node_name(int): Name for the currently processed intersection
  ----------------------------------------------------
  """
  __map.append(intersection(__name, __position, __neighbors, __weights))
  __node_name = __node_name + 1
  return __map, __node_name

# distance_between_intersections -> dbi
# num_of_intersections -> noi
def generate_map(noi, dbi, offsetX = 0, offsetY = 0, is_fully_connected = True):
  """
  ----------------------------------------------------
  Function to generate square like maps(2x2, 3x3, ...)
  into a list for further use
  ----------------------------------------------------
  Parameters:
    noi(int):
    dbi(int):
    offsetX(int):
    offsetY(int):
    is_fully_connected(bool):
  ----------------------------------------------------
  Returns:
    __map(list):
  ----------------------------------------------------
  """
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
        __weights.extend([1, 1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == 0 and idy == noi-1):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi-2, 2*noi-1])
        __weights.extend([1, 1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == noi-1 and idy == 0):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi*(noi-2), noi*(noi-1)+1])
        __weights.extend([1, 1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == noi-1 and idy == noi-1):
        print(f"X {idx}, Y {idy}")
        __neighbors.extend([noi*(noi-1)-1, noi**2-2])
        __weights.extend([1, 1])
        #print(f"neighbors are {__neighbors}")
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      # Other borders
      elif(idx == 0 and 1 <= idy <= noi-2):
        __neighbors.extend([idy-1, idy+1, idy+noi])
        __weights.extend([1, 1, 1])
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(1 <= idx <= noi-2 and idy == 0):
      #  print(f"X {idx}, Y {idy}")
        __neighbors.extend([__node_name-noi, __node_name+1, __node_name+noi])
        __weights.extend([1, 1, 1])
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(idx == noi-1 and 1 <= idy <= noi-2):
        print("__node_name", __node_name)
        __neighbors.extend([__node_name-noi, __node_name-1, __node_name+1])
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      elif(1 <= idx <= noi-2 and idy == noi-1):
        __neighbors.extend([__node_name-noi, __node_name-1, __node_name+noi])
        __weights.extend([1, 1, 1])
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      # Everything else - center intersections with 4 edges
      else:
        __neighbors.extend([__node_name-noi, __node_name-1, __node_name+1, __node_name+noi])
        __weights.extend([1, 1, 1, 1])
        __map, __node_name = map_helper(__map, __name, __position, __neighbors, __weights, __node_name)

      """
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
        """
  return __map
# x->
#y# "v00", "v10",
#|# "v01", "v11"
#v
roads = {
  (0, 1): 2,
  (0, 2): 1
}
map = [
  #            name   position    neighbors    weights
  intersection("v0",  (50, 50),   [1, 4],      [2, 3]),
  intersection("v1",  (50, 150),  [0, 2],      [1, 3]),
  intersection("v2",  (50, 250),  [1, 3, 7],   [1, 3]),
  intersection("v3",  (50, 350),  [2],         [1]),
  intersection("v4",  (150, 50),  [0, 5],      [1, 1]),
  intersection("v5",  (250, 50),  [4],      [ 1]),
  intersection("v6",  (170, 150), [1, 4],      [1, 1]),
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

map_scenario_2 = [
  #            name   position    neighbors    weights
  intersection("v0",  (100, 100),   [1],      [2, 3]),
  intersection("v1",  (500, 100),  [0],      [1, 3]),
]

def update_weights_of(map_):
  """
  ----------------------------------------------------
  Function to ...
  ----------------------------------------------------
  Parameters:
    map_(list):
  ----------------------------------------------------
  Returns:
    Does not return
  ----------------------------------------------------
  """
  
  # For each road:
  # -> check amount of cars
  # -> update weight for given equation - new_weight = old_weight*num_of_cars

  return map_


def draw_map(map_):
  """
  ----------------------------------------------------
  Function to ...
  ----------------------------------------------------
  Parameters:
    map_(list):
  ----------------------------------------------------
  Returns:
    Does not return
  ----------------------------------------------------
  """
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
      map_[neighbor].neighborsFrom.append(i)
      __edge = []
      #print(f"i, before added to edge = {i}")
      __edge.append(i)
      __edge.append(neighbor)
      __edge = sorted(__edge)
      #print(f"edge = {__edge}")
      __visited.append(__edge)
      #print(f"visited = {__visited}")
      if(__visited.count(__edge) > 1):
        pygame.draw.line(WIN, WHITE, map_[i]["position"],
                                     map_[neighbor]["position"],
                                     2)
        #print(f"[{i}] and [{neighbor}] DOUBLE EDGE")

      else:
        print("here2")
        pygame.draw.line(WIN, DIMGRAY, map_[i]["position"],
                                       map_[neighbor]["position"],
                                       30)

    
    #print(f"[{i}] and [{neighbor}] SINGLE EDGE")
    WIN.blit(FONT.render(map_[i].name, True, (map_[i].color)), (x+10, y+10))
    # Update screen
    pygame.display.update()

        #print(f"[{i}] and [{neighbor}] SINGLE EDGE")
    WIN.blit(FONT.render(map_[i].name, True, (map_[i].color)), (x+10, y+10))
    # Update screen
    pygame.display.update()
    pygame.image.save(WIN, "images/background.jpg")

def main():

  clock = pygame.time.Clock()
  run = True

  new_map = []

  num_of_intersections = 5
  distance_between_intersections = 150
  center_of_map = distance_between_intersections*num_of_intersections/2
  offsetX = WIDTH/2 - center_of_map
  offsetY = HEIGHT/2 - center_of_map #+ 100

  #new_map = generate_map(num_of_intersections, distance_between_intersections, offsetX, offsetY)
  #draw_map(new_map)
  draw_map(map_scenario_2)
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

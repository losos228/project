#from turtle import position
import pygame
import os
#import networkx as nx

FPS = 60
WIDTH, HEIGHT = 900, 500
# Nodes radius
RADIUS = 35
# Distance between intersections
DISTANCE = 50
WHITE = (255, 255, 255)
DEEPBLUE = (0, 191, 255)
GREEN = (0, 250, 80)
DARK = (0, 0, 0)
DIMGRAY = (105, 105, 105)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph")

pygame.init()
FONT = pygame.font.SysFont('arial', 40)

class intersection(pygame.sprite.Sprite):
  def addOutgoing(self, car, goingTo):
    self.outgoing.append((car, goingTo))
  def removeFromOutgoing(self, car, goingTo):
    self.outgoing.remove((car, goingTo))

  def __init__(self, name, position, neighbors, weights):
    self.name = name
    self.position = position
    self.neighbors = neighbors
    self.weights = weights
    self.font = FONT
 #   self.outgoing = [][2] #car, going to
  def __getitem__ (self, key):
    return getattr(self, key)
  #def add_text_to_map(self):


# distance_between_intersections -> dbi
def generate_map(num_of_intersections, dbi, is_fully_connected):
  _map = []

  for idx in range(num_of_intersections):
    _name = f"v{idx}"
    # generate positions
    _position = (0, 0)
    # generate neigbors
    _neighbors = []
    # generate weights
    _weights = []
    _map.append(intersection(_name, _position, _neighbors, _weights))

  return _map


map = [
  #            name   position    neighbors    weights
  intersection("v0",  (50, 50),   [1, 4, 5],   [2, 3, 1]),
  intersection("v1",  (50, 150),  [0, 2],      [1, 3]),
  intersection("v2",  (50, 250),  [1, 3, 7],   [1, 3]),
  intersection("v3",  (50, 350),  [2],         [1]),
  intersection("v4",  (150, 50),  [0, 5],      [1, 1]),
  intersection("v5",  (250, 50),  [4, 9],      [1, 1]),
  intersection("v6",  (150, 150), [1, 4],      [1, 1]),
  intersection("v7",  (150, 250), [2, 6, 8],   [1, 1, 1]),
  intersection("v8",  (150, 350), [3],         [1, 1]),
  intersection("v9",  (350, 50),  [5,14],      [1, 1]),

  intersection("v10",  (450, 50),  [9, 11],    [1, 1]),
  intersection("v11",  (450, 150), [10],       [1, 1]),
  intersection("v12",  (450, 250), [11, 13],   [1, 1]),
  intersection("v13",  (450, 350), [12],       [1]),
  intersection("v14",  (350, 150), [9, 15],    [1, 1]),
  intersection("v15",  (350, 250), [14,  12],  [1, 1]),
]



def draw_window():
  WIN.fill(GREEN)
  pygame.display.flip()
  visited = []
  for i in range(len(map)):
    #font = pygame.font.sysFont(map["name"], 30)
    # Get node position and draw
    x, y = map[i]["position"]
    WIN.blit(map[i].font.render(map[i].name, True, (WHITE)), (x+10, y+10))
    # Draw Nodes
    # pygame.draw.circle(WIN, DEEPBLUE,
    #                   (x, y), RADIUS)


    for neighbor in map[i]["neighbors"]:
      edge = []
      edge.append(i)
      edge.append(neighbor)
      edge = sorted(edge)
      visited.append(edge)

      if(visited.count(edge) > 1):
        pygame.draw.line(WIN, DIMGRAY, map[i]["position"],
                                    map[neighbor]["position"],
                                    30 )
        pygame.draw.line(WIN, WHITE, map[i]["position"],
                                    map[neighbor]["position"],
                                    2 )
        #print(f"[{i}] and [{neighbor}] DOUBLE EDGE")
      else:
        pygame.draw.line(WIN, DIMGRAY, map[i]["position"],
                                    map[neighbor]["position"],
                                    30 )
        #print(f"[{i}] and [{neighbor}] SINGLE EDGE")

    # Update screen
    pygame.display.update()
    pygame.image.save(WIN, "images/background.jpg")

    #print(f"i {i}: X is {x} and Y is {y}\n")

def main():




  #pygame.init()
  clock = pygame.time.Clock()
  run = True

  draw_window()

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

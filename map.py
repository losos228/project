from turtle import position
import pygame
import os
#import networkx as nx

FPS = 60
WIDTH, HEIGHT = 900, 500
# Nodes radius
RADIUS = 35
WHITE = (255, 255, 255)
DEEPBLUE = (0, 191, 255)
GREEN = (0, 250, 80)
DARK = (0, 0, 0)
DIMGRAY = (105, 105, 105)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Graph")

class intersection(pygame.sprite.Sprite):
  def __init__(self, position, neighbors, weights):
    self.position = position
    self.neighbors = neighbors
    self.weights = weights
  def __getitem__ (self, key):
    return getattr(self,key)
    

map = {
  "v1": intersection((50,50), ["v2","v3"], [2,3]),
  "v2": intersection((100, 300),["v1"],[1, 3])  ,
  "v3": intersection((350, 150),["v4", "v1"],[1, 3]),
  "v4": intersection((400, 400),["v2", "v5"],[1]),
  "v5": intersection((600, 400),["v4"],[1]),
  "v6": intersection((600, 300),["v4", "v5"],[1])
}


def draw_window():
  WIN.fill(GREEN)
  pygame.display.flip()
  visited = []
  for node in map:
    # Get node position and draw
    x, y = map[node]["position"]
    # Draw Nodes
    pygame.draw.circle(WIN, DEEPBLUE,
                      (x, y), RADIUS)


    for neighbor in map[node]["neighbors"]:
      edge = []
      edge.append(node)
      edge.append(neighbor)
      edge = sorted(edge)
      visited.append(edge)

      if(visited.count(edge) > 1):
        pygame.draw.line(WIN, DIMGRAY, map[node]["position"],
                                    map[neighbor]["position"],
                                    30 )
        pygame.draw.line(WIN, WHITE, map[node]["position"],
                                    map[neighbor]["position"],
                                    2 )
        #print(f"[{node}] and [{neighbor}] DOUBLE EDGE")
      else:
        pygame.draw.line(WIN, DIMGRAY, map[node]["position"],
                                    map[neighbor]["position"],
                                    30 )
        #print(f"[{node}] and [{neighbor}] SINGLE EDGE")

    # Update screen
    pygame.display.update()
    pygame.image.save(WIN, "images/background.jpg")

    #print(f"Node {node}: X is {x} and Y is {y}\n")

def main():
  clock = pygame.time.Clock()
  run = True

  draw_window()

  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False



  #pygame.quit()




if __name__ == '__main__':

  main()
  # Draw all nodes



    #print(node)
  ##print(map["v1"]["position"][0])
  #main()

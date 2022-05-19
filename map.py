#from turtle import position
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


map = [
  intersection("v1", (50, 50), [1,2], [2,3]),
  intersection("v2", (100, 300),[0],[1, 3]),
  intersection("v3", (350, 150),[3, 0, 5],[1, 3]),
  intersection("v4", (400, 400),[1, 4],[1]),
  intersection("v5", (600, 400),[3, 5],[1]),
  intersection("v6", (700, 150),[3, 4],[1])
]



def draw_window():
  WIN.fill(GREEN)
  pygame.display.flip()
  visited = []
  for i in range(len(map)):
    #font = pygame.font.sysFont(map["name"], 30)
    # Get node position and draw
    x, y = map[i]["position"]
    WIN.blit(map[i].font.render(map[i].name, True, (WHITE)), (x+20, y+20))
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

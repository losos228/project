import multiprocessing as mp
import numpy as np
import pygame



green = (34,139,34)
#red = (255,0,0)
gameDisplay = pygame.display.set_mode((900,500))



def distance(fr, to):
    dist = np.sqrt((fr[0]-to[0])**2+(fr[1]-to[1])**2)
    if dist != 0:
        return dist
    else:
        return 0.001

def diffWithin(a, b, maxDif):
    return np.abs(a-b) <= maxDif

import multiprocessing as mp
import numpy as np
import pygame



green = (34,139,34)
#red = (255,0,0)
gameDisplay = pygame.display.set_mode((900,500))



def distance(A, B):
    """
    ----------------------------------------------------
    Function to:
    calculate the distance from A to B
    ----------------------------------------------------
    Parameters:
    A(float,float): coordinates of point A
    B(float,float): coordinates of point B

    Note: Both input parameters can have len() longer 
    than 2, as long as the first 2 elements are floats 
    the function will function as intended.
    ----------------------------------------------------
    Returns:
    (float) the distance from A to B
    ----------------------------------------------------
    """
    dist = np.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)
    if dist != 0:
        return dist
    else:
        return 0.001

def diffWithin(a, b, maxDif):
    """
    ----------------------------------------------------
    Function to:
    Check wether the absolute difference beetween 
    a and b is not bigger than maxDif
    ----------------------------------------------------
    Parameters:
    a(float): the first number to check
    b(float): the seccond number to check
    maxDiff(float):
    ----------------------------------------------------
    Returns:
    (bool) wether the absolute difference between 
    a and b is not bigger than maxDif
    ----------------------------------------------------
    """
    return np.abs(a-b) <= maxDif

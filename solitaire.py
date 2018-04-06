import math
import numpy as np

class Field:
  '''class to describe a solitaire field'''


  parent_of ={}
    
  def __init__(self, stones, name, parent):
    self.stones = stones
    self.name = name
    self.final = None
    self.parent_of[name] = parent
    
  def new(hole, name):
    stones = np.ones((7,7),np.int)
    stones[ 0:2, 0:2] = np.zeros((2,2))
    stones[ 0:2,-2: ] = np.zeros((2,2))
    stones[-2: , 0:2] = np.zeros((2,2))
    stones[-2: ,-2: ] = np.zeros((2,2))
    if stones[hole] != 0:
      stones[hole] = -1
      return Field(stones, name, parent=None)
    else:
      raise NameError("Initial hole is outside the board!")
      
  def isOnBoard(self, coord):
    if (coord[0] < 0) \
    or (coord[1] < 0) \
    or (coord[0] >= len(self.stones)) \
    or (coord[1] >= len(self.stones[0])):
      return False
    elif self.stones[coord] == 0:
      return False
    else:
      return True
  
  def neighbours(self, coord):
    list_of_neighbours = []
    ncoords = [(coord[0],coord[1]-1),
               (coord[0],coord[1]+1),
               (coord[0]-1,coord[1]),
               (coord[0]+1,coord[1])]
    nncoords = [(coord[0],coord[1]-2),
                (coord[0],coord[1]+2),
                (coord[0]-2,coord[1]),
                (coord[0]+2,coord[1])]
    
    for n, nn in zip(ncoords, nncoords):
      if self.isOnBoard(n) and self.stones[n] == 1:
        if self.isOnBoard(nn) and self.stones[nn] ==1:
          list_of_neighbours.append((n,nn))
      
    return list_of_neighbours
    
  def holeCoords(self):
    list_of_holes = []
    for i in range(len(self.stones)):
      for j in range(len(self.stones[0])):
        if self.stones[(i,j)] == -1:
          if len(self.neighbours((i,j))) > 0:
            list_of_holes.append((i,j))
    
    if len(list_of_holes) = 0:
      self.final = True
    else:
      self.final = False
      
    return list_of_holes
    
  def isFinal(self):
    return False
  
  def next(self):
    pass
    
  

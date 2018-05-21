import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy as cp


class Field:
  '''class to describe a solitaire field'''

  # class variables, shared by all objects
  parent_of = {}  # name: [parent, final, stage]
  last_name = []  # last name having been used for a field (needed to name new fields)
  max_stage = []  # stores the highest reached stage
  fields = {}  # name: field
  stage = {}  # stage: [names of fields belonging to that stage]

  def __init__(self, stones, name, parent):
    self.name = name  # a unique number
    self.stones = stones  # the distribution of stones on the field
    self.children = {}  # link the children objects
    self.final = None  # true if field has no children or if all of its' children are final

    self.parent_of[name] = [parent, None, self.get_stage()]
    if len(self.last_name) == 0:  # first run
      self.last_name.append(cp.copy(name))
      self.fields[0] = self
      self.max_stage.append(0)
      self.stage[0] = [self.name]
    else:
      self.set_stage(self.get_stage(), name)
    if self.get_stage() > self.max_stage[0]:
      self.max_stage[0] = self.get_stage()

  @classmethod
  def new(cls, hole, name=None):  # creates a new starting field with specified starting hole
    if name is None:
      name = 0

    stones = np.ones((7, 7), np.int)
    stones[0:2, 0:2] = np.zeros((2, 2))
    stones[0:2, -2:] = np.zeros((2, 2))
    stones[-2:, 0:2] = np.zeros((2, 2))
    stones[-2:, -2:] = np.zeros((2, 2))
    if stones[hole] != 0:
      stones[hole] = -1
      return Field(stones, name, parent=None)
    else:
      raise NameError("Initial hole is outside the board!")

  def set_stage(self, stage, name):  # adds an entry to the stages dictionary
    if stage in self.stage.keys():
      self.stage[stage].append(name)
    else:
      self.stage[stage] = [name]

  def isOnBoard(self, coord):  # checks if stones are on the board
    if (coord[0] < 0) \
      or (coord[1] < 0) \
      or (coord[0] >= len(self.stones)) \
      or (coord[1] >= len(self.stones[0])):
      return False
    elif self.stones[coord] == 0:
      return False
    else:
      return True

  def neighbours(self, coord):  # returns a list of neighbours that contain stones to a given position
    list_of_neighbours = []
    ncoords = [(coord[0], coord[1]-1),
               (coord[0], coord[1]+1),
               (coord[0]-1, coord[1]),
               (coord[0]+1, coord[1])]
    nncoords = [(coord[0], coord[1]-2),
                (coord[0], coord[1]+2),
                (coord[0]-2, coord[1]),
                (coord[0]+2, coord[1])]

    for n, nn in zip(ncoords, nncoords):
      if self.isOnBoard(n) and self.stones[n] == 1:
        if self.isOnBoard(nn) and self.stones[nn] == 1:
          list_of_neighbours.append((n, nn))

    return list_of_neighbours
  
  def hole_coords(self):  # returns a list of holes of a given field
    list_of_holes = []
    for i in range(len(self.stones)):
      for j in range(len(self.stones[0])):
        if self.stones[(i, j)] == -1:
          if len(self.neighbours((i, j))) > 0:
            list_of_holes.append((i, j))
    if len(list_of_holes) == 0:
      self.final = True
    else:
      self.final = False
    self.parent_of[self.name][1] = self.final
  
    return list_of_holes
  
  def create_children(self):  # creates all children to a given field
    my_children = {}
    for h in self.hole_coords():
      for n, nn in self.neighbours(h):
        self.last_name[0] += 1
        my_children[self.last_name[0]] = {
          "hole": h,
          "neighbours": (n, nn),
          "final": None,
          "field": None
        }

    return my_children

  def go_forward(self):
    if len(self.children) == 0:
      my_children = self.create_children()
      if len(my_children) == 0:
        self.final = True
      if self.get_stage() == 31:
        print("Victory!!!!!!")
      else:
        self.final = True
        for k in my_children.keys():
          if not my_children[k]["final"]:
            self.final = False
            h, (n, nn) = my_children[k]["hole"], my_children[k]["neighbours"]
            stones = cp.copy(self.stones)
            stones[h] = 1
            stones[n] = -1
            stones[nn] = -1
            self.fields[k] = self.children[k] =Field(stones, name=k, parent=self.name)
 
  def is_final(self):  # a field is final if it has no children or all of its' children are final
    if not self.final:
      self.final = True
      for k in self.children.keys():
        if not self.children[k].final:
          self.final = False
          break

    return self.final

  def get_stage(self):
    return 32-(sum(sum(self.stones))+33)//2

  def next_child(self):
    for k in self.children.keys():
      if not self.children[k].final:
        return k
    return None
    
  def up_and_free(self):
    old_name = cp.copy(self.name)
    parent_name = self.parent_of[old_name][0]
    # print("parent: ", parent)
    stage = self.fields[old_name].get_stage()
    new_f = self.fields[parent_name]
    del(new_f.children[old_name])
    del(new_f.fields[old_name])
    del(new_f.parent_of[old_name])
    i = new_f.stage[stage].index(old_name)
    del(new_f.stage[stage][i])
    
    return new_f
    
  def field_comp(self, field):
    my_stones = -cp.copy(field.stones)
    for i in range(2):
      for j in range(4):
        if np.count_nonzero(self.stones - my_stones) == 0:
          return True
        my_stones = np.rot90(my_stones)
      my_stones = np.fliplr(my_stones)
 
    return False
  
  def plot_stones(self):
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig, ax = plt.subplots()
    for i, row in enumerate(self.stones):
      for j, stone in enumerate(row):
        if stone == 1:
          ax.scatter(i, j, s=100, c="red")
        elif stone == -1:
          ax.scatter(i, j, s=100, c="lightgrey")
    ax.set_title('solitaire field')
    ax.set_aspect(1.0)
    plt.show()
    plt.close()
  
  
# ============================================================================#

my_f = Field.new((2, 2), name=0)
max_stage = 0
stage = 0
while stage < 31:
  if my_f.name % 10000 == 0:
    print(my_f.name)
    print(my_f.stones)
  my_f.go_forward()
  if my_f.is_final():
    my_f = my_f.up_and_free()
  k = None
  while k is None:
    k = my_f.next_child()
    if k is None:
      my_f = my_f.up_and_free()
    else:
      my_f = my_f.children[k]

  stage = my_f.get_stage()
  if stage > max_stage:
    max_stage = cp.copy(stage)
    print(stage)


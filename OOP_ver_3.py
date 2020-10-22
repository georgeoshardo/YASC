#%%
import pymunk as pm
from pymunk.pyglet_util import DrawOptions
import numpy as np
import math
from numba import njit
import cell_geometry
from Cell import Cell
import cell_physics
import matplotlib.pyplot as plt
import cell_drawing

## DEFINE SPACE
space = pm.Space()
space.iterations = 100
options = DrawOptions()
options.collision_point_color = (0,0,0,0)
space.debug_draw(options)
space.gravity = 0,0

## ADD INITIAL CELLS
cell_1 = Cell(length = 15, width = 7.5, x_pos = 0, y_pos = 0, angle=0, colour = (1,0,0,1), perm_colour = (1,0,0,1), space = space)
cell_2 = Cell(length = 15, width = 7.5, x_pos = 0, y_pos = 0, angle=1, colour = (0,1,0,1), perm_colour = (0,1,0,1), space = space)

cells = [cell_1, cell_2]



#%%
## MAIN LOOP
import pymunk.matplotlib_util
for x in range(100):
    cell_physics.update(space,0.001,cells)
    cell_drawing.draw_scene(cells=cells,space=space,debug=True, savedir="ver_3", iteration=x)
    print(cell_2.length)
# %%

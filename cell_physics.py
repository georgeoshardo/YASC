import pymunk as pm
from pymunk.pyglet_util import DrawOptions
import numpy as np
import math
from numba import njit
import cell_geometry
from Cell import Cell
import itertools
def space_updater(dt, space, cells):
    #reset the space
    for x in range(len(space._get_shapes())):
        space._remove_shape(space._get_shapes()[0])
        space._remove_body(space._get_bodies()[0])
    for cell in cells:
        if radial_distance(cell) > 0:
            cell.growth(np.random.uniform(low = 0, high = 0.3) * (radial_distance(cell)))
        else:
            cell.growth(np.random.uniform(low = 0, high = 0.3) )
        cell.update_pm_object()
        #space.reindex_shape(cell.pm_object[0])
        #space.reindex_shapes_for_body(cell.pm_object[1])
        space.step(dt)
        if cell.is_dividing() == 1:
            cell.divide()
            space.step(dt)
            cell.update_pm_object()
            space.step(dt)
            daughter = Cell(length = cell.daughter_length(), width = cell.daughter_width(), x_pos = cell.daughter_x_pos(), y_pos = cell.daughter_y_pos(), angle=cell.daughter_angle(), colour=cell.perm_colour, perm_colour = cell.perm_colour, space = space)
            cells.append(daughter)
        cell_adder(cell)
        
        #resolve collisions from growth
        if len(cells) <= 20:
            for x in range(20):
                space.step(dt)
                cell.update_pm_object()
        elif len(cells) <= 300:
            for x in range(150):
                space.step(dt)
                cell.update_pm_object()
        elif len(cells) > 300:
            space.step(dt)
            cell.update_pm_object()

    #resolve collisions from forces:
    for x in range(100):
        for cell in cells:  
            if is_peripheral(cell):
                if (cell.x_pos + cell.y_pos) == 0:
                    pass
                else:
                    norm = np.sqrt((cell.x_pos)**2 + (cell.y_pos)**2)
                    cell.pm_object[1].apply_force_at_local_point((-1*cell.x_pos/(norm * np.sqrt(len(cells))), -1*cell.y_pos/(norm* np.sqrt(len(cells)))), (0, 0))
        space.step(dt)


    #for cell in cells:#[cells[i] for i in rand_force_cells]:
    #    cell.pm_object[1].apply_force_at_local_point((-25*cell.x_pos*np.exp(-0.01*len(cells)), -25*cell.y_pos *np.exp(-0.01*len(cells))), (0, 0))
    #    space.step(dt)
    #print(len(cells))
    #print(cell_1.pm_object[1].angle)

def is_peripheral(cell):
    x_s, y_s = [], []
    for x in range(len(cells)):
        x_s.append(abs(cells[x].x_pos))
        y_s.append(abs(cells[x].y_pos))
    colony_size = np.sqrt((max(x_s))**2 + (max(y_s))**2)
    #print(colony_size)
    distance = np.sqrt((cell.x_pos)**2 + (cell.y_pos)**2)
    if distance > 0.85*colony_size:
        return 1
    else:
        return 0

def radial_distance(cell):
    size = colony_size()
    #print(colony_size)
    distance = np.sqrt((cell.x_pos)**2 + (cell.y_pos)**2)
    if distance/size > 0.9:
        return 1
    else:
        return distance/size

def colony_size():
    x_s, y_s = [], []
    for x in range(len(cells)):
        x_s.append(abs(cells[x].x_pos))
        y_s.append(abs(cells[x].y_pos))
    colony_size = np.sqrt((max(x_s))**2 + (max(y_s))**2)
    return colony_size

def radial_growth_function(r):
    return 1 - np.exp(-2*r)

def colony_CoM(cells):
    length = len(cells)
    centroids = np.zeros((length,2))
    a = 0
    for cell in cells:
        centroids[a] = cell.pm_object[1].position
        a +=1
    sum_x = np.sum(centroids[:, 0])
    sum_y = np.sum(centroids[:, 1])
    return sum_x/length, sum_y/length

def cell_adder(cell, space):
    space.add(cell.pm_object)


def update(space,dt, cells):
    
    for __ in itertools.repeat(None, len(space._get_shapes())):
        space._remove_shape(space._get_shapes()[0])
        space._remove_body(space._get_bodies()[0])


    for cell in cells:
        cell.update()
           


    for cell in cells:
        space.add(cell.pm_object)


    for __ in itertools.repeat(None, 100):
        space.step(dt)
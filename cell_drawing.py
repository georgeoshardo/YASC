import pymunk as pm
from pymunk.pyglet_util import DrawOptions
import numpy as np
import math
from numba import njit
import cell_geometry
from Cell import Cell
import cell_physics
import matplotlib.pyplot as plt

def draw_scene(cells, space, debug, savedir, iteration):   
    fig = plt.figure(figsize=(5,5))
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
    ax.set_aspect("equal")
    ax.set_facecolor((0,0,0))
    plt.axis('off') 

    for cell in cells:
        plt.plot(cell.draw_2()[0], cell.draw_2()[1])
        #plt.plot(cell.draw()[0], cell.draw()[1])
        plt.scatter(cell.x_pos, cell.y_pos, s=30, zorder=100)

    if debug == True:
        o = pm.matplotlib_util.DrawOptions(ax)
        o.collision_point_color = (0,0,0,0)
        space.debug_draw(o)

    fig.savefig(savedir+"/image{}.png".format(str(iteration).zfill(3)), bbox_inches="tight")
    plt.close("all")
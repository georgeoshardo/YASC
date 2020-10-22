from numba import njit
import math
import numpy as np

@njit
def circ(theta, start, radius):
    y = radius * np.cos(theta) +radius
    x = radius * np.sin(theta) + start + radius
    return x, y
@njit
def wall(radius, start, end, t_or_b, resolution):
    wall_x = np.linspace(start, end, resolution)
    wall_y = np.ones(resolution)*radius * t_or_b +radius
    return wall_x, wall_y

def get_cell_vertices_for_draw(cell_length, cell_width, resolution):

    cell_width = cell_width/2
    left_wall = circ(np.linspace(np.pi,2*np.pi, resolution), 0, cell_width)
    top_wall_xy = wall(cell_width, cell_width, cell_length, 1, resolution)
    bottom_wall_xy = wall(cell_width, cell_width, cell_length, -1, resolution)
    right_wall = circ(np.linspace(0,np.pi, resolution), cell_length - cell_width, cell_width)
    return [[left_wall[0][x] - cell_length/2, left_wall[1][x] - cell_width/2] for x in reversed(range(len(left_wall[0])))] + \
            [[bottom_wall_xy[0][x] - cell_length/2, bottom_wall_xy[1][x]- cell_width/2] for x in (range(len(bottom_wall_xy[0])))] + \
            [[right_wall[0][x] - cell_length/2, right_wall[1][x]- cell_width/2] for x in reversed(range(len(right_wall[0])))] + \
            [[top_wall_xy[0][x] - cell_length/2, top_wall_xy[1][x]- cell_width/2] for x in reversed(range(len(top_wall_xy[0])))]

@njit
def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return qx, qy

def vertices(x_pos, y_pos, length, width, resolution, angle):
    points = np.array(get_cell_vertices_for_draw(length, width, resolution))
    points[:,0] = points[:,0] + x_pos
    points[:,1] = points[:,1] + y_pos

    rotated = np.zeros((len(points),2))
    for x in range(len(points)):
        rotated[x] = rotate((x_pos, y_pos), (points[x][0],points[x][1]), angle)

    return rotated
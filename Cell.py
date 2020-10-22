import pymunk as pm
from pymunk.pyglet_util import DrawOptions
import numpy as np
import math
from numba import njit
import cell_geometry
import itertools
class Cell:
    def __init__(self,
    length, 
    width, 
    x_pos, 
    y_pos, 
    colour,
    perm_colour,
    space,
    angle = 0, 
    resolution = 30, 
    model = "adder", 
    food_conc = 5, 
    mass = 0.1, 
    friction = 0, 
    body = 0,
    poly = 0,
    division_threshold = 30,
    mother = None):
        self.length = length
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.angle = angle
        self.resolution = resolution
        self.model = model
        self.food_conc = food_conc
        self.mass = mass
        self.friction = friction
        self.colour = colour
        self.perm_colour = perm_colour
        self.space = space
        self.division_threshold = division_threshold
        self.mother = mother
        self.body = body
        self.poly = poly
        self.pm_object = self.initialise_pm_object()

    def initialise_pm_object(self):
        self.poly = pm.Poly(None, cell_geometry.vertices(0, 0, self.length, self.width, self.resolution, self.angle))
        self.poly.color = self.colour
        self.poly.friction = self.friction
        _moment = pm.moment_for_poly(self.mass, self.poly.get_vertices())
        self.body = pm.Body(self.mass, _moment)
        self.poly.body = self.body
        self.body.center_of_gravity = self.centroid()
        self.body.angle = self.angle
        self.body.position = self.x_pos, self.y_pos
        self.space.reindex_shapes_for_body(self.body)
        return self.poly, self.body

    def update_position(self):
        self.x_pos, self.y_pos = self.body.local_to_world(self.body.center_of_gravity)
        self.angle = self.body.angle


    def growth_rate(self):
        return self.food_conc

    def growth(self, dt):
        self.length = self.length + dt * self.growth_rate()

    def update_pm_object(self):
        self.poly = pm.Poly(None, cell_geometry.vertices(0, 0, self.length, self.width, self.resolution, self.angle))
        self.poly.color = self.colour
        self.poly.friction = self.friction
        _moment = pm.moment_for_poly(self.mass, self.poly.get_vertices())
        self.body = pm.Body(self.mass, _moment)
        self.poly.body = self.body
        self.body.center_of_gravity = self.centroid()
        self.body.angle = self.angle
        self.body.position = self.x_pos, self.y_pos
        self.space.reindex_shapes_for_body(self.body)
        self.pm_object =  self.poly, self.body

    def update(self):
        self.update_position()
        #self.growth(0.1)
        #self.update_pm_object()
        for __ in itertools.repeat(None, 1000):
            self.space.step(0.001)
        self.update_position()

    def is_dividing(self):
        if self.length > self.division_threshold * np.random.uniform(low = 0.9, high = 1.1):
            return 1
        if self.length < self.division_threshold:
            return 0
    def divide(self):
        self.length = self.length/2
        self.x_pos = self.x_pos - self.length/4 * np.cos(self.angle)
        self.y_pos = self.y_pos - self.length/4 * np.sin(self.angle)
        self.angle = np.random.uniform(low = self.angle - 2*np.pi*0.033, high = self.angle + 2*np.pi*0.033)

    def centroid(self):
        verts = cell_geometry.vertices(self.x_pos, self.y_pos, self.length, self.width, self.resolution, self.angle)
        length = verts.shape[0]
        sum_x = np.sum(verts[:, 0])
        sum_y = np.sum(verts[:, 1])
        return sum_x/length, sum_y/length

    def daughter_length(self):
        return self.length
    def daughter_width(self):
        return np.random.uniform(low = self.width*0.95, high = self.width*1.05)
    def daughter_x_pos(self):
        return self.x_pos + self.length/2 * np.cos(self.angle)
    def daughter_y_pos(self):
        return self.y_pos + self.length/2 * np.sin(self.angle)
    def daughter_angle(self):
        return np.random.uniform(low = self.angle - 2*np.pi*0.033, high = self.angle + 2*np.pi*0.033)
    def daughter_colour(self):
        return self.colour

    def draw(self):
        points = np.array(cell_geometry.get_cell_vertices_for_draw(self.length, self.width, self.resolution))
        points[:,0] = points[:,0] + self.x_pos
        points[:,1] = points[:,1] + self.y_pos

        rotated = np.zeros((len(points),2))
        for x in range(len(points)):
            rotated[x] = cell_geometry.rotate((self.x_pos, self.y_pos), (points[x][0],points[x][1]), self.angle)

        return (rotated[:,0], rotated[:,1])

    def draw_2(self):
        verts = list(map(self.body.local_to_world, self.poly.get_vertices()))
        verts_x = [verts[x][0] for x in range(len(verts))]
        verts_y = [verts[x][1] for x in range(len(verts))]
        return (verts_x, verts_y)
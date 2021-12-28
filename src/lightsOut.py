import pygame
import math
import numpy as np

import galois
#import scipy.linalg as sp
import sage as sg
from sympy import Matrix, Rational, mod_inverse, pprint

### Globals ###

pygame.init()

adj = [[0, 0], [0, -1], [-1, 0], [0, 1], [1, 0]]

BOARD_SIZE = 5
TILE_HEIGHT = 50
TILE_WIDTH = 50
MARGIN = 2

# This is the distance multiplier to enable gaps between the polygons
DISTANCE = 1.1

# This is the scale multiplier. All coordinates for polygons are done with a unit length of 1,
# so this is the number of pixels per unit length
SCALE = 50

# Set the state colors
ON_COLOR = (255, 0, 0)
OFF_COLOR = (0, 255, 0)

GRID_SIZE = [20, 20]


def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    return numer * mod_inverse(denom, modulus) % modulus

def polarToCart(dist, angle):
    angle = math.radians(angle)
    x = int(dist * math.cos(angle))
    y = int(dist * math.sin(angle))
    return x, y

class Solver:

    def getSolveMtx(self, puzzle):
        return np.concatenate((puzzle.getAdjacencyMtx(), puzzle.getStateMtx()[:, None]), axis=1)

    def solveRREF(self, puzzle):
        mtx = Matrix(self.getSolveMtx(puzzle))
        mtx = mtx.rref(iszerofunc=lambda x: x % 2 == 0)
        mtx = mtx[0].applyfunc(lambda x: mod(x, 2))
        mtx = mtx.col(-1).reshape(len(puzzle.getGameGrid()), len(puzzle.getGameGrid()))
        return mtx


class Polygon:
    shape = None
    adjPolygons = None
    state = False
    position = None
    rotation = None
    points = None
    polyid = None
    polyMan = None

    def __init__(self, polyMan, polyid, position, rotation, points, adjPolygons):
        self.polyMan = polyMan
        self.polyid = polyid
        self.position = position
        self.rotation = rotation
        self.points = points
        self.adjPolygons = adjPolygons

    def __repr__(self):
        return "PolyID: " + str(self.polyid) + ", Position: " + str(self.position) + ", Rotation: " + str(self.rotation)

    def build(self):
        self.transformPoints()
        self.drawClickMap()
        self.drawPolygon()
        self.spawnAdjPolygons()

    def transformPoints(self):
        (px, py) = self.position
        rot = self.rotation*math.pi/180

        for i, point in enumerate(self.points):
            (ox, oy) = point
            qx = (math.cos(rot) * ox) - (math.sin(rot) * oy)
            qy = (math.sin(rot) * oy) + (math.cos(rot) * oy)
            self.points[i] = (qx + px, qy + py)

        # for i, point in enumerate(self.points):
        #     (ox, oy) = point
        #     qx = ox + math.cos(rot) * (px - ox) - math.sin(rot) * (py - oy)
        #     qy = oy + math.sin(rot) * (px - ox) + math.cos(rot) * (py - oy)
        #     self.points[i] = (qx, qy)

        print(self.points)

    def getAdjPolygons(self):
        return self.adjPolygons

    def getState(self):
        return self.state

    def spawnAdjPolygons(self):
        self.adjPolygons = [self.polyMan.createPolygon(shape = adjPolygon.getShape(),
                                                       position = adjPolygon.getPosition(),
                                                       rotation = adjPolygon.getRotation())
                            for adjPolygon in self.adjPolygons]
        self.adjPolygons = [i for i in self.adjPolygons if i]

    def drawPolygon(self):
        if self.getState() == True:
            pygame.draw.polygon(gameBoard, ON_COLOR, self.points)
        else:
            pygame.draw.polygon(gameBoard, OFF_COLOR, self.points)

        screen.blit(gameBoard, (0, 0))
        pygame.display.update()
        return None

    def drawClickMap(self):
        pygame.draw.polygon(clickMap, self.polyid, self.points)
        screen.blit(clickMap, (0, 0))
        pygame.display.update()


class AdjPolygon:

    def __init__(self, shape, angle=0, distance=SCALE*DISTANCE,  rotation=0):
        self.shape = shape
        self.angle = angle
        self.distance = distance
        self.position = polarToCart(round(distance, 2), angle)
        self.rotation = rotation

    def __repr__(self):
        return "Shape: " + str(self.shape) + ", Angle: " + str(self.angle) + ", Distance: " + str(self.distance) + \
               ", Position: ", self.position, "Rotation: " + str(self.rotation)

    def getShape(self):
        return self.shape

    def getPosition(self):
        return self.position

    def getRotation(self):
        return self.rotation

    def incRotation(self, rotation):
        self.rotation += rotation

    def incPosition(self, position):
        self.position = tuple(map(sum, zip(self.position, position)))

class PolygonManager:

    polygons = []

    def createPolygon(self, shape, position=(0, 0), rotation=0):

        maxSize = pygame.display.get_surface().get_size()
        if any(x > y for x, y in zip(position, maxSize)) or any(x < y for x, y in zip(position, (0, 0))):
            return None
        pid = pygame.Surface.get_at(clickMap, position)
        pid = (pid[0] << 16) + (pid[1] << 8) + pid[2]
        if pid == ((255 << 16) + (255 << 8) + 255):  # If the point is white, no point exists there
            points, adjPolygons = self.getPolygonData(shape)
            if len(self.polygons) == 0 and position == (0, 0):  # Offset the first point by its minimum spatial values
                position = tuple(map(abs, min(points, key=lambda t: t[1])))
            map(lambda x: x.incRotation(rotation), adjPolygons)
            map(lambda x: x.incPosition(position), adjPolygons)
            polygon = Polygon(polyMan = self, polyid = len(self.polygons), position = position, rotation = rotation,
                              points = points, adjPolygons = adjPolygons)
            self.polygons.append(polygon)
            print("Built ", repr(polygon))
            polygon.build()
        else:
            polygon = self.getPolygon(pid)


        return polygon

    def getPolygon(self, polyid):
        return self.polygons[polyid]

    def getPolygons(self):
        return self.polygons

    @staticmethod
    def getPolygonData(shape):

        if shape == "Square":
            points = [(-0.5, -0.5), (-0.5, .5), (0.5, 0.5), (0.5, -0.5)]
            adjPolygons = [
                AdjPolygon(shape="Square", angle=0),
                AdjPolygon(shape="Square", angle=90),
                AdjPolygon(shape="Square", angle=180),
                AdjPolygon(shape="Square", angle=270)
            ]
        elif shape == "Triangle":
            points = [(0, 0.5), (-0.5, -0.5), (0.5, -0.5)]
            adjPolygons = [
                AdjPolygon(shape="Triangle", angle=60,  rotation=180),
                AdjPolygon(shape="Triangle", angle=180, rotation=180),
                AdjPolygon(shape="Triangle", angle=300, rotation=180)
            ]

        def scalePos(position):
            (x, y) = position
            return (x*SCALE, y*SCALE)

        points = [scalePos(element) for element in points]
        return points, adjPolygons


class LightsOut:

    polygons = None
    moves = None
    gameGrid = None
    polyMan = PolygonManager()

    def __init__(self, fname=None):
        self.polyMan.createPolygon("Square")
        # if fname is not None:
        #     self.load_level(fname)
        #print(self.getAdjacencyMtx())
        # self.drawGame()
        # self.drawClickMap()

    # def load_level(self, fname):
    #     lstr = []
    #     f = open(fname)
    #     for line in f:
    #         lstr += [line.split()[0]]
    #     f.close()
    #     for y in range(len(lstr)):
    #         for x in range(len(lstr[y])):
    #             self.grid[x][y] = int(lstr[y][x])

    def drawGame(self):
        # for y in range(BOARD_SIZE):
        #     for x in range(BOARD_SIZE):
        #         i = x * TILE_WIDTH + MARGIN
        #         j = y * TILE_HEIGHT + MARGIN
        #         h = TILE_HEIGHT - (2 * MARGIN)
        #         w = TILE_WIDTH - (2 * MARGIN)
        #         if self.gameGrid[y][x] == 1:
        #             pygame.draw.rect(screen, (105, 210, 231), [i, j, w, h])
        #         else:
        #             pygame.draw.rect(screen, (255, 255, 255), [i, j, w, h])
        for polygon in self.polygons:
            polygon.drawPolygon()

    def drawClickMap(self):
        for polygon in self.polygons:
            polygon.drawClickMap()

    def getAdjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < BOARD_SIZE) and (0 <= j + y < BOARD_SIZE):
                adjs += [[i + x, j + y]]
        return adjs

    def click(self, polyID):
        print(polyID)


    # def click(self, pos):
    #     x = math.floor(pos[0] / TILE_WIDTH)
    #     y = math.floor(pos[1] / TILE_HEIGHT)
    #     print("Clicked: (",x,", ",y,")")
    #     self.press(x,y)

    def press(self,x,y):
        adjs = self.getAdjacent(x, y)
        for i, j in adjs:
            self.gameGrid[j][i] = (self.gameGrid[j][i] + 1) % 2

    def getGameGrid(self):
        return self.gameGrid

    def getSolveGrid(self):
        return self.solveGrid

    def getAdjacencyMtx(self):
        elems = len(self.gameGrid)*len(self.gameGrid[0])
        adj = [[0 for i in range(elems)] for j in range(elems)]
        for n in range(elems):
            x = n % len(self.gameGrid)
            y = n // len(self.gameGrid)
            adjs = self.getAdjacent(x, y)
            for i, j in adjs:
                adj[n][i+j*len(self.gameGrid)] = 1
        return np.array(adj)

    def getStateMtx(self):
        return np.array(self.gameGrid).flatten()

    def getSolveMtx(self):
        return

    def addPolygon(self, polygon):
        self.polygons.append(polygon)



### Main ###

if __name__ == "__main__":

    gameSize = (GRID_SIZE[0] * SCALE, GRID_SIZE[1]*SCALE)

    screen = pygame.display.set_mode(gameSize)
    screen.fill((167, 219, 216))

    # Add the hit detection via a surface hidden below the game where the color of each polygon is equal to it's ID
    clickMap = pygame.Surface(gameSize)
    clickMap.fill((255, 255, 255))
    screen.blit(clickMap, (0, 0))

    # Add the actual game board
    gameBoard = pygame.Surface(gameSize)
    gameBoard.fill((255, 255, 255))
    screen.blit(gameBoard, (0, 0))

    pygame.display.set_caption("Lights Out")

    game = LightsOut()

    clock = pygame.time.Clock()

    keepGoing = True
    while keepGoing:

        clock.tick(30)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clickid = pygame.Surface.get_at(clickMap, pos)
                clickid = (clickid[0] << 16) + (clickid[1] << 8) + clickid[2]
                game.click(clickid)

        pygame.display.flip()
    pygame.quit()

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


class LightsOut:

    polygons = None
    moves = None
    gameGrid = None

    def __init__(self, fname=None):
        self.clear()
        # if fname is not None:
        #     self.load_level(fname)
        print(self.getAdjacencyMtx())

    def clear(self):
        self.gameGrid = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

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

    def click(self, polyid):



    def click(self, pos):
        x = math.floor(pos[0] / TILE_WIDTH)
        y = math.floor(pos[1] / TILE_HEIGHT)
        print("Clicked: (",x,", ",y,")")
        self.press(x,y)

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


def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    return numer * mod_inverse(denom, modulus) % modulus


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

    def __init__(self, polyid, position, rotation, points, adjPolygons):
        self.polyid = polyid
        self.position = position
        self.rotation = rotation
        self.points = points
        self.adjPolygons = adjPolygons

    def build(self):
        self.transformPoints()
        self.spawnAdjPolygons()

    def transformPoints(self):
        px, py = self.position
        rot = self.rotation*math.pi/180

        for i, point in enumerate(self.points):
            ox, oy = point
            qx = ox + math.cos(rot) * (px - ox) - math.sin(rot) * (py - oy)
            qy = oy + math.sin(rot) * (px - ox) + math.cos(rot) * (py - oy)
            self.points[i] = [qx, qy]

    def getAdjPolygons(self):
        return self.adjPolygons

    def getState(self):
        return self.state

    def spawnAdjPolygons(self):

        newPolygons = None
        for adj in self.adjPolygons:
            1+1

        return 5

    def drawPolygon(self):
        if self.getState() == True:
            pygame.draw.polygon(gameBoard, ON_COLOR, self.points)
        else:
            pygame.draw.polygon(gameBoard, OFF_COLOR, self.points)
        return None

    def drawClickMap(self):
        pygame.draw.polygon(clickMap, self.polyid, self.points)


class AdjPolygon:
    def __init__(self, shape, angle=0, distance=SCALE*DISTANCE,  rotation=0):
        self.shape = shape
        self.angle = angle
        self.distance = math.round(distance, 2)
        self.rotation = rotation

    def __repr__(self):
        return "Shape: " + str(self.getShape()) + ", Angle: " + str(self.getAngle()) + \
               ", Distance: " + str(self.getDistance()) + ", Rotation: " + str(self.getRotation())

    def getShape(self):
        return self.shape

    def getAngle(self):
        return self.angle

    def getDistance(self):
        return self.distance

    def getRotation(self):
        return self.rotation

    def incRotation(self, rotation):
        self.rotation += rotation

class PolygonManager:

    polygons = []

    def createPolygon(self, shape, position, rotation):

        pid = pygame.Surface.get_at(clickMap, pos)
        pid = (pid[0] << 16) + (pid[1] << 8) + pid[2]
        if pid == ((255 << 16) + (255 << 8) + 255):  # If the point is white, no point exists there
            points, adjPolygons = self.getPolygonData(shape)
            if len(self.polygons) == 0 and position == [0, 0]:  # Offset the first point by its minimum spatial values
                minpos = min(points, key=lambda t: t[1])
                position = [abs(num) for num in minpos]
            map(lambda x: x.incRotation(rotation), adjPolygons)
            polygon = Polygon(position, rotation, points, adjPolygons, len(self.polygons))
            self.polygons.append(polygon)
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
            points = [[-0.5, -0.5], [-0.5, .5], [0.5, 0.5], [0.5, -0.5]] * SCALE
            adjPolygons = [
                AdjPolygon(shape="Square", angle=0),
                AdjPolygon(shape="Square", angle=90),
                AdjPolygon(shape="Square", angle=180),
                AdjPolygon(shape="Square", angle=270)
            ]
        elif shape == "Triangle":
            points = [[0, 0.5], [-0.5, -0.5], [0.5, 0.5]] * SCALE
            adjPolygons = [
                AdjPolygon(shape="Triangle", angle=60,  rotation=180),
                AdjPolygon(shape="Triangle", angle=180, rotation=180),
                AdjPolygon(shape="Triangle", angle=300, rotation=180)
            ]
        return points, adjPolygons


def polarToCart(dist, angle):
    angle = math.radians(angle)
    x = dist * math.cos(angle)
    y = dist * math.sin(angle)
    return x, y

### Main ###

if __name__ == "__main__":

    screen = pygame.display.set_mode((BOARD_SIZE * TILE_WIDTH, BOARD_SIZE * TILE_HEIGHT))
    screen.fill((167, 219, 216))

    # Add the hit detection via a surface hidden below the game where the color of each polygon is equal to it's ID
    clickMap = pygame.Surface((BOARD_SIZE * TILE_WIDTH, BOARD_SIZE * TILE_HEIGHT))
    clickMap.fill((255, 255, 255))
    screen.blit(clickMap, (0, 0))

    # Add the actual game board
    gameBoard = pygame.Surface((BOARD_SIZE * TILE_WIDTH, BOARD_SIZE * TILE_HEIGHT))
    gameBoard.fill((255, 255, 255))
    screen.blit(gameBoard, (0, 0))

    pygame.display.set_caption("Lights Out")

    game = LightsOut()

    clock = pygame.time.Clock()

    keepGoing = True
    while keepGoing:

        clock.tick(30)

        #game.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                polyid = pygame.Surface.get_at(clickMap, pos)
                polyid = (polyid[0] << 16) + (polyid[1] << 8) + polyid[2]
                game.click(polyid)

        pygame.display.flip()
    pygame.quit()

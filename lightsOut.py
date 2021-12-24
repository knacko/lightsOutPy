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

#This is the distance multiplier to enable gaps between the polygons
DISTANCE = 1.1

# This is the scale multiplier. All coordinates for polygons are done with a unit length of 1,
# so this is the number of pixels per unit length
SCALE = 50

### LightsOut Class ###


class LightsOut:

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

    def draw(self):
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                i = x * TILE_WIDTH + MARGIN
                j = y * TILE_HEIGHT + MARGIN
                h = TILE_HEIGHT - (2 * MARGIN)
                w = TILE_WIDTH - (2 * MARGIN)
                if self.gameGrid[y][x] == 1:
                    pygame.draw.rect(screen, (105, 210, 231), [i, j, w, h])
                else:
                    pygame.draw.rect(screen, (255, 255, 255), [i, j, w, h])

    def getAdjacent(self, x, y):
        adjs = []
        for i, j in adj:
            if (0 <= i + x < BOARD_SIZE) and (0 <= j + y < BOARD_SIZE):
                adjs += [[i + x, j + y]]
        return adjs

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


class Solver:

    def mod(x, modulus):
        numer, denom = x.as_numer_denom()
        return numer * mod_inverse(denom, modulus) % modulus

    def getSolveMtx(self, puzzle):
        return np.concatenate((puzzle.getAdjacencyMtx(), puzzle.getStateMtx()[:, None]), axis=1)

    def solveRREF(self, puzzle):
        mtx = Matrix(self.getSolveMtx(puzzle))
        mtx = mtx.rref(iszerofunc=lambda x: x % 2 == 0)
        mtx = mtx[0].applyfunc(lambda x: self.mod(x, 2))
        mtx = mtx.col(-1).reshape(len(puzzle.getGameGrid()), len(puzzle.getGameGrid()))
        return mtx


class Polygon:
    shape = None
    adjPolygons = None
    state = False
    position = None
    rotation = None
    points = None

    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

    def build(self):
        self.transformPoints()
        self.draw()
        self.spawnAdjPolygons()

    def transformPoints(self):
        px, py = self.position
        rot = self.rotation*math.pi/180

        for i, point in enumerate(self.points):
            ox, oy = point
            qx = ox + math.cos(rot) * (px - ox) - math.sin(rot) * (py - oy)
            qy = oy + math.sin(rot) * (px - ox) + math.cos(rot) * (py - oy)
            self.points[i] = [qx,qy]

    def getAdjPolygons(self):
        return self.adjPolygons

    def state(self):
        return self.state

    def spawnAdjPolygons(self):
        return None

    def draw(self):
        return None


class AdjPolygon:
    def __init__(self, shape, angle=0, distance=SCALE*DISTANCE,  rotation=0):
        self.shape = shape
        self.angle = angle
        self.distance = distance
        self.rotation = rotation

    def getShape(self):
        return self.shape

    def getPosition(self):
        return self.position

    def getDistance(self):
        return self.distance

    def getRotation(self):
        return self.rotation

    def incRotation(self, rotation):
        self.rotation += rotation


class SquarePolygon(Polygon):

    def __init__(self, position, rotation):

        super().__init__(self, position, rotation)

        self.points = [[-0.5,-0.5],[-0.5,.5],[0.5,0.5],[0.5,-0.5]]*SCALE

        self.adjPolygons = [
            AdjPolygon(shape="Square", angle=0),
            AdjPolygon(shape="Square", angle=90),
            AdjPolygon(shape="Square", angle=180),
            AdjPolygon(shape="Square", angle=270)
        ]

        # self.adjPolygons = [
        #     AdjPolygon(shape = "Square", angle = 0,   distance = SCALE*DISTANCE, rotation = 0),
        #     AdjPolygon(shape = "Square", angle = 90,  distance = SCALE*DISTANCE, rotation = 0),
        #     AdjPolygon(shape = "Square", angle = 180, distance = SCALE*DISTANCE, rotation = 0),
        #     AdjPolygon(shape = "Square", angle = 270, distance = SCALE*DISTANCE, rotation = 0)
        # ]

        self.build()



def polarToCart(dist, angle):
    angle = math.radians(angle)
    x = dist * math.cos(angle)
    y = dist * math.sin(angle)
    return x,y

### Main ###

if __name__ == "__main__":

    screen = pygame.display.set_mode((BOARD_SIZE * TILE_WIDTH, BOARD_SIZE * TILE_HEIGHT))
    screen.fill((167, 219, 216))
    pygame.display.set_caption("Lights Out")

    game = LightsOut()

    clock = pygame.time.Clock()

    keepGoing = True
    while keepGoing:

        clock.tick(30)

        game.draw()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                keepGoing = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.click(pos)

        pygame.display.flip()
    pygame.quit()

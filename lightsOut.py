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

### LightsOut Class ###

class LightsOut:

    def __init__(self, fname=None):
        self.clear()
        # if fname is not None:
        #     self.load_level(fname)
        print(self.getAdjacencyMtx())

    def clear(self):
        self.grid = [[0 for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]

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
                if self.grid[y][x] == 1:
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
            self.grid[j][i] = (self.grid[j][i] + 1) % 2
        pprint(self.solvePuzzle())

    def getGrid(self):
        return self.grid

    def getAdjacencyMtx(self):
        elems = len(self.grid)*len(self.grid[0])
        adj = [[0 for i in range(elems)] for j in range(elems)]
        for n in range(elems):
            x = n % len(self.grid)
            y = n // len(self.grid)
            adjs = self.getAdjacent(x, y)
            for i, j in adjs:
                adj[n][i+j*len(self.grid)] = 1
        return np.array(adj)

    def getStateMtx(self):
        return np.array(self.grid).flatten()

    def getSolveMtx(self):
        return np.concatenate((self.getAdjacencyMtx(), self.getStateMtx()[:,None]),axis=1)

    def solvePuzzle(self):
        mtx = Matrix(self.getSolveMtx())
        mtx = mtx.rref(iszerofunc=lambda x: x % 2 == 0)
        mtx = mtx[0].applyfunc(lambda x: mod(x, 2))
        mtx = mtx.col(-1).reshape(len(self.grid), len(self.grid))
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
        self.draw()

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
    def __init__(self, shape, position = 0, distance = 0, rotation = 0):
        self.shape = shape
        self.position = position
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

class PolygonManager:





def mod(x, modulus):
    numer, denom = x.as_numer_denom()
    return numer*mod_inverse(denom,modulus) % modulus

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

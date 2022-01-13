import pygame
import numpy as np
from PolygonManager import PolygonManager
import config
import Solver as Solver

# import galois
# import sage as sg
# from sympy import Matrix, Rational, mod_inverse, pprint

pygame.init()


class LightsOut:

    polygons = None
    moves = None
    gameGrid = None

    def __init__(self, fname=None):
        self.polyMan = PolygonManager(self)
        position = tuple(x / 2 for x in pygame.display.get_surface().get_size())
        self.polyMan.createPolygon("OctogonSquare", position = position)

    def drawGame(self):
        for polygon in self.polygons:
            polygon.drawPolygon()

    def drawClickMap(self):
        for polygon in self.polygons:
            polygon.drawClickMap()

    def drawPolygon(self, surface, points, color):
        if surface == "GameBoard":
            pygame.draw.polygon(gameBoard, color, points)
            screen.blit(gameBoard, (0, 0))
        elif surface == "ClickMap":
            pygame.draw.polygon(clickMap, color, points)
            screen.blit(clickMap, (0, 0))
        pygame.display.update()

    def getPolygon(self, position):
        pid = pygame.Surface.get_at(clickMap, position)
        pid = (pid[0] << 16) + (pid[1] << 8) + pid[2]

        # If the point is white, no point exists there
        return pid if pid != ((255 << 16) + (255 << 8) + 255) else None

    def click(self, polyID):
        if polyID != ((255 << 16) + (255 << 8) + 255):
            self.polyMan.getPolygon(polyID).click()

    def getPolyMan(self):
        return self.polyMan

    def getAdjacencyMtx(self):
        polygons = self.polyMan.getPolygons()
        adjMtx = []
        for polygon in polygons:
            adj = [0 for i in range(len(polygons))]
            adjIDs = polygon.getAdjPolygonID()
            for adjID in adjIDs:
                adj[adjID] = 1
            adjMtx.append(adj)
        return adjMtx

    def getStateMtx(self):
        return list(map(int, [polygon.getState() for polygon in self.polyMan.getPolygons()]))

    def getSolveMtx(self):
        return np.c_[self.getAdjacencyMtx(), self.getStateMtx()]

        # return np.concatenate((s[:, None]), axis=1)

    def addPolygon(self, polygon):
        self.polygons.append(polygon)


if __name__ == "__main__":

    screen = pygame.display.set_mode(config.GAME_SIZE)
    screen.fill((167, 219, 216))

    # Add the hit detection via a surface hidden below the game where the color of each polygon is equal to it's ID
    clickMap = pygame.Surface(config.GAME_SIZE)
    clickMap.fill((255, 255, 255))
    screen.blit(clickMap, (0, 0))

    # Add the actual game board
    gameBoard = pygame.Surface(config.GAME_SIZE)
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
                print(Solver.solveRREF(game))

        pygame.display.flip()
    pygame.quit()

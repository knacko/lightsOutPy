import math
import AccFuncs
from sympy import pprint
import numpy as np
import config

class Polygon:
    game = None
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
        self.rotation = rotation % 360
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
        (ox, oy) = self.position
        rot = -math.radians(self.rotation)

        pprint(self.points)
        print(rot)

        for i, point in enumerate(self.points):
            (px, py) = point
            qx = (math.cos(rot) * px) - (math.sin(rot) * py)
            qy = (math.sin(rot) * px) + (math.cos(rot) * py)
            self.points[i] = (round(qx + ox), round(qy + oy))

        pprint(self.points)

        # for i, point in enumerate(self.points):
        #     (ox, oy) = point
        #     qx = ox + math.cos(rot) * (px - ox) - math.sin(rot) * (py - oy)
        #     qy = oy + math.sin(rot) * (px - ox) + math.cos(rot) * (py - oy)
        #     self.points[i] = (qx, qy)

    def getAdjPolygons(self):
        return self.adjPolygons

    def getAdjPolygonID(self):
        adjID = [adjPoly.getID() for adjPoly in self.getAdjPolygons()]
        adjID.insert(0, self.getID())
        return adjID

    def getState(self):
        return self.state

    def getID(self):
        return self.polyid

    def click(self, propogate = True):
        self.state = not self.state
        self.drawPolygon()
        if propogate:
            print("Internal click on " + str(self.polyid))
            #self.spawnAdjPolygons()
            for adjPolygon in self.adjPolygons:
                adjPolygon.click(propogate=False)

    def spawnAdjPolygons(self):
        self.adjPolygons = [self.polyMan.createPolygon(shape = adjPolygon.getShape(),
                                                       position = np.array(self.position) + adjPolygon.calcPosition(self.rotation),
                                                       rotation = self.rotation + adjPolygon.getRotation())
                            for adjPolygon in self.adjPolygons]
        self.adjPolygons = [i for i in self.adjPolygons if i]  # Removes the out-of-bounds polygons

    def drawPolygon(self):
        tileColor = config.ON_COLOR if self.getState() else config.OFF_COLOR
        self.polyMan.drawPolygon("GameBoard", self.points, tileColor)

    def drawClickMap(self):
        self.polyMan.drawPolygon("ClickMap", self.points, self.polyid)

    def drawAdjGuides(self):
        return None



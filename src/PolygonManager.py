from Polygon import Polygon
from AdjPolygon import AdjPolygon
import config
import math


class PolygonManager:

    polygons = []

    def __init__(self, game):
        self.game = game

    def drawPolygon(self, surface, points, color):
        self.game.drawPolygon(surface, points, color)

    def createPolygon(self, shape, position=(0, 0), rotation=0):

        maxSize = config.GAME_SIZE
        if any(x >= y-config.BORDER for x, y in zip(position, maxSize)) or \
                any(x <= y for x, y in zip(position, (config.BORDER, config.BORDER))):
            return None
        position = [int(n) for n in position]
        pid = self.game.getPolygon(position)
        if pid is None:
            points, adjPolygons = self.getPolygonData(shape)
            if len(self.polygons) == 0:  # Offset the first point by its minimum spatial values
                position = tuple(x/2 for x in maxSize)#tuple(map(abs, min(points, key=lambda t: t[1])))
            polygon = Polygon(polyMan = self, polyid = len(self.polygons), position = position, rotation = rotation,
                              points = points, adjPolygons = adjPolygons)
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
            points = [(-0.5, -0.5), (-0.5, .5), (0.5, 0.5), (0.5, -0.5)]
            adjPolygons = [
                AdjPolygon(shape="Square", angle=0),
                AdjPolygon(shape="Square", angle=90),
                AdjPolygon(shape="Square", angle=180),
                AdjPolygon(shape="Square", angle=270)
            ]
        elif shape == "Triangle":
            centerToTop = 1/math.sqrt(3)
            centerToBottom = math.sqrt(3)/6
            points = [(0, centerToTop),
                      (-0.5, -1 * centerToBottom),
                      (0.5,  -1 * centerToBottom)]
            adjPolygons = [
                AdjPolygon(shape="Triangle", angle=60,  distance = 2*centerToBottom, rotation=180),
                AdjPolygon(shape="Triangle", angle=180, distance = 2*centerToBottom, rotation=180),
                AdjPolygon(shape="Triangle", angle=300, distance = 2*centerToBottom, rotation=180)
            ]
        elif shape == "Hexagon":
            centerToTop = 0.5*math.sqrt(3)/2
            points = [(-.5, 0),
                      (-.25, centerToTop),
                      (.25, centerToTop),
                      (.5, 0),
                      (0.25, -centerToTop),
                      (-0.25, -centerToTop)]
            adjPolygons = [
                AdjPolygon(shape="Hexagon", angle=0,  distance=2*centerToTop, rotation=0),
                AdjPolygon(shape="Hexagon", angle=60,  distance=2*centerToTop, rotation=0),
                AdjPolygon(shape="Hexagon", angle=120, distance=2*centerToTop, rotation=0),
                AdjPolygon(shape="Hexagon", angle=180, distance=2*centerToTop, rotation=0),
                AdjPolygon(shape="Hexagon", angle=240, distance=2*centerToTop, rotation=0),
                AdjPolygon(shape="Hexagon", angle=300, distance=2*centerToTop, rotation=0)]
        elif shape == "SquareOctogon":
            squareUnitLength = 0.75  # This must match the value in SquareOctogon
            axisToAngle = squareUnitLength * math.sin(math.radians(45)) / math.sin(math.radians(90))
            points = [(0, axisToAngle),
                      (axisToAngle, 0),
                      (0, -axisToAngle),
                      (-axisToAngle, 0)]
            squareToOct = squareUnitLength + axisToAngle
            adjPolygons = [
                AdjPolygon(shape="OctogonSquare", angle=45,  distance=squareToOct, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=135, distance=squareToOct, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=225, distance=squareToOct, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=315, distance=squareToOct, rotation=0)]
        elif shape == "OctogonSquare":
            squareUnitLength = 0.75  # This must match the value in OctogonSquare
            axisToAngle = squareUnitLength * math.sin(math.radians(45)) / math.sin(math.radians(90))
            squareUnitLength /= 2
            axisToAngle += squareUnitLength
            points = [(-squareUnitLength, axisToAngle),
                      (squareUnitLength, axisToAngle),
                      (axisToAngle, squareUnitLength),
                      (axisToAngle, -squareUnitLength),
                      (squareUnitLength, -axisToAngle),
                      (-squareUnitLength, -axisToAngle),
                      (-axisToAngle, -squareUnitLength),
                      (-axisToAngle, squareUnitLength)]
            octToOct = 2 * axisToAngle
            octToSquare = axisToAngle + squareUnitLength
            adjPolygons = [
                AdjPolygon(shape="OctogonSquare", angle=0, distance=octToOct, rotation=0),
                AdjPolygon(shape="SquareOctogon", angle=45, distance=octToSquare, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=90, distance=octToOct, rotation=0),
                AdjPolygon(shape="SquareOctogon", angle=135, distance=octToSquare, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=180, distance=octToOct, rotation=0),
                AdjPolygon(shape="SquareOctogon", angle=225, distance=octToSquare, rotation=0),
                AdjPolygon(shape="OctogonSquare", angle=270, distance=octToOct, rotation=0),
                AdjPolygon(shape="SquareOctogon", angle=315, distance=octToSquare, rotation=0)]

        def scalePos(point):
            (x, y) = point
            return round(x*config.SCALE), round(y*config.SCALE)

        points = [scalePos(element) for element in points]

        return points, adjPolygons

import config
import AccFuncs


class AdjPolygon:

    def __init__(self, shape, angle=0, distance=1, rotation=0):
        """
        Data structure for a polygon that is adjacent to its parent polygon
        :param string shape: The name of the shape
        :param integer angle: The polar angle from the parent object
        :param distance: The polar distance from the parent object
        :param rotation: The rotation of the polygon relative the parent
        """
        self.shape = shape
        self.angle = angle
        self.distance = distance*config.SCALE*config.DISTANCE
        self.position = AccFuncs.polarToCart(self.distance, angle)
        self.rotation = rotation

    def __repr__(self):
        return "Shape: " + str(self.shape) + ", Angle: " + str(self.angle) + ", Distance: " + str(self.distance) + \
               ", Position: " + str(self.position) + ", Rotation: " + str(self.rotation) + "\n"

    def getShape(self):
        return self.shape

    def getRotation(self):
        return self.rotation

    def calcPosition(self, parentRotation):
        return AccFuncs.polarToCart(self.distance,
                                    self.angle + parentRotation + 90)  # TODO: Not sure why the +90 is necessary

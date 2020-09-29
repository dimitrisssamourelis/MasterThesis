import numpy as np

class Point:

    def __init__(self, x, y, refId):
        self.__coord = np.array([x, y])
        self.__refId = refId

    @property
    def x(self):
        return self.__coord[0]

    @property
    def y(self):
        return self.__coord[1]

    @property
    def coords(self):
        return self.__coord

    @property
    def id(self):
        return self.__refId

    def __gt__(self, otherPoint):
        if self.y > otherPoint.y:
            return True
        elif (self.y == otherPoint.y) & (self.x > otherPoint.x):
            return True
        else:
            return False

    def __str__(self):
        return "%d(%.3f, %.3f)"%(self.id, self.x, self.y)

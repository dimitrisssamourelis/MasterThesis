class Vector:

    def __init__(self, pointA, pointB):
        self._pointA = pointA
        self._pointB = pointB
        self._coords = pointB.coords - pointA.coords

    @property
    def pointA(self):
        return self._pointA

    @property
    def pointB(self):
        return self._pointB

    @property
    def coords(self):
        return self._coords

    def __str__(self):
        return "[%s -> %s]"%(str(self.pointA), str(self.pointB))

    def innerProduct(self, aVector):
        return np.dot(self.coords, aVector.coords)
    
    def formAdjacentTrianglesForCheck(self, pointA, pointB):
        first = self.pointA if self.pointA.id < self.pointB.id else self.pointB
        second = self.pointB if self.pointA.id < self.pointB.id else self.pointA
        testP1 = pointA if pointA.id < pointB.id else pointB
        testP2 = pointB if pointA.id < pointB.id else pointA

        if first.id >= 0:
            if testP1.id >= 0:
                xros1 = np.cross(Vector(first, second).coords, Vector(first, testP1).coords)
                xros2 = np.cross(Vector(first, second).coords, Vector(first, testP2).coords)
                if xros1*xros2 > 0:
                    return False
                else:
                    return True
            else:
                return False 
        else:
            if testP1.id < 0:
                return False
            else:
                small = testP2 if testP1 > testP2 else testP1
                large = testP1 if testP1 > testP2 else testP2
                xros = np.cross(Vector(small, second).coords, Vector(small, large).coords)
                return True if (((xros > 0) & (first.id == -2)) | ((xros < 0) & (first.id == -1))) else False


if __name__ == "__main__":
    from point import *
else:
    try:
        from .point import *
    except:
        from point import *


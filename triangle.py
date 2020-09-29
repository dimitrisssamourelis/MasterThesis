import numpy as np 
#rom .vector import *

class Triangle:
    def __init__(self, pointA, pointB, pointC):
        self.__points = {pointA.id : pointA, pointB.id : pointB, pointC.id : pointC }
        
        self.__nodeIds = np.array(list(self.__points.keys()))
        
        self.__containsMinusOne = np.isin(-1, self.__nodeIds)
        self.__containsMinusTwo = np.isin(-2, self.__nodeIds)
            
    def point(self, id):
        return self.__points[id] if id in self.__points else None
    
    @property
    def pointIds(self):
        return self.__nodeIds

    def containsMinusOneNode(self):
        return self.__containsMinusOne

    def containsMinusTwoNode(self):
        return self.__containsMinusTwo

    def hasEdge(self, pointA, pointB):
        return np.isin([pointA.id, pointB.id], self.__nodeIds).all()

    def getThirdNode(self, vector):
        points = np.array(list(self.__points.values()))
        theid = self.__nodeIds[np.isin(self.__nodeIds, [vector.pointA.id, vector.pointB.id]) == False][0]
        return self.__points[theid]

    def __str__(self):
        return "[%20s, %20s, %20s]"%tuple([str(self.point(x)) for x in list(self.pointIds)])
    
    def __eq__(self, otherTriangle):
        return np.isin(self.__nodeIds, otherTriangle.pointIds).all()

    def __isInMinusNodeTriangle(self, minusSide, aPoint):
        theids = list(self.__nodeIds[np.isin(self.__nodeIds, [minusSide]) == False])
        points = [self.point(x) for x in theids]
        pointA = points[0] if points[0] > points[1] else points[1]
        pointB = points[1] if points[0] > points[1] else points[0]
            
        xros = np.cross(Vector(pointA, pointB).coords, Vector(pointA, aPoint).coords)
        if xros > 0:
            flag1 = True if minusSide == -1 else False
        elif xros == 0:
            if (((pointA > aPoint) & (aPoint > pointB)) | ((pointB > aPoint) & (aPoint > pointA))):
                return True, Vector(pointA, pointB)
            else:
                return False, False
        else:
            flag1 = False if minusSide == -1 else True
        
        xros = np.cross(Vector(pointB, pointA).coords, Vector(pointB, aPoint).coords)
        if xros < 0:
            flag2 = True if minusSide == -1 else False
        elif xros == 0:
            if (((pointA > aPoint) & (aPoint > pointB)) | ((pointB > aPoint) & (aPoint > pointA))):
                return True, Vector(pointA, pointB)
            else:
                return False, False
        else:
            flag2 = False if minusSide == -1 else True

        if pointA > aPoint and aPoint > pointB:
            flag3 = True
        else:
            flag3 = False

        return (flag1 & flag2 & flag3, None)

    def contains(self, aPoint):
        if self.containsMinusOneNode() and self.containsMinusTwoNode():
            theid = self.__nodeIds[np.isin(self.__nodeIds, [-1,-2]) == False][0]
            return (True, None) if self.point(theid) > aPoint else (False, None)
        elif self.containsMinusOneNode():
            return self.__isInMinusNodeTriangle(-1, aPoint)
        elif self.containsMinusTwoNode():
            return self.__isInMinusNodeTriangle(-2, aPoint)
        else:
            points = list(self.__points.values())
            # Create essential vectors
            v0 = Vector(points[0], points[1])
            v1 = Vector(points[0], points[2])
            v2 = Vector(points[0], aPoint)

            ## Compute all the inner products
            dot00 = v0.innerProduct(v0)
            dot01 = v0.innerProduct(v1)
            dot02 = v0.innerProduct(v2)
            dot11 = v1.innerProduct(v1)
            dot12 = v1.innerProduct(v2)
            
            ## Compute the barycentric coordinates
            invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
            u = (dot11 * dot02 - dot01 * dot12) * invDenom
            v = (dot00 * dot12 - dot01 * dot02) * invDenom
            
            inTriangle = (u >= 0) & (v >= 0) & (u + v <= 1)
            
            if inTriangle:
                if u == 0:
                    return True, Vector(points[0], points[2])
                elif v == 0:
                    return True, Vector(points[0], points[1])
                elif u +v == 1: 
                    return True, Vector(points[1], points[2])
                else: 
                    return True, None
            else : 
                return inTriangle, False

if __name__ == "__main__":
    from vector import *
else:
    from .vector import *

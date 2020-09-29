from delauney.entities.circle import *

class Dtree:
    def __init__(self, triangle, parents=None, step=0):
        self.__triangle = triangle
        self.__parents = parents
        self.__children = []
        self.__step = step
        if self.__parents is None:
            self.__level = 0
        else:
            self.__level = max(list(map(lambda x : x.level, self.__parents))) + 1

    @property
    def triangle(self):
        return self.__triangle
    
    @property
    def level(self):
        return self.__level

    @property
    def children(self):
        return self.__children

    @property
    def parents(self):
        return self.__parents

    @property
    def step(self):
        return self.__step
    
    def checkChildrenForTriangle(self, triangle):
        if len(self.__children) == 0:
            return None

        for child in self.__children:
            if child.triangle == triangle:
                return child

        for child in self.__children:
            res = child.checkChildrenForTriangle(triangle)
            if not (res is None):
                return res

    def appendChild(self, child):
        self.__children.append(child)

    def getNodeWithTriangle(self, triangle):
        if self.__triangle == triangle:
            return node
        else:
            return self.checkChildrenForTriangle(triangle)

    def insertChild(self, triangle, otherParent=None, step = 0):
        parents = [self]
        if not (otherParent is None):
            parents.append(otherParent)
        child = Dtree(triangle, parents, step)
        self.appendChild(child)
        if not (otherParent is None):
            otherParent.appendChild(child)

    def getLastContainingTriangle(self, point, lastEdge = None):
        if len(self.__children) == 0:
            return self, lastEdge
        else:
            for i in self.__children:
                inTriangle, edge = i.triangle.contains(point)
                if inTriangle:
                    return i.getLastContainingTriangle(point, edge)

    def __str__(self):
        retStr = "\t"*self.__level + str(self.step)
        for i in self.__children:
            retStr = retStr + "\n" + str(i)
        return retStr


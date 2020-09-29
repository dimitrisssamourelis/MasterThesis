from entities.triangle import *

class Circle:
    def __init__(self, triangle):

        ids = triangle.pointIds

        x1 = triangle.point(ids[0]).x
        y1 = triangle.point(ids[0]).y
        x2 = triangle.point(ids[1]).x
        y2 = triangle.point(ids[1]).y
        x3 = triangle.point(ids[2]).x
        y3 = triangle.point(ids[2]).y

        A = x1*(y2-y3) - y1*(x2-x3) + x2*y3-x3*y2
        B = (x1**2 + y1**2)*(y3-y2) + (x2**2 + y2**2)*(y1-y3) + (x3**2 + y3**2)*(y2-y1)
        C = (x1**2 + y1**2)*(x2-x3) + (x2**2 + y2**2)*(x3-x1) + (x3**2 + y3**2)*(x1-x2)
        D = (x1**2 + y1**2)*(x3*y2-x2*y3) + (x2**2 + y2**2)*(x1*y3-x3*y1) + (x3**2 + y3**2)*(x2*y1-x1*y2)

        self._center = Point(-B/(2*A), -C/(2*A), np.inf)

        self._radius = np.sqrt((B**2 + C**2 - 4*A*D)/(4*A**2))

    @property
    def center(self):
        return self._center
    
    @property
    def radius(self):
        return self._radius

    def contains(self, point):
        v = Vector(self.center, point)
        d = np.sqrt(v.innerProduct(v))

        if d < self.radius:
            return True
        else:
            return False

    def __str__(self):
        return "Circle[Center = %s, radius = %.3f]"%(str(self.center), self.radius)


if __name__ == "__main__":
    A = Point(0, 0)
    B = Point(0, 1)
    C = Point(1, 0)

    triangle = Triangle(A, B, C)
    circle = Circle(triangle)

    print(triangle)
    print(circle)

    v1 = Vector(triangle.pointA, circle.center)
    v2 = Vector(triangle.pointB, circle.center)
    v3 = Vector(triangle.pointC, circle.center)

    d1 = np.sqrt(v1.innerProduct(v1))
    d2 = np.sqrt(v2.innerProduct(v2))
    d3 = np.sqrt(v3.innerProduct(v3))

    print("Circle Center distance from each triangle point")
    print("%.3f, %.3f, %.3f"%(d1, d2, d3))

    P1 = Point(0, 0.125)
    P2 = Point(2,2)

    print("%s in circle %s : %s"%(P1, circle, circle.contains(P1)))
    print("%s in circle %s : %s"%(P2, circle, circle.contains(P2)))

from delauney.entities.circle import *
from .Dtree import *
import json 
import logging

class DCEL:
    def __init__(self, points):
        
        logging.basicConfig(level=logging.INFO)

        self.__logger = logging.getLogger(__name__)
        #self.__logger.addHandler(fh)

        self.__step = 1
        self.__triangles = []
        self.__circles = []
        self.__dtree = None
        self.__points = points

    @property
    def dtree(self):
        return self.__dtree

    def __addNewTriangle(self, newTriangle, treenode, otherParent = None):
        if True: #sum([newTriangle == t for t in self.__triangles]) == 0:
            self.__triangles.append(newTriangle)
            treenode.insertChild(newTriangle, otherParent, step = self.__step)
            self.__infoLogger("Triangle %s inserted to triangulization."%(str(newTriangle)))

    def __infoLogger(self, string):
        self.__logger.info(string)

    def __get_initial_point(self):
        row_ids = np.where(self.__points[:,1] == np.max(self.__points, axis=0)[1])[0]
        sel_row = np.argmax(self.__points[row_ids, :], axis=0)[0]
        p0 = self.__points[row_ids[sel_row], :]
        self.__infoLogger("Lexicographically Distant Point : %s"%(str(p0)))
        return(p0, row_ids[sel_row])

    def __remove_triangle(self, triangle):
        index = self.__triangles.index(triangle)
        del self.__triangles[index]
        self.__infoLogger("Removed triangle %s from triangulization."%(str(triangle)))
        return

    def __shift_edge(self, pr, pk, edge, triangles):
        self.__infoLogger("Shifting Edge " + str(edge) + " to " + str(Vector(pr, pk)))
        for triangle in triangles:
            self.__remove_triangle(triangle)
            
        nodes = [self.__dtree.getNodeWithTriangle(triangle) for triangle in triangles]
        
        self.__addNewTriangle(Triangle(pr, pk, edge.pointA), nodes[0], nodes[1]) 
        self.__addNewTriangle(Triangle(pr, pk, edge.pointB), nodes[0], nodes[1])

        self.__step = self.__step + 1

           
    def __fix_edge(self, pr, edge):
        self.__infoLogger("Fix Edge(pr = " + str(pr) + ", edge = " + str(edge) + ")")
        if self.__dtree.triangle.hasEdge(edge.pointA, edge.pointB):
            return
        else:
            triangles_with_edge = [i for i in self.__triangles if i.hasEdge(edge.pointA, edge.pointB)]
            points = [triangle.getThirdNode(edge) for triangle in triangles_with_edge]
            pk = points[0] if points[0].id != pr.id else points[1]
                
            adjacentTrianglesExist = edge.formAdjacentTrianglesForCheck(pr, pk)
                
            if not adjacentTrianglesExist:
                return
                
            if ((pk.id < 0)  | (pr.id < 0) | (edge.pointA.id < 0) | (edge.pointB.id < 0)):
                if min(edge.pointA.id, edge.pointB.id) > min(pk.id, pr.id):
                    return
                else:
                    self.__shift_edge(pr, pk, edge, triangles_with_edge)
                    self.__fix_edge(pr, Vector(edge.pointA, pk))
                    self.__fix_edge(pr, Vector(pk, edge.pointB))
                    
                    return
            else:
                if Circle(Triangle(edge.pointA, edge.pointB, pk)).contains(pr):
                    self.__shift_edge(pr, pk, edge, triangles_with_edge)
                    self.__fix_edge(pr, Vector(edge.pointA, pk))
                    self.__fix_edge(pr, Vector(pk, edge.pointB))
                        
                    return
                else:
                    return


    def execute(self):
        p0, ind = self.__get_initial_point()

        p0 = Point(p0[0], p0[1], 0)
        
        pm1 = Point(-1, -1, -1)

        pm2 = Point(-2, -2, -2)

        firstTriangle = Triangle(p0, pm1, pm2)
        self.__dtree = Dtree(firstTriangle, None, step = self.__step)
        self.__step = self.__step + 1

        self.__triangles.append(firstTriangle)

        self.__infoLogger("Created initial structures")

        rest_points = np.delete(self.__points, ind, axis=0)
        
        rest_points = np.random.permutation(rest_points)
        for i in range(np.size(rest_points, 0)):
            p = Point(rest_points[0, 0], rest_points[0,1], i+1)

            self.__infoLogger("Starting point %s insertion"%(str(p)))

            treenode, edge = self.__dtree.getLastContainingTriangle(p)

            if edge is None:
                self.__infoLogger("%s located inside triangle %s"%(str(p), str(treenode.triangle)))

                self.__remove_triangle(treenode.triangle)
                points = list(map(lambda x : treenode.triangle.point(x), treenode.triangle.pointIds))
                self.__addNewTriangle(Triangle(points[0], points[1], p), treenode)
                self.__addNewTriangle(Triangle(points[0], points[2], p), treenode)
                self.__addNewTriangle(Triangle(points[1], points[2], p), treenode)
                
                self.__step = self.__step + 1

                self.__fix_edge(p, Vector(points[0], points[1]))
                self.__fix_edge(p, Vector(points[0], points[2]))
                self.__fix_edge(p, Vector(points[1], points[2]))

            else:
                self.__infoLogger("%s located on the edge %s of triangle %s"%(str(p), str(edge), str(treenode.triangle)))
                
                triangles_to_remove = [i for i in self.__triangles if i.hasEdge(edge.pointA, edge.pointB)]
                otherPoints = [triangle.getThirdNode(edge) for triangle in triangles_to_remove]
                for triangle in triangles_to_remove:
                    self.__remove_triangle(triangle)
                
                nodes = [self.__dtree.getNodeWithTriangle(triangle) for triangle in triangles_to_remove]
                otherParent = nodes[1] if nodes[0].triangle == treenode.triangle else nodes[0]

                for point in otherPoints:
                    self.__addNewTriangle(Triangle(point, edge.pointA, p), treenode, otherParent)
                    self.__addNewTriangle(Triangle(point, edge.pointB, p), treenode, otherParent)
                
                self.__step = self.__step + 1

                for point in otherPoints:
                    self.__fix_edge(p, Vector(edge.pointA, point))
                    self.__fix_edge(p, Vector(edge.pointB, point))

            rest_points = np.delete(rest_points, 0, axis=0)
            
        self.__triangles = [x for x in self.__triangles if ((x.point(-1) is None) and (x.point(-2) is None))]
        return self.__triangles
    
    def visualize_triangulization(self, imgname):
        import networkx as nx
        import matplotlib.pyplot as plt

        G = nx.Graph()
        for t in self.__triangles:
            ids = t.pointIds
            for anId in ids:
                if not G.has_node(anId):
                    p = t.point(anId)
                    G.add_node(anId, pos=(p.x, p.y))

            G.add_edge(ids[0], ids[1])
            G.add_edge(ids[0], ids[2])
            G.add_edge(ids[1], ids[2])
    
        fig, ax = plt.subplots(1, 1, figsize = (12, 12))
        posdict = {}
        labeldict = {}
        initdict = dict(G.nodes())
        for g in initdict.keys():
            posdict[g] = initdict[g]["pos"]
        
        nx.draw_networkx(G, pos = posdict, ax = ax, with_labels=True, node_size=1500, node_color="skyblue")
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        fig.savefig(imgname)
        return

    def __add_to_tree_graph(self, G, treenode):
        G.add_node(str(treenode.step) + ":\n" + str(treenode.triangle.pointIds))
        if not (treenode.parents is None):
            for parent in treenode.parents:
                G.add_edge(str(parent.step) + ":\n" + str(parent.triangle.pointIds), str(treenode.step) + ":\n" + str(treenode.triangle.pointIds))
        for child in treenode.children:
            self.__add_to_tree_graph(G, child)

    def __create_positions(self, G, treenode, posdict, x, y, width):
        posdict[str(treenode.triangle.pointIds)] = (x, y)


    def visualize_tree(self, imgname):
        import networkx as nx
        import matplotlib.pyplot as plt
        from networkx.drawing.nx_agraph import write_dot, graphviz_layout

        G = nx.DiGraph()
        i = 0
        self.__add_to_tree_graph(G, self.__dtree)
        
        fig, ax = plt.subplots(1, 1, figsize = (12, 12))

        pos = graphviz_layout(G, prog='dot')
        
        nx.draw(G, pos = pos, ax = ax, with_labels=True, arrows=True, node_size=3000, node_color="skyblue")
        fig.savefig(imgname + '.jpg')

    def __group_triangles_by_step(self, treenode, aDict = {}):
        if treenode.step in aDict:
            aDict[treenode.step].append(treenode)
        else:
            aDict[treenode.step] = [treenode]
        for child in treenode.children:
            aDict = self.__group_triangles_by_step(child, aDict)
        return aDict

        

    def visualize_algorithm(self, foldername):
        import networkx as nx
        import os, shutil
        import matplotlib.pyplot as plt 

        if not os.path.exists("./" + foldername):
            os.makedirs("./" + foldername)
        else:
            for filename in os.listdir(foldername):
                file_path = os.path.join(foldername, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))
                        
        aDict = self.__group_triangles_by_step(self.__dtree, {})
        G = nx.Graph()
        posdict = {}
        xmax = max([max(list(map(lambda pid : x.point(pid).x, x.pointIds))) for x in self.__triangles])
        ymax = max([max(list(map(lambda pid : x.point(pid).y, x.pointIds))) for x in self.__triangles])
        xmin = min([min(list(map(lambda pid : x.point(pid).x, x.pointIds))) for x in self.__triangles])
        ymin = min([min(list(map(lambda pid : x.point(pid).y, x.pointIds))) for x in self.__triangles])

        for i in range(1, self.__step):
            deleteParents = True
            for treenode in aDict[i]:
                if not (treenode.parents is None) and deleteParents:

                    for pnode in treenode.parents:
                        pt = pnode.triangle
                        ids = pt.pointIds
                        rpoints = list(map(lambda x : pt.point(x), ids))
                        for p_ind in range(len(rpoints)):
                            q_ind = p_ind + 1 if p_ind < len(rpoints) - 1 else 0
                            p = rpoints[p_ind]
                            q = rpoints[q_ind]
                            if ((p.id >= 0) & (q.id >= 0)):
                                if G.has_edge(p.id, q.id):
                                    G.remove_edge(p.id, q.id)
                                if G.has_edge(q.id, p.id):
                                    G.remove_edge(q.id, p.id)
                
                triangle = treenode.triangle
                tids = list(triangle.pointIds)
                points = list(map(lambda x : triangle.point(x), tids))
               
                for p in points:
                    if p.id >= 0:
                        G.add_node(p.id)
                        posdict[p.id] = (p.x, p.y)
                        
                for p_ind in range(len(points)):
                    q_ind = p_ind + 1 if p_ind < 2 else 0
                    p = points[p_ind]
                    q = points[q_ind]
                    if ((p.id >= 0) & (q.id >= 0)):
                        if not G.has_edge(p.id, q.id) and not G.has_edge(q.id, p.id):
                            G.add_edge(p.id, q.id)
                
                deleteParents = False
                
            fig, ax = plt.subplots(1, 1, figsize = (12, 12))
            nx.draw_networkx(G, pos = posdict, ax = ax, with_labels=True, node_size=1500, node_color="skyblue")
            ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            ax.set_xlim(-0.1*xmax, xmax + max(xmin, 0.1*xmax))
            ax.set_ylim(-0.1*xmax, ymax + max(ymin, 0.1*ymax))
            fig.savefig("./" + foldername + "/" + str(i) + ".jpg")
            plt.close(fig)


    def __str__(self):
        return json.dumps(self._triangulization)


if __name__ == "__main__":
    dcel = DCEL()

    self.__infoLogger(dcel)

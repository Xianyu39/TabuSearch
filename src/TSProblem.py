"""
encoding = utf-8

Traversal Purchaser Problem, 
is about how to find the shortest way that reaches all the nodes and finally goes back,
which can be solved by tabu-search.

Here is an example.
"""
# from _typeshed import OpenBinaryMode
# from os import name
import numpy as np


class Error(Exception):
    """Cities and pathes matrix are not conpatible, or matrix are not square matrix."""
    def __init__(self, args: object) -> None:
        self.args=args


class MapError(Error):
    def __init__(self, message:str) -> None:
        self.message = message


class Map:
    """Acturally, Map is a directed graph, which uses tuple as verteces, ndarray as edges."""
    
    def __init__(self, cities:tuple, pathes:np.ndarray) -> None:
        if pathes.shape[0] != pathes.shape[1]:
            raise MapError("Pathes matrix is not a square matrix.")
        elif len(cities) != pathes.shape[0]:
            raise MapError("Cities and Pathes are not compatible.")

        self.cities=cities
        self.pathes=pathes

    def vertex(self)->tuple:
        return self.cities

    def edges(self)->np.ndarray:
        return self.pathes

    def __str__(self) -> str:
        return "Cities:\n"+str(self.cities)+"\nPathes:\n"+str(self.pathes)


class Tabu_Search:
    """Tabu search class, includes visualization."""
    def __init__(self, map:np.ndarray) -> None:
        pass


# style string
vertex="\t{name}[shape=circle, label={label}, size=0.1, fillcolor=black, style=filled, fontcolor=white]\n"
arrow="\t{v1}->{v2}[label=\"{w}\"]\n"
def visualize_Map(map:Map):
    # Open script file
    with open("./rsrc/Map.dot","w") as script:
        script.write("digraph {\n")
        script.write("\tlabel=\"Map\"\n")

        # Generate verteces
        verteces=list()
        for v in map.vertex():
            verteces.append(str(v))
            script.write(vertex.format(name=str(v), label=str(v)))

        # Connect
        for i in range(map.edges().shape[0]):
            for j in range(map.edges().shape[1]):
                weight = map.edges()[i,j]
                if weight!=0:
                    script.write(arrow.format(v1=verteces[i], v2=verteces[j], w=weight))

        script.write("}")

    print("Visualized successfully.")


def main():
    mt=np.array([[0,1,0.5,1],[1,0,1,1,],[1.5,5,0,1],[1,1,1,0]])
    
    map = Map(('A','B','C','D'),mt)
    visualize_Map(map)
    print(mt)

main()
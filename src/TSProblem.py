"""
encoding = utf-8

Traversal Purchaser Problem, 
is about how to find the shortest way that reaches all the nodes and finally goes back,
which can be solved by tabu-search.

Here is an example.
"""

import numpy as np

class Error(Exception):
    """Cities and pathes matrix are not conpatible, or matrix are not square matrix."""
    def __init__(self, args: object) -> None:
        self.args=args


class MapError(Error):
    def __init__(self, message:str) -> None:
        self.message = message


INFINITY = 0xFFFFFFFFF

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
    def __init__(self, map:Map) -> None:
        self.TabuList = list()
        self.TabuLength = int()
        self.map = map
        self.beginCity=self.map.cities[0]


    def neighbours(self, ans:tuple)->tuple:
        ans_collection=list()
        ex_collection=list()
        for i in range(len(self.map.cities)):
            for j in range(i+1, len(self.map.cities)):
                if self.map.cities[i]!=self.beginCity and self.map.cities[j]!=self.beginCity:
                    ex_collection.append((self.map.cities[i], self.map.cities[j]))

        neighbour_collection = list()

        # Watch
        # print(ex_collection)
        for ex in ex_collection:
            possible_ans=list(ans)
            # Exchange 2 elements in ex to generate new answers.
            x = possible_ans.index(ex[0])
            y = possible_ans.index(ex[1])
            possible_ans[x]=ex[1]
            possible_ans[y]=ex[0]

            if possible_ans not in self.TabuList:
                neighbour_collection.append(tuple(possible_ans))

        return tuple(neighbour_collection)


    def evaluate(self, ans:tuple)->float:
        length = float(0)
        for ix in range(len(ans)):
            v1 = self.map.cities.index(ans[ix-1])
            v2 = self.map.cities.index(ans[ix])
            length+=self.map.edges()[v1,v2]

        return length
            


# style template
vertex="\t{name}[shape=\"circle\", label=\"{label}\", size=0.1, fillcolor=\"black\", style=\"filled\", fontcolor=\"white\"]\n"
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
                if weight!=INFINITY:
                    script.write(arrow.format(v1=verteces[i], v2=verteces[j], w=weight))

        script.write("}")

    print("Visualized successfully.")


def main():
    mt=np.array([[INFINITY, 1,1.5,1],[1,INFINITY,1,1,],[1.5,5,INFINITY,1],[1,1,1,INFINITY]])
    map = Map(('A','B','C','D'),mt)

    TS=Tabu_Search(map)
    TS.beginCity='A'
    print("Original answer:\n", ('A','B','C','D'), ": ", TS.evaluate(('A','B','C','D')))
    print("Adjacent answer: ")
    for ans in TS.neighbours(('A','B','C','D')):
        print(ans, ": ", TS.evaluate(ans))

    visualize_Map(map)

main()
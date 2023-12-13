import matplotlib.pyplot as plt
import networkx as nx
from collections import deque


# Класс для представления graphического объекта
class Graph:

    # 1ТП4Т Конструктор
    def __init__(self, edges=None, n=0):
        # Общее количество узлов в Graph
        self.n = n

        # Список списков для представления списка смежности
        self.adjList = [[] for _ in range(n)]

        # добавляет ребра в неориентированный graph
        for (src, dest) in edges:
            # добавляет ребро от источника к месту назначения
            self.adjList[src].append(dest)

            # добавляет ребро от пункта назначения к источнику
            self.adjList[dest].append(src)


# Выполнить BFS на Graph, начиная с вершины `v`
def isBipartite(graph):
    # запускается с любого узла, так как graph связный и ненаправленный
    v = 0

    # для отслеживания обнаружена вершина или нет
    discovered = [False] * graph.n

    # хранит уровень каждой вершины в BFS
    level = [None] * graph.n

    # пометить исходную вершину как обнаруженную и установить ее уровень на 0
    discovered[v] = True
    level[v] = 0

    # создает queue для выполнения BFS и ставит в queue исходную вершину
    q = deque()
    q.append(v)

    # Цикл # до тех пор, пока queue не станет пустой
    while q:

        # удалить передний узел из очереди и распечатать его
        v = q.popleft()

        # делаем для каждого ребра (v, u)
        for u in graph.adjList[v]:
            # , если вершина `u` исследуется впервые
            if not discovered[u]:
                # пометить как обнаруженный
                discovered[u] = True

                # устанавливает уровень на один больше, чем уровень родительского узла
                level[u] = level[v] + 1

                # Вершина постановки в queue
                q.append(u)

            # , если вершина уже обнаружена и
            # вершины `u` и `v` совпадают, то
            # Graph # содержит нечетный цикл и не является двудольным.
            elif level[v] == level[u]:
                return False

    return True


if __name__ == '__main__':

    # Список ребер Graph
    # Обратите внимание, что если мы добавим ребро (1, 3), graph станет недвудольным.
    edges = [(0, 1), (1, 2), (1, 7), (2, 3), (3, 5), (4, 6), (4, 8), (7, 8)]

    # общее количество узлов в Graph (от 0 до 8)
    n = 9

    # строит graph по заданным ребрам
    graph = Graph(edges, n)

    if isBipartite(graph):
        print('Graph is bipartite')
    else:
        print('Graph is not bipartite')

        # Создаем графический объект из вашего объекта Graph
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    G.add_edges_from(edges)

    # Раскраска двудольного графа
    colors = ['red' if level[node] % 2 == 0 else 'blue' for node in G.nodes()]

    # Рисуем граф
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color=colors, font_color='black',
            font_size=10, edge_color='gray', linewidths=1, arrowsize=15)

    # Отображаем граф
    plt.show()
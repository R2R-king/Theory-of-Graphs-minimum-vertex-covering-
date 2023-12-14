import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from collections import deque
import random as rn
import time


# Класс для представления graphического объекта
class Graph:
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


def find_maximum_matching(graph):
    max_matching = nx.max_weight_matching(graph, maxcardinality=True)
    return max_matching


def generate_bipartite_graph():
    G = nx.Graph()
    # Количество вершин слева
    num_left_nodes = rn.randint(10, 50)
    # количество вершин справа
    num_right_nodes = rn.randint(10, 50)
    # вероятность связи вершин графа
    probability = rn.uniform(0.1, 0.8)
    # Добавляем левые и правые узлы
    left_nodes = range(num_left_nodes)
    right_nodes = range(num_left_nodes, num_left_nodes + num_right_nodes)
    G.add_nodes_from(left_nodes, bipartite=0)
    G.add_nodes_from(right_nodes, bipartite=1)

    # Добавляем рёбра с заданной вероятностью
    for left_node in left_nodes:
        for right_node in right_nodes:
            if rn.random() < probability:
                G.add_edge(left_node, right_node)

    return G

def generate_bipartite_connected_graph():
    while True:
        G = generate_bipartite_graph()
        if nx.is_connected(G):  # Проверка на связность
            return G

def find_minimum_vertex_cover(graph):
    min_vertex_cover = set()
    for u, v in graph.edges:
        if u not in min_vertex_cover and v not in min_vertex_cover:
            min_vertex_cover.add(u)
            min_vertex_cover.add(v)

    return min_vertex_cover

def hopcroft_karp_max_matching(graph):
    left, right = nx.bipartite.sets(graph)
    matching = nx.bipartite.hopcroft_karp_matching(graph, left)
    max_matching = [(key, matching[key]) for key in matching]
    return max_matching


graph_number = 50
graphs = [generate_bipartite_connected_graph() for i in range(graph_number)]

# Сохранение результатов
matching_sizes = []
vertex_cover_sizes = []
initial_vertex_number = [G.number_of_nodes() for G in graphs]  # Добавим эту строку

for graph in graphs:
    max_matching = hopcroft_karp_max_matching(graph)
    min_vertex_cover = find_minimum_vertex_cover(graph)

    matching_sizes.append(len(max_matching))
    vertex_cover_sizes.append(len(min_vertex_cover))

# Построение графика
plt.figure(figsize=(10, 6))
plt.scatter(initial_vertex_number, matching_sizes, label='Наибольшее паросочетание', marker='o')
plt.scatter(initial_vertex_number, vertex_cover_sizes, label='Минимальное вершинное покрытие', marker='x')
plt.xlabel('Количество вершин в графе')
plt.ylabel('Размеры')
plt.title('Сравнение размеров паросочетания и вершинного покрытия')
plt.legend()
plt.grid(True)
plt.show()

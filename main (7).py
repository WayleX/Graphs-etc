"""
'Graphs etc' computer project.
"""

from copy import deepcopy
from itertools import permutations
from collections import defaultdict
from util_functions import is_strongly_connected, has_euler_cycle, dfs

def read_graph(filename: str) -> dict[int, list[int]]:
    """
    Function reads graph from .csv file.
    File have to contain edges on each line in format [source, destination].
    """
    graph = defaultdict(lambda: [])

    try:
        with open(filename, encoding="utf-8") as src_file:
            for line in src_file.readlines():
                pair = tuple(map(int, line.strip().split(",")))

                graph[pair[0]].append(pair[1])
                if pair[1] not in graph:
                    graph[pair[1]] = []
    except FileNotFoundError:
        print(f"'{filename}' file is not found.")
        return {}

    return dict(graph)

def hamiltonian_cycle(graph: dict[int, list[int]]) -> list[int]:
    """
    Function takes graph and returs Hamiltonian cycle
    of the graph if exists.
    >>> hamiltonian_cycle({1: [2], 2: [3], 3: [4], 4: []})
    >>> hamiltonian_cycle({1: [2], 2: [3], 3: [1, 4], 4: [1]})
    [1, 2, 3, 4, 1]
    >>> hamiltonian_cycle({1: [2], 2: [3], 3: [4], 4: [1]})
    [1, 2, 3, 4, 1]
    >>> hamiltonian_cycle({1: [2], 2: [1]})
    [1, 2, 1]
    >>> hamiltonian_cycle({0: [1, 4, 3], 1: [4], 2: [1, 0], 3: [2], 4: [3]})
    [0, 1, 4, 3, 2, 0]
    >>> hamiltonian_cycle({})
    []
    >>> hamiltonian_cycle({0: [1, 4, 3], 1: [4], 2: [1, 0], 3: [2], 4: [3], 8: [5], 5: [8]})
    >>> hamiltonian_cycle({0: [1], 1: [2], 2: [5, 3], 3: [4, 5], 4: [3, 0], 5: [2, 3, 4]})
    [0, 1, 2, 3, 5, 4, 0]
    >>> hamiltonian_cycle({0: [1], 1: [2], 2: [5, 3], 3: [4, 5], 4: [3, 0], 5: [2, 3]})
    [0, 1, 2, 5, 3, 4, 0]
    """
    if not graph:
        return []

    vertices = list(graph.keys())
    cycle = [vertices[0]]
    ban = set()

    while len(cycle) != (len(vertices) + 1) and cycle:
        vertex = cycle[-1]
        adj = {ver for ver in graph[vertex] if not(ver in cycle[1:] or tuple(cycle + [ver]) in ban)}

        if len(cycle) < len(graph.keys()):
            adj = {ver for ver in adj if ver != cycle[0]}

        if not adj:
            vertex = cycle.pop()
            if cycle:
                ban.add(tuple(cycle + [vertex]))
                continue
            return None

        cycle.append(next(iter(adj)))

    return cycle

def euler_cycle(graph: dict[int, list[int]]) -> list[int]:
    """
    Function takes graph and returns Euler's cycle if exists.
    If not returns None.
    >>> euler_cycle({0: [1], 1: [2], 2: [3], 3: [0]})
    [0, 1, 2, 3, 0]
    >>> euler_cycle({0: [1], 1: [2], 2: [3], 3: []})

    >>> euler_cycle({0: [1, 6], 1: [2], 2: [0, 3], 3: [4], 4: [2, 5], 5: [0], 6: [4]})
    [0, 6, 4, 5, 0, 1, 2, 3, 4, 2, 0]
    """
    if not is_strongly_connected(graph):
        return None

    if not has_euler_cycle(graph):
        return None

    graph = deepcopy(graph)
    circuit = []

    current_vertex = list(graph.keys())[0]
    current_path = [current_vertex]

    while current_path:
        if graph[current_vertex]:
            current_vertex = graph[current_vertex].pop()
            current_path.append(current_vertex)
        else:
            circuit.append(current_path.pop())

    circuit.reverse()
    return circuit

def is_bipartite(graph: dict[int, list[int]]) -> bool:
    """
    Function checks if graph is bipartite.
    >>> is_bipartite({1: [2, 3], 4: [2, 3], 2: [], 3: []})
    True
    >>> is_bipartite({1: [2], 2: [3], 3:[4], 4: [5], 5: [6], 6: [1]})
    True
    >>> is_bipartite({0: [3], 1: [2, 3], 2: [1, 3, 5, 6, 7],\
    3: [0, 1, 2], 4: [5, 6], 5: [2, 4, 6], 6: [2, 4, 5], 7: [2]})
    False
    >>> is_bipartite({1: [2], 2: [3], 3:[1], 4: [5], 5: [6], 6: [4]})
    False
    """
    graph = deepcopy(graph)
    for key, value in graph.items():
        for adj in value:
            graph[adj].append(key)

    if set(graph.keys()) != set(dfs(graph, next(iter(graph.keys())))):
        return False

    initial_vertex = next(iter(graph.keys()))
    queue = [initial_vertex]
    coloring = {0: {initial_vertex}, 1: set()}

    while queue:
        vertex = queue.pop(0)
        current_color = vertex in coloring[1]

        for adj_vertex in graph[vertex]:
            if adj_vertex in coloring[current_color]:
                return False
            if adj_vertex in coloring[not current_color]:
                continue

            queue.append(adj_vertex)
            coloring[not current_color].add(adj_vertex)

    return True

def is_isomorphic(graph1: dict[int, list[int]], graph2: dict[int, list[int]]) -> bool:
    """
    Function takes two graphs and determines
    are they isomorphic of not.
    >>> is_isomorphic({1: [3, 5], 2: [7], 5: [2, 3], 5: [], 7: [], 3: []},\
    {5: [], 7: [], 2: [3, 5], 1: [7], 3: [1, 5]})
    False
    >>> is_isomorphic({'a': ['c', 'b'], 'b': ['d'], 'c': [], 'd': []\
    }, {0: [1, 2], 1: [3], 2: [], 3: []})
    True
    >>> is_isomorphic({'a': ['b', 'd'], 'd': ['b'], 'b': ['c'], 'c': ['a', 'd']},\
    {'a': ['b', 'd'], 'd': ['b', 'c'], 'b': ['c'], 'c': ['a']})
    True
    >>> is_isomorphic({'a': ['b'], 'd': [], 'b': ['d'], 'c': ['a', 'b']},\
    {'a': ['c', 'd'], 'd': ['b'], 'b': [], 'c': ['b']})
    False
    """
    if len(graph1.keys()) != len(graph2.keys()):
        return False

    original = {(frm, to_ver) for frm, to in graph1.items() for to_ver in to}

    for permitation in permutations(graph1.keys()):
        bjection = {key: value for key, value in zip(graph2.keys(), permitation)}
        mutated = {(bjection[frm], bjection[to_ver]) for frm, to in graph2.items() for to_ver in to}

        if mutated == original:
            return True

    return False

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

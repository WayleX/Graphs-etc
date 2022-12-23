"""
Module contains functions required for other algorithms.
"""

from collections import defaultdict

def dfs(graph: dict[int, list[int]], start_in: int = 0, terminate_in: int = -1) -> list:
    """
    Function computed Depth First Search on 'graph'.
    >>> dfs({0: [2, 5, 7], 1: [2, 6, 7], 2: [0, 1, 4, 5, 6, 7],\
    3: [6, 7], 4: [2, 5, 7], 5: [0, 2, 4, 7],\
    6: [1, 2, 3, 7], 7: [0, 1, 2, 3, 4, 5, 6]})
    [0, 2, 1, 6, 3, 7, 4, 5]
    """
    if start_in not in graph.keys():
        return None

    stack = [start_in]
    result = [start_in]

    while stack:
        for adj_vertex in graph[stack[-1]]:
            if adj_vertex not in result:
                result.append(adj_vertex)
                stack.append(adj_vertex)

                if terminate_in == adj_vertex:
                    return result

                break
        else:
            stack.pop()

    return result

def get_transposed(graph: dict[int, list[int]]):
    """
    Function returns transpised graph.
    >>> get_transposed({0: [1], 1: [2], 2: [3], 3: [0], 4: []})
    {0: [3], 1: [0], 2: [1], 3: [2], 4: []}
    """
    result = defaultdict(list)

    for key, value in graph.items():
        if not result.get(key, []):
            result[key] = []
        for ver in value:
            result[ver].append(key)

    return dict(result)

def is_strongly_connected(graph: dict[int, list[int]]):
    """
    Function checks is graph strongly connected or not.
    WE DO NOT CONSIDER ISOLATED VERTICES.
    >>> is_strongly_connected({0: [1], 1: [2], 2: [3], 3: [0], 4: []})
    True
    >>> is_strongly_connected({0: [1], 1: [2], 2: [3], 3: [0], 4: []})
    True
    >>> is_strongly_connected({0: [1], 1: [2], 2: [0], 10: [11], 11: [12], 12: [10]})
    False
    """
    transposed_graph = get_transposed(graph)
    isolated_vertices = {key for key in graph if not graph[key] and not transposed_graph[key]}
    vertices = set(graph.keys()) - isolated_vertices

    direct_dfs = dfs(graph, next(iter(vertices)))
    reverse_dfs = dfs(transposed_graph, next(iter(vertices)))

    return set(direct_dfs) == vertices and vertices == set(reverse_dfs)

def has_euler_cycle(graph: dict[int, list[int]]) -> bool:
    """
    Function checks has graph Euler's cycle or not.
    >>> has_euler_cycle({0: [1], 1: [2], 2: [3], 3: [0]})
    True
    >>> has_euler_cycle({0: [1], 1: [2, 3], 2: [3], 3: [0]})
    False
    """
    vertices_degree = defaultdict(lambda: 0)

    for vertex, vertices_list in graph.items():
        vertices_degree[vertex] += len(vertices_list)
        for adj_vertex in vertices_list:
            vertices_degree[adj_vertex] -= 1

    return not any(vertices_degree.values())

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
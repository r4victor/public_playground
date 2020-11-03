import copy
import random

import pytest

import near_tree


# fixtures

@pytest.fixture()
def smallest_cycle():
    graph = [
        [(1, 1), (2, 2)],
        [(0, 1), (2, 3)],
        [(0, 2), (1, 3)],
    ]
    return graph


# test find_cycle

def is_cycle(graph, cycle):
    def is_edge_in_graph(graph, edge, cost):
        v, w = edge
        for u, c in graph[v]:
            if u == w:
                if c != cost:
                    raise ValueError(f'Edge in cycle {cycle} has wrong cost.')
                return True
        return False

    def can_edge_follow_edge(graph, edge1, edge2):
        if edge1[0] == edge2[0] and edge1[1] != edge2[1]:
            return True
        if edge1[0] == edge2[1] and edge1[1] != edge2[0]:
            return True
        if edge1[1] == edge2[0] and edge1[0] != edge2[1]:
            return True
        if edge1[1] == edge2[1] and edge1[0] != edge2[0]:
            return True
        return False
            

    if len(cycle) < 3:
        raise ValueError(f'Not a cycle: {cycle}')

    prev_edge, _ = cycle[-1]
    for edge, cost in cycle:
        if not is_edge_in_graph(graph, edge, cost):
            raise ValueError(f'Edge {edge} from cycle {cycle} is not in a graph.')
        if not can_edge_follow_edge(graph, edge, prev_edge):
            raise ValueError(f'Edge {edge} cannot follow edge {prev_edge}.')
        prev_edge = edge


def test_find_cycle_smallest_cycle(smallest_cycle):
    graph = smallest_cycle
    cycle = near_tree.find_cycle(graph)
    is_cycle(graph, cycle)


def test_find_cycle_no_cycle():
    graph = [
        [(1, 1), (2, 2)],
        [(0, 1),],
        [(0, 2),],
    ]
    cycle = near_tree.find_cycle(graph)
    assert cycle is None
    

# test break_cycle

def test_break_cycle_smallest_cycle(smallest_cycle):
    graph = smallest_cycle
    cycle = [((0, 1), 1), ((1, 2), 3), ((0, 2), 2)]
    edge_to_remove = near_tree.break_cycle(graph, cycle)
    expected_edge_to_remove = (1, 2)
    assert edge_to_remove == expected_edge_to_remove


# test mst

def get_graph_edges(graph):
    edges = []
    for v in range(len(graph)):
        for w, c in graph[v]:
            if v < w:
                edges.append(((v, w), c))
    return frozenset(edges)


def test_mst_smallest_cycle(smallest_cycle):
    graph = smallest_cycle
    expected_graph = [
        [(1, 1), (2, 2)],
        [(0, 1)],
        [(0, 2)],
    ]
    near_tree.near_tree_mst(graph)
    assert get_graph_edges(graph) == get_graph_edges(expected_graph)


def test_mst_two_cycles():
    graph = [
        [(1, 4)],
        [(2, 2), (3, 1), (4, 3)],
        [(1, 2), (3, 3), (4, 1)],
        [(1, 1), (2, 3)],
        [(1, 3), (2, 1)]
    ]
    expected_graph = [
        [(1, 4)],
        [(2, 2), (3, 1)],
        [(1, 2), (4, 1)],
        [(1, 1)],
        [(2, 1)]
    ]
    near_tree.near_tree_mst(graph)
    assert get_graph_edges(graph) == get_graph_edges(expected_graph)


MAX_NUM_OF_REDUNDANT_EDGES = 9


def generate_near_trees(n):
    in_tree = [0]
    not_in_tree = list(range(1, n))
    tree = [[] for _ in range(n)]
    # build some tree
    while len(not_in_tree) > 0:
        u = random.choice(in_tree)
        v = random.choice(not_in_tree)
        in_tree.append(v)
        not_in_tree.remove(v)
        cost = random.randint(1, 20)
        tree[u].append((v, cost))
        tree[v].append((u, cost))

    for r in range(MAX_NUM_OF_REDUNDANT_EDGES+1):
        graph = copy.deepcopy(tree)
        for _ in range(r):
            u = random.randint(0, n-1)
            adjacent = set(w for w, _ in graph[u])
            if len(adjacent) == n - 1:
                    continue
            while True:
                v = random.randint(0, n-1)
                if v != u and v not in adjacent:
                    break
            cost = random.randint(21, 40)
            graph[u].append((v, cost))
            graph[v].append((u, cost))
        
        yield tree, graph
            

@pytest.mark.long
def test_random_mst():
    i = 0
    seed = 123
    random.seed(seed)
    for n in range(1, 10000):
        for tree, graph in generate_near_trees(n):
            i += 1
            print(i)
            near_tree.near_tree_mst(graph)
            assert get_graph_edges(graph) == get_graph_edges(tree)

        







        


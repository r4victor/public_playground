

def near_tree_mst(graph):
    """
    Removes edges form the connected graph
    until the graph becomes a Minimum Spanning Tree (MST).

        :param graph: an adjacency list, each element is a tuple (node, cost)
        :return: returns `None`, modifies the graph

    At each iteration it first finds a cycle.
    Then breaks the cycle by removing the heaviest edge.
    When no more cycles exist, the graps is an MST.

    The algorithm is correct because if an edge is the heaviest edge of some cycle,
    it cannot be in an MST.
    Otherwise we could built an ST with the smaller weight by replacing this edge
    with another edge from the cycle.
    More thorough proof can be conducted using the induction.

    r (number of edges to remove) = m - (n - 1) = m - n + 1
    If the graph is a near tree (m <= n + 8), r <= 9.
    The maximum number of iteration is r.
    In this particular implementation:
        - cost of find_cycle <= 2m
        - cost of break_cycle <= 3m
    Cost of near_tree_mst <= r*5m <= 45m.
    Thus, near_tree_mst is O(m) = O(n).

    Another possible implementation is not to modify the graph
    but to keep track of removed edges and then built the MST in the end.
    It's more efficient and pure, but requires more bookkeeping.
    Its cost <= r*3m + 9m <= 36m.
    """
    while True:
        cycle = find_cycle(graph)
        if cycle is None:
            return

        break_cycle(graph, cycle)


def find_cycle(graph):
    """
    Finds cycle in a graph.

        :param graph: an adjacency list, each element is a tuple (node, cost)
        :return: cycle – a list of tuples (edge, cost), where edge is a tuple (u, v)

    The algorithm runs the DFS. It detects the cycle when it sees an already visited node.
    `previous_node[v]` stores the node from which the DFS went to the node `v`.
    This list is used to restore the cycle.
    """
    def restore_cycle(from_node):
        v = from_node
        cycle = []
        while True:
            w = previous_node[v]
            current_edge = tuple(sorted([v, w]))
            current_edge_cost = previous_edge_cost[v]
            cycle.append((current_edge, current_edge_cost))
            v = w
            if v == from_node:
                return cycle

    n = len(graph)
    stack = [0]
    visited = [False] * n
    previous_node = [None] * n
    previous_edge_cost = [None] * n

    while stack:
        v = stack.pop()
        
        visited[v] = True
        for w, edge_cost in graph[v]:
            if w == previous_node[v]:
                continue

            stack.append(w)
            previous_node[w] = v
            previous_edge_cost[w] = edge_cost

            if visited[w]:
                return restore_cycle(w)

    return None


def break_cycle(graph, cycle):
    """
    Finds the heaviest edge in `cycle` and removes it from `graph`.

        :param graph: an adjacency list, each element is a tuple (node, cost)
        :param cycle: a list of tuples (edge, cost), where edge is a tuple (u, v)
        :return: returns removed edge, modifies the graph

    """
    max_edge_cost = cycle[0][1]
    edge_to_remove = cycle[0][0]

    for edge, edge_cost in cycle[1:]:
        if edge_cost > max_edge_cost:
            max_edge_cost = edge_cost
            edge_to_remove = edge

    v, w = edge_to_remove
    graph[v] = [(u, c) for u, c in graph[v] if u != w]
    graph[w] = [(u, c) for u, c in graph[w] if u != v]

    return edge_to_remove


if __name__ == '__main__':
    pass
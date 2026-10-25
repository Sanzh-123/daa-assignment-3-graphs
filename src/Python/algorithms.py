import sys
import heapq
from collections import defaultdict

sys.setrecursionlimit(300000)

def dsu(request):
    n = request.get("n", 0)
    operations = request.get("operations", [])
    if n == 0:
        return {"states": []}
    
    parent = list(range(n))
    size = [1] * n
    components = n
    largest = 1
    states = []
    
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(u, v):
        nonlocal components, largest
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if size[root_u] < size[root_v]:
                root_u, root_v = root_v, root_u
            parent[root_v] = root_u
            size[root_u] += size[root_v]
            components -= 1
            if size[root_u] > largest:
                largest = size[root_u]

    for op in operations:
        u, v = op[0], op[1]
        if 0 <= u < n and 0 <= v < n:
            union(u, v)
        states.append([components, largest])
        
    return {"states": states}


def kruskal(request):
    n = request.get("n", 0)
    edges = request.get("edges", [])
    if n == 0:
        return {"cost": 0, "edge_ids": [], "components": 0}
    
    parent = list(range(n))
    size = [1] * n
    components = n

    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i

    def union(u, v):
        nonlocal components
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            if size[root_u] < size[root_v]:
                root_u, root_v = root_v, root_u
            parent[root_v] = root_u
            size[root_u] += size[root_v]
            components -= 1
            return True
        return False

    indexed_edges = []
    for idx, edge in enumerate(edges):
        u, v, w = edge[0], edge[1], edge[2]
        indexed_edges.append((w, idx, u, v))
        
    indexed_edges.sort(key=lambda x: x[0])

    cost = 0
    edge_ids = []

    for w, idx, u, v in indexed_edges:
        if u == v:
            continue
        if 0 <= u < n and 0 <= v < n:
            if union(u, v):
                cost += w
                edge_ids.append(idx)

    return {"cost": cost, "edge_ids": edge_ids, "components": components}


def prim(request):
    n = request.get("n", 0)
    edges = request.get("edges", [])
    if n == 0:
        return {"cost": 0, "edge_ids": [], "components": 0}
    
    adj = defaultdict(list)
    for idx, edge in enumerate(edges):
        u, v, w = edge[0], edge[1], edge[2]
        if 0 <= u < n and 0 <= v < n and u != v:
            adj[u].append((w, v, idx))
            adj[v].append((w, u, idx))

    visited = [False] * n
    cost = 0
    edge_ids = []
    components = 0

    for start in range(n):
        if not visited[start]:
            components += 1
            visited[start] = True
            pq = []
            for w, neighbor, idx in adj[start]:
                heapq.heappush(pq, (w, neighbor, idx))
            
            while pq:
                w, u, idx = heapq.heappop(pq)
                if visited[u]:
                    continue
                visited[u] = True
                cost += w
                edge_ids.append(idx)
                for nw, neighbor, nidx in adj[u]:
                    if not visited[neighbor]:
                        heapq.heappush(pq, (nw, neighbor, nidx))

    return {"cost": cost, "edge_ids": edge_ids, "components": components}


def scc(request):
    n = request.get("n", 0)
    edges = request.get("edges", [])
    if n == 0:
        return {"component": [], "condensation": []}
    
    adj = [[] for _ in range(n)]
    rev_adj = [[] for _ in range(n)]
    for edge in edges:
        u, v = edge[0], edge[1]
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            rev_adj[v].append(u)

    visited = [False] * n
    order = []

    def dfs1(u):
        visited[u] = True
        for v in adj[u]:
            if not visited[v]:
                dfs1(v)
        order.append(u)

    for i in range(n):
        if not visited[i]:
            dfs1(i)

    visited = [False] * n
    component = [-1] * n

    def dfs2(u, root):
        visited[u] = True
        component[u] = root
        for v in rev_adj[u]:
            if not visited[v]:
                dfs2(v, root)

    for u in reversed(order):
        if not visited[u]:
            dfs2(u, u)

    cond_edges = set()
    for u in range(n):
        u_label = component[u]
        for v in adj[u]:
            v_label = component[v]
            if u_label != v_label:
                cond_edges.add((u_label, v_label))

    condensation = [list(edge) for edge in cond_edges]
    return {"component": component, "condensation": condensation}


def topo(request):
    n = request.get("n", 0)
    edges = request.get("edges", [])
    if n == 0:
        return {"acyclic": True, "order": []}
    
    adj = [[] for _ in range(n)]
    for edge in edges:
        u, v = edge[0], edge[1]
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)

    state = [0] * n  # 0: unvisited, 1: active, 2: finished
    order = []
    acyclic = True

    def dfs(u):
        nonlocal acyclic
        if not acyclic:
            return
        state[u] = 1
        for v in adj[u]:
            if state[v] == 1:
                acyclic = False
                return
            elif state[v] == 0:
                dfs(v)
                if not acyclic:
                    return
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            dfs(i)
            if not acyclic:
                return {"acyclic": False, "order": []}

    order.reverse()
    return {"acyclic": True, "order": order}


def dag(request):
    n = request.get("n", 0)
    source = request.get("source", 0)
    edges = request.get("edges", [])
    if n == 0:
        return {"acyclic": True, "distance": [], "parent_edge": []}
    
    adj = [[] for _ in range(n)]
    for idx, edge in enumerate(edges):
        u, v, w = edge[0], edge[1], edge[2]
        if 0 <= u < n and 0 <= v < n:
            adj[u].append((v, w, idx))

    state = [0] * n
    acyclic = True

    def check_cycle(u):
        nonlocal acyclic
        if not acyclic:
            return
        state[u] = 1
        for v, w, idx in adj[u]:
            if state[v] == 1:
                acyclic = False
                return
            elif state[v] == 0:
                check_cycle(v)
                if not acyclic:
                    return
        state[u] = 2

    for i in range(n):
        if state[i] == 0:
            check_cycle(i)
            if not acyclic:
                return {"acyclic": False, "distance": [], "parent_edge": []}

    order = []
    state = [0] * n
    def topo_dfs(u):
        state[u] = 1
        for v, w, idx in adj[u]:
            if state[v] == 0:
                topo_dfs(v)
        state[u] = 2
        order.append(u)

    for i in range(n):
        if state[i] == 0:
            topo_dfs(i)
    order.reverse()

    distance = [None] * n
    parent_edge = [-1] * n

    if 0 <= source < n:
        distance[source] = 0
        parent_edge[source] = -1

    for u in order:
        if distance[u] is not None:
            for v, w, idx in adj[u]:
                new_dist = distance[u] + w
                if distance[v] is None or new_dist < distance[v]:
                    distance[v] = new_dist
                    parent_edge[v] = idx

    return {"acyclic": True, "distance": distance, "parent_edge": parent_edge}


def reconstruct_route(source, target, parent_edge, edges):
    """
    Route reconstruction helper.
    """
    if source == target:
        return [source]
    
    curr = target
    edge_map = {idx: (u, v) for idx, (u, v, *_) in enumerate(edges)}
    path_edges = []
    
    while curr != source:
        p_edge = parent_edge[curr]
        if p_edge == -1 or p_edge not in edge_map:
            return []
        u, v = edge_map[p_edge]
        if v != curr:
            return []
        path_edges.append(p_edge)
        curr = u
        
    path_edges.reverse()
    route = [source]
    curr = source
    for p_edge in path_edges:
        u, v = edge_map[p_edge]
        route.append(v)
        curr = v
        
    return route if route[-1] == target else []
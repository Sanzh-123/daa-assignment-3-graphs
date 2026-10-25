### Command to Run

```
$env:PYTHONIOENCODING="utf-8"
python tools/run.py --input tests/my_cases.jsonl

```

### Test Cases

#### Test Case 1: DSU Empty Graph ($n=0$)

* **Input:** `{"task":"dsu","n":0,"operations":[]}`
* **Expected & Actual Output:** `{"states":[]}`
* **Justification:** An empty graph has no vertices or operations, resulting in an empty states array.

#### Test Case 2: Kruskal Minimum Spanning Forest (Triangle Graph)

* **Input:** `{"task":"kruskal","n":3,"edges":[[0,1,1],[1,2,1],[0,2,1]]}`
* **Expected & Actual Output:** `{"cost":2,"edge_ids":[0,1],"components":1}`
* **Justification:** Connects 3 vertices using 2 edges of weight 1, yielding a total cost of 2 and 1 connected component.

#### Test Case 3: Prim Minimum Spanning Forest

* **Input:** `{"task":"prim","n":3,"edges":[[0,1,5],[1,2,5],[0,2,5]]}`
* **Expected & Actual Output:** `{"cost":10,"edge_ids":[0,1],"components":1}`
* **Justification:** Prim greedily selects two edges of weight 5 to span all 3 vertices for a total cost of 10.

#### Test Case 4: SCC with Self-Loop and Duplicate

* **Input:** `{"task":"scc","n":3,"edges":[[0,1],[1,2],[2,0],[1,1]]}`
* **Expected & Actual Output:** `{"component":[0,0,0],"condensation":[]}`
* **Justification:** Vertices 0, 1, and 2 form a single strongly connected cycle; self-loops and duplicate edges are safely handled.

#### Test Case 5: Topological Sort with Cycle

* **Input:** `{"task":"topo","n":3,"edges":[[0,1],[1,2],[2,0]]}`
* **Expected & Actual Output:** `{"acyclic":false,"order":[]}`
* **Justification:** The graph contains a directed cycle ($0 \to 1 \to 2 \to 0$), so `acyclic` is `false` and `order` is empty.

#### Test Case 6: DAG Shortest Paths

* **Input:** `{"task":"dag","n":3,"source":0,"edges":[[0,1,2],[1,2,3],[0,2,10]]}`
* **Expected & Actual Output:** `{"acyclic":true,"distance":[0,2,5],"parent_edge":[-1,0,1]}`
* **Justification:** Shortest path to vertex 2 goes through vertex 1 with total distance $2 + 3 = 5$, via edge IDs 0 and 1.

```
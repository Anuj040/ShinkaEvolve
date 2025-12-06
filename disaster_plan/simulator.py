import random
import networkx as nx
from typing import Callable
def block_random_edges(G:nx.MultiDiGraph, p:float=0.02) -> nx.MultiDiGraph:
    """Randomly mark p% of edges as blocked."""
    G_sim = G.copy()
    random.seed(42) # for reproducibility
    for u, v, k in G_sim.edges(keys=True):
        G_sim.edges[u, v, k]["blocked"] = random.random() < p
    return G_sim

def route_to_target(G:nx.MultiDiGraph, start, target):
    """Compute shortest path ignoring blocked edges."""
    G2 = G.copy()
    # remove blocked edges
    blocked_edges = [(u, v, k) for u, v, k in G2.edges(keys=True)
                     if G2.edges[u, v, k].get("blocked", False)]
    G2.remove_edges_from(blocked_edges)
    try:
        return nx.shortest_path(G2, start, target)
    except Exception:
        return None  # unreachable

def run_scenario(G, depot, shelter_nodes, choose_next_target_fn: Callable) -> float:
    """Run a simulation scenario. Returns a score (higher is better)."""

    served = set()
    current = depot
    total_steps = 0
    hazard_pen = 0

    for _ in range(300):  # max steps
        # Done?
        if len(served) == len(shelter_nodes):
            break

        # Pick next target (this is where evolution kicks in)
        target = choose_next_target_fn(
            G_sim=G,
            current_node=current,
            shelters=shelter_nodes,
            served=served
        )

        path = route_to_target(G, current, target)
        if path is None:
            # Unreachable → penalty
            hazard_pen += 5
            continue

        # Move along one edge
        nxt = path[1] if len(path) > 1 else current
        # Check if stepped into hazard
        for edge_info in G.edges(current, nxt, keys=True):
            u, v, k = edge_info[:3]
            if G.edges[u, v, k].get("blocked", False):
                hazard_pen += 1

        current = nxt
        total_steps += 1

        # Delivered?
        if current in shelter_nodes:
            served.add(current)

    unmet = len(shelter_nodes) - len(served)

    return -total_steps - 20 * unmet - hazard_pen

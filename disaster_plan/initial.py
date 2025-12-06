# initial.py
import pickle
import networkx as nx
from simulator import run_scenario, block_random_edges

bundle = pickle.load(open("data/shibuya_bundle.pkl", "rb"))
G = bundle["graph"]
SHELTERS = bundle["shelters"]["nearest_node"].tolist()
DEPOT = bundle["depot_node"]

# ===============================
# EVOLVE-BLOCK
# ===============================

# EVOLVE-BLOCK-START
def choose_next_target(G_sim, current_node, shelters, served):
    """
    Baseline heuristic:
    Move to the closest unserved shelter by shortest path length.
    ShinkaEvolve will mutate this.
    """
    best = None
    best_dist = 999999
    for s in shelters:
        if s not in served:
            d = nx.shortest_path_length(G_sim, current_node, s)
            if d < best_dist:
                best_dist = d
                best = s
    return best
# EVOLVE-BLOCK-END


# ===============================
# SHINKAEVOLVE EVALUATION FUNCTION
# ===============================

def run_experiment(seed=0, num_scenarios=5):
    import random
    rng = random.Random(seed)
    scores = []

    for _ in range(num_scenarios):
        # randomize blocked edges
        G_sim = block_random_edges(G, p=0.02)
        score = run_scenario(
            G_sim,
            DEPOT,
            SHELTERS,
            choose_next_target
        )
        scores.append(score)

    avg_score = sum(scores) / len(scores)
    feedback = "\n".join([f"scenario_score={s}" for s in scores])
    return avg_score, feedback

from simulator import run_scenario, block_random_edges
import pickle
import networkx as nx
from pathlib import Path

def run_simulator(shelter_data_bundle:str) -> float:

    bundle = pickle.load(open(Path(shelter_data_bundle), "rb"))
    G = bundle["graph"]
    depot = bundle["depot_node"]
    shelters = bundle["shelters"]["nearest_node"].tolist()[-2:]

    def baseline_policy(current_node, shelters, served) -> int:
        # naive baseline: go to closest unserved node
        best = None
        best_dist = 999999
        for s in shelters:
            if s not in served:
                d = nx.shortest_path_length(G, current_node, s)
                if d < best_dist:
                    best_dist = d
                    best = s
        return best

    G_sim = block_random_edges(G, p=0.02)
    return run_scenario(G_sim, depot, shelters, baseline_policy)

if __name__ == "__main__":
    print(run_simulator("disaster_plan/data/shibuya_bundle.pkl"))
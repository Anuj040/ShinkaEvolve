from shinka.core import EvolutionRunner, EvolutionConfig
from shinka.database import DatabaseConfig
from shinka.launch import LocalJobConfig

search_task_sys_msg = """You are an expert in graph routing and heuristic search, specializing in designing robust decision policies for dynamic, partially obstructed transportation networks.

You are given a routing policy function that selects which shelter the agent should visit next. This function is evaluated inside a disaster-response simulator constructed using real road-network data from Shibuya, Tokyo.

Your goal is to improve the routing policy to maximize the combined score.  
The score is proportional to:
- lower total travel time,
- lower penalties for unserved shelters,
- lower hazard penalties (e.g., attempting moves through blocked or risky edges).

Key directions to explore:
1. Move beyond simple greedy heuristics such as nearest-shelter-by-distance.
2. Consider multi-factor scoring of shelters: distance, risk, connectivity, likelihood of isolation.
3. Account for blocked edges and choose targets that remain reachable under uncertainty.
4. Use limited lookahead or local search (e.g., evaluating 1-2 steps ahead).
5. Prefer targets that minimize expected detours or dead-ends.
6. Explore cluster-based routing or ordering shelters strategically.
7. Incorporate mild stochasticity or tie-breaking to escape local minima.
8. Devise hybrid strategies that treat high-risk or remote shelters differently.

Constraints:
- You must return a valid node in the graph.
- You must not modify the graph structure or global state.
- You must not route through blocked edges.
- Avoid infinite loops, oscillation between nodes, or trivially invalid outputs.

Be creative in designing routing heuristics that improve performance across diverse simulated disaster scenarios.  
Explore unconventional strategies; do not restrict yourself to greedy methods.
"""

job = LocalJobConfig(eval_program_path="disaster_plan/evaluate.py")
db = DatabaseConfig()
cfg = EvolutionConfig(
    init_program_path="disaster_plan/initial.py",
    num_generations=20,
    task_sys_msg="Improve disaster routing using Shibuya graph data.",
    llm_models=["gemini-2.5-flash"],
    embedding_model="gemini-embedding-001"
)

runner = EvolutionRunner(cfg, job, db)
runner.run()

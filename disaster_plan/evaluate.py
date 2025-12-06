# evaluate.py
from shinka.core import run_shinka_eval

def get_kwargs(run_idx):
    return {"seed": run_idx, "num_scenarios": 5}

def aggregate_fn(results):
    scores = [r[0] for r in results]
    return {
        "combined_score": sum(scores)/len(scores),
        "public": {"avg_score": sum(scores)/len(scores)},
        "private": {},
        "extra_data": {"scores": scores},
        "text_feedback": str(scores),
    }

def validate_fn(result) -> bool:
    score, _ = result
    return -10000 < score < 10000

def main(program_path:str, results_dir:str) -> None:
    run_shinka_eval(
        program_path=program_path,
        results_dir=results_dir,
        experiment_fn_name="run_experiment",
        num_runs=3, # evaluate multiple times with different seeds
        get_experiment_kwargs=get_kwargs,
        aggregate_metrics_fn=aggregate_fn,
        validate_fn=validate_fn,
    )

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--program_path")
    parser.add_argument("--results_dir")
    args = parser.parse_args()
    main(args.program_path, args.results_dir)

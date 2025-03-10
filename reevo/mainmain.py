import hydra
import logging 
import os
from pathlib import Path
import subprocess
from utils.utils import init_client
import glob
os.environ["HYDRA_FULL_ERROR"] = "1"
ROOT_DIR = os.getcwd()
logging.basicConfig(level=logging.INFO)

@hydra.main(version_base=None, config_path="cfg", config_name="config")
def main(cfg):
    workspace_dir = Path.cwd()
    # Set logging level
    logging.info(f"Workspace: {workspace_dir}")
    logging.info(f"Project Root: {ROOT_DIR}")
    logging.info(f"Using LLM: {cfg.get('model', cfg.llm_client.model)}")
    logging.info(f"Using Algorithm: {cfg.algorithm}")

    client = init_client(cfg)

    if cfg.algorithm == "reevo":
        from moomoo import ReEvoMooMoo as LHH
    elif cfg.algorithm == "ael":
        from baselines.ael.ga import AEL as LHH
    elif cfg.algorithm == "eoh":
        from baselines.eoh import EoH as LHH
    else:
        raise NotImplementedError

    # Main algorithm
    lhh = LHH(cfg, ROOT_DIR, client)
    best_code_pareto_overall, best_code_pareto_path_overall = lhh.evolve()
    logging.info(f"Best Pareto Code Overall (list): {best_code_pareto_overall}")
    logging.info(f"Best Pareto Code Path Overall (list): {best_code_pareto_path_overall}")

    if not best_code_pareto_overall:
        raise RuntimeError("Pareto front is empty. No valid candidates to validate.")

    candidate_dir = f"{ROOT_DIR}/problems_moo/{cfg.problem.problem_name}"
    os.makedirs(candidate_dir, exist_ok=True)
    # Remove any previous candidate files and gpt.py
    for filepath in glob.glob(os.path.join(candidate_dir, "gpt_candidate_*.py")):
        os.remove(filepath)
    gpt_file = os.path.join(candidate_dir, "gpt.py")
    if os.path.exists(gpt_file):
        os.remove(gpt_file)
    # eval eval
    validation_results = {}
    for i, candidate_code in enumerate(best_code_pareto_overall):
        candidate_file = os.path.join(candidate_dir, f"gpt_candidate_{i}.py")
        gpt_to_eval_file = os.path.join(candidate_dir, f"gpt.py")
        with open(candidate_file, 'w') as file:
            file.write(candidate_code + '\n')
        with open(gpt_to_eval_file, 'w') as file:
            file.write(candidate_code + '\n')
        
        test_script = f"{ROOT_DIR}/problems_moo/{cfg.problem.problem_name}/eval.py"
        test_script_stdout = f"best_code_overall_val_stdout_{i}.txt"
        
        logging.info(f"Running validation script for candidate {i}...: {test_script}")
        with open(test_script_stdout, 'w') as stdout:
            subprocess.run(["python", test_script, "-1", ROOT_DIR, "val"], stdout=stdout)
        
        logging.info(f"Validation for candidate {i} finished. Results are saved in {test_script_stdout}.")

        with open(test_script_stdout, 'r') as file:
            result_lines = file.readlines()
            validation_results[f"candidate_{i}"] = [line.strip() for line in result_lines]
            for line in result_lines:
                logging.info(f"Candidate {i}: {line.strip()}")

    logging.info("Validation Results for all candidates:")
    for candidate, results in validation_results.items():
        logging.info(f"{candidate}: {results}")


if __name__ == "__main__":
    main()
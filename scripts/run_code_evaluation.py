import os
import json
import time
import argparse
import traceback

from glob import glob
from os.path import join as pjoin

from tqdm import tqdm
from termcolor import colored

from bytes32 import check_winnability
from bytes32 import check_compliance
from bytes32 import check_alignment
from bytes32 import check_validity
from bytes32.utils import get_empty_metrics


def automatic_evaluation(gamefile, args, metrics=None):
    """ Automatically evaluate one game """

    metrics = metrics or get_empty_metrics()

    # Run validity check.
    print(colored("Running validity check...", "yellow"))
    metrics["validity"] = check_validity(gamefile, args)

    # Run GPT evaluation for compliance.
    if not args.skip_check_compliance:
        metrics["compliance"] = check_compliance(gamefile, args)

    if metrics["validity"]["error_msg"] and not args.ignore_validity_errors:
        return metrics  # Can't run the program correctly.

    # Run GPT evaluation for alignment.
    if not args.skip_check_alignment:
        metrics["alignment"] = check_alignment(gamefile, args)

    # Run GPT agent for winnability.
    if not args.skip_check_winnability:
        try:
            print(colored("Running winnability check...", "yellow"))
            metrics["winnability"] = check_winnability(gamefile, args.agent_model_name, args.game_random_seed, args.env_step_limit)
        except Exception as e:
            stacktrace = [frame.replace(os.getcwd(), "").strip() for frame in traceback.format_tb(e.__traceback__) if gamefile in frame or "language_agent.py" in frame]
            metrics["validity"]["error_msg"] = "\n".join(stacktrace) + "\n" + str(e)

    return metrics


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--game-folder")
    group.add_argument("--games", nargs="+")

    parser.add_argument("--results-file", type=str, default="eval_results.json")

    parser.add_argument("--skip-check-alignment", action="store_true")
    parser.add_argument("--skip-check-compliance", action="store_true")
    parser.add_argument("--skip-check-winnability", action="store_true")
    parser.add_argument("--ignore-validity-errors", action="store_true",
                        help="Ignore validity errors and run alignment and winnability checks anyway.")

    validity_group = parser.add_argument_group("Technical Validity")
    validity_group.add_argument("--max-steps", type=int, default=3)
    validity_group.add_argument("--random-seed", type=int, default=0)
    validity_group.add_argument("--max-num-actions", type=int, default=100)

    compliance_group = parser.add_argument_group("Specification Compliance")
    compliance_group.add_argument("--compliance-model-name", default="gpt-4")
    compliance_group.add_argument("--evaluation-form", type=str, default="data/test_eval.csv")
    compliance_group.add_argument("--test-prompt-input-folder", type=str, default="data/test_prompts")
    compliance_group.add_argument("--compliance-majority-vote", type=int, default=31)

    alignment_group = parser.add_argument_group("Physical Reality Alignment")
    alignment_group.add_argument("--alignment-model-name", default="gpt-4")
    alignment_group.add_argument("--shuffle-random-seed", type=int, default=0)
    alignment_group.add_argument("--max-depth", type=int, default=2)
    alignment_group.add_argument("--max-paths", type=int, default=25000)
    alignment_group.add_argument("--error-strategy", type=str, default="fail")
    alignment_group.add_argument("--num-samples-per-game", type=int, default=100)
    alignment_group.add_argument("--sample-strategy", type=str, default="action_even")
    alignment_group.add_argument("--alignment-batch-size", type=int, default=1)

    winnability_group = parser.add_argument_group("Winnability")
    winnability_group.add_argument("--agent-model-name", default="gpt-4")
    winnability_group.add_argument("--env-step-limit", type=int, default=30)
    winnability_group.add_argument("--game-random-seed", type=int, default=20230614)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    results = {}
    if os.path.exists(args.results_file):
        input(colored(f"WARNING: {args.results_file} already exists, data will be updated.\nPress Enter to continue...", "red", attrs={'bold': True}))
        with open(args.results_file) as f:
            results = json.load(f)

    gamefiles = args.games or glob(pjoin(args.game_folder, "*.py"))
    pbar = tqdm(sorted(gamefiles))
    for gamefile in pbar:
        time.sleep(0.1)
        pbar.set_description(os.path.basename(gamefile))

        if os.path.basename(gamefile) in results:
            continue

        existing_metrics = results.get(os.path.basename(gamefile), {}).get("metrics")
        existing_reflection_prompt = results.get(os.path.basename(gamefile), {}).get("reflection_prompt", "")
        existing_reflection_response = results.get(os.path.basename(gamefile), {}).get("reflection_response", "")
        new_metrics = automatic_evaluation(gamefile, args, metrics=existing_metrics)
        results[os.path.basename(gamefile)] = {
            "metrics": new_metrics,
            "reflection_prompt": existing_reflection_prompt,
            "reflection_response": existing_reflection_response
        }

        with open(args.results_file, 'w') as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

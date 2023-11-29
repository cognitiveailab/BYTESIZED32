import os
import re
import json
import time
import shutil
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
from bytes32.utils import stream_llm_gpt, count_tokens, extract_python_code, get_empty_metrics


def automatic_evaluation(gamefile, args):
    """ Automatically evaluate one game """

    metrics = get_empty_metrics()

    # Compare new code with the one from the previous iteration.
    # Find the lastest code revision.
    version = int(re.search(r"_v(\d+)\.py", gamefile).group(1))
    if version > 0:
        old_gamefile = gamefile.replace(f"v{version}.py", f"v{version-1}.py")

        with open(old_gamefile) as f:
            old_code = f.read()

        with open(gamefile) as f:
            new_code = f.read()

        if new_code == old_code:
            metrics["validity"]["error_msg"] = "STOP: Code is the same as previous iteration."
            return metrics

        if len(new_code) / len(old_code) < 0.5:
            metrics["validity"]["error_msg"] = "STOP: Code has 50% less lines than previous iteration."
            return metrics

    # Run validity check.
    print(colored("Running validity check...", "yellow"))
    metrics["validity"] = check_validity(gamefile, args)
    if metrics["validity"]["error_msg"]:
        return metrics

    # Run GPT evaluation for compliance.
    if args.reflect_compliance:
        metrics["compliance"] = check_compliance(gamefile, args)
        if not metrics["compliance"]["passed"]:
            return metrics

    # Run GPT evaluation for alignment.
    if args.reflect_alignment:
        metrics["alignment"] = check_alignment(gamefile, args)
        if not metrics["alignment"]["aligned"]:
            return metrics

    # Run GPT agent for winnability.
    if args.reflect_winnability:
        try:
            print(colored("Running winnability check...", "yellow"))
            metrics["winnability"] = check_winnability(gamefile, args.agent_model_name, args.game_random_seed, args.env_step_limit)
        except Exception as e:
            stacktrace = [frame.replace(os.getcwd(), "").strip() for frame in traceback.format_tb(e.__traceback__) if gamefile in frame or "language_agent.py" in frame]
            metrics["validity"]["error_msg"] = "\n".join(stacktrace) + "\n" + str(e)

    return metrics


def reflect(gamefile, metrics, args):
    with open(gamefile, 'r') as f:
        generated_game = f.read()

        if args.strip_comments:
            # Remove Python comments from generated_game.
            generated_game = re.sub(r'#[^\n]*', '', generated_game)

    # 'DeveloperGPT' prompt from @skirano
    prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out. \n"

    prompt += "Your task is to correct a buggy program that represents a text-based simulation.\n"

    if args.reflect_with_reference_game:
        # Load reference game
        reference_name = os.path.basename(gamefile).rsplit("_", 1)[0] + ".py"
        with open(pjoin(args.game_folder, "..", "gold-games", "program", reference_name)) as f:
            reference_game = f.read()

        if args.strip_comments:
            # Remove Python comments from reference_game.
            reference_game = re.sub(r'#[^\n]*', '', reference_game)

        prompt += "Here is the example code the buggy program was based on \n"
        prompt += "```"
        prompt += reference_game
        prompt += "```\n"

    prompt += "Here is the code of the buggy program \n"
    prompt += "```"
    prompt += generated_game
    prompt += "```\n"

    if metrics["validity"]["error_msg"] and metrics["winnability"]["transcript"]:
        prompt_ = "Here is the error message from a Python interpretor\n."
        prompt_ += metrics["validity"]["error_msg"]
        prompt_ += "\n"
        prompt_ += "Here's the transcript of someone playing the game when that error happened:\n"
        prompt_ += "```"
        prompt_ += metrics["winnability"]["transcript"]
        prompt_ += "```\n"
        prompt_ += "Based on this transcript and the Python error raised while playing the game, identify the problems and fix the code accordingly.\n"
    elif metrics["validity"]["error_msg"]:
        prompt_ = "Here is the error message from a Python interpretor.\n"
        prompt_ += metrics["validity"]["error_msg"]
        prompt_ += "\n"
    elif args.reflect_compliance and not metrics["compliance"]["passed"] and metrics["compliance"]["response_msg"]:
        prompt_ = f"While there were no errors from the Python interpretor, the game misses a required {metrics['compliance']['experiment']}. Here's the evaluation comments of the game:\n"
        prompt_ += "```"
        prompt_ += metrics["compliance"]["response_msg"]
        prompt_ += "```\n"
        prompt_ += "Based on this comments, identify the problems and fix the code accordingly.\n"
    elif args.reflect_alignment and not metrics["alignment"]["aligned"] and metrics["alignment"]["response_msg"]:
        prompt_ = f"While there were no errors from the Python interpretor, the game does not correctly model the physical world. Here's the evaluation comments of the game:\n"
        prompt_ += "```"
        prompt_ += metrics["alignment"]["response_msg"]
        prompt_ += "```\n"
        prompt_ += "Based on this comments, identify the problems and fix the code accordingly.\n"
    elif args.reflect_winnability and metrics["winnability"]["gpt_bug"]:
        prompt_ = "While there were no errors from the Python interpretor, the game was not working as intended. Here's the transcript of the broken game:\n"
        prompt_ += "```"
        prompt_ += metrics["winnability"]["transcript"]
        prompt_ += "```\n"
        prompt_ += "Based on this transcript, identify the problems and fix the code accordingly.\n"
    elif args.reflect_winnability and metrics["winnability"]["gpt_done"] and not metrics["winnability"]["done"]:
        prompt_ = "While there were no errors from the Python interpretor, the game couldn't be completed as expected. Here's the transcript of the broken game:\n"
        prompt_ += "```"
        prompt_ += metrics["winnability"]["transcript"]
        prompt_ += "```\n"
        prompt_ += "Based on this transcript, identify the problems and fix the code accordingly.\n"
    elif args.reflect_winnability and metrics["winnability"]["step"] >= metrics["winnability"]["max_steps"]:
        prompt_ = f"While there were no errors from the Python interpretor, the game couldn't be completed as expected within {args.env_step_limit*2} steps. Here's the transcript of the broken game:\n"
        prompt_ += "```"
        prompt_ += metrics["winnability"]["transcript"]
        prompt_ += "```\n"
        prompt_ += "Based on this transcript, identify the problems and fix the code accordingly.\n"
    else:
        raise NotImplementedError()

    print(colored(prompt_, "cyan"))
    prompt += prompt_

    prompt += "You must provide the *full working code* that includes the fix. Do not respond with partial code or say anything else."

    print(colored(f"Prompting {args.reflect_model_name} for reflection...", "yellow"))
    response = stream_llm_gpt(prompt, model=args.reflect_model_name)
    print(colored(f"Responded with {count_tokens(response)} tokens.", "yellow"))
    generated_game = extract_python_code(response)

    return generated_game, prompt, response


def find_latest_revision(source, args):
    game_name = os.path.basename(source)[:-3]

    # Find the lastest code revision.
    for i in range(args.max_reflection_steps + 1)[::-1]:
        gamefile = pjoin(args.revision_folder, f"{game_name}_v{i}.py")
        if os.path.exists(gamefile):
            return i, gamefile

    return 0, source


def stop_reflection(metrics, args):
    if metrics["validity"]["error_msg"].startswith("STOP:"):
        return True

    return (
        # The game has no error and is runnable, and the GPT agent has finished the game without reporting a bug.
        metrics["validity"]["error_msg"] == "" and
        metrics["validity"]["runnable"] and
        (not args.reflect_compliance or metrics["compliance"]["passed"]) and
        (not args.reflect_winnability or not metrics["winnability"]["gpt_bug"]) and
        (not args.reflect_winnability or metrics["winnability"]["done"])
    )


def perform_code_reflection(source, args):
    game_name = os.path.basename(source)[:-3]
    last_revision, gamefile = find_latest_revision(source, args)
    if last_revision == 0:
        gamefile = pjoin(args.revision_folder, f"{game_name}_v0.py")
        shutil.copyfile(source, gamefile)

    metrics = automatic_evaluation(gamefile, args)
    yield gamefile, {"metrics": metrics, "reflection_prompt": "", "reflection_response": ""}

    # Prompt GPT for code revision until automatic evaluation yields success or we reach max reflection steps.
    for i in range(last_revision, args.max_reflection_steps):
        if stop_reflection(metrics, args):
            # The new code is the same as the old code, or has 50% less lines of code.
            # The game has no error and is runnable, and the GPT agent has finished the game without reporting a bug.
            break

        reflection_game, reflection_prompt, reflection_response = reflect(gamefile, metrics, args)
        gamefile = pjoin(args.revision_folder, f"{game_name}_v{i+1}.py")
        with open(gamefile, 'w') as f:
            f.write(reflection_game)

        metrics = automatic_evaluation(gamefile, args)
        yield gamefile, {"metrics": metrics, "reflection_prompt": reflection_prompt, "reflection_response": reflection_response}


def parse_args():
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--game-folder")
    group.add_argument("--games", nargs="+")

    parser.add_argument("--results-file", default="results.json")
    parser.add_argument("--revision-folder", default="revised_games/",
                        help="Where to save the revised games. Default: %(default)s")
    parser.add_argument("--final-folder", default="final_games/",
                        help="Where to save the final revised games. Default: %(default)s")

    parser.add_argument("--reflect-model-name", default="gpt-4-32k")
    parser.add_argument("--max-reflection-steps", type=int, default=3)
    parser.add_argument("--strip-comments", action="store_true",
                        help="Remove Python comments from generated_game to save context space.")
    parser.add_argument("--reflect-with-reference-game", action="store_true",
                        help="Also, provide the original reference game during reflection (NB: requires very large context size).")

    parser.add_argument("--reflect-alignment", action="store_true",
                        help="Also, reflect on physical reality alignment.")
    parser.add_argument("--reflect-compliance", action="store_true",
                        help="Also, reflect on specification compliance.")
    parser.add_argument("--reflect-winnability", action="store_true",
                        help="Also, reflect on game winnability.")

    validity_group = parser.add_argument_group("Technical Validity")
    validity_group.add_argument("--max-steps", type=int, default=3)
    validity_group.add_argument("--random-seed", type=int, default=0)
    validity_group.add_argument("--max-num-actions", type=int, default=100)

    compliance_group = parser.add_argument_group("Specification Compliance")
    compliance_group.add_argument("--compliance-model-name", default="gpt-4")
    compliance_group.add_argument("--evaluation-form", type=str, default="data/test_eval.csv")
    compliance_group.add_argument("--test-prompt-input-folder", type=str, default="data/test_prompts")

    alignment_group = parser.add_argument_group("Physical Reality Alignment")
    alignment_group.add_argument("--alignment-model-name", default="gpt-4")
    alignment_group.add_argument("--shuffle-random-seed", type=int, default=0)
    alignment_group.add_argument("--max-depth", type=int, default=2)
    alignment_group.add_argument("--max-paths", type=int, default=25000)
    alignment_group.add_argument("--error-strategy", type=str, default="fail")
    alignment_group.add_argument("--num-samples-per-game", type=int, default=100)
    alignment_group.add_argument("--sample-strategy", type=str, default="action_even")

    winnability_group = parser.add_argument_group("Game Winnability")
    winnability_group.add_argument("--agent-model-name", default="gpt-4")
    winnability_group.add_argument("--env-step-limit", type=int, default=30)
    winnability_group.add_argument("--game-random-seed", type=int, default=20230614)

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # Create a folder to store revised and final games.
    os.makedirs(args.revision_folder, exist_ok=True)
    os.makedirs(args.final_folder, exist_ok=True)

    reflection_results = {}
    if os.path.exists(args.results_file):
        input(colored(f"WARNING: {args.results_file} already exists, data will be appended to it.\nPress Enter to continue...", "red", attrs={'bold': True}))
        with open(args.results_file) as f:
            reflection_results = json.load(f)

    gamefiles = args.games or glob(pjoin(args.game_folder, "*.py"))
    pbar = tqdm(sorted(gamefiles))
    for gamefile in pbar:
        time.sleep(0.1)
        pbar.set_description(os.path.basename(gamefile))

        latest_revision, revised_gamefile = find_latest_revision(gamefile, args)
        if latest_revision >= args.max_reflection_steps:
            continue

        if os.path.basename(revised_gamefile) in reflection_results:
            if stop_reflection(reflection_results[os.path.basename(revised_gamefile)]["metrics"], args):
                # The new code is the same as the old code, or has 50% less lines of code.
                # The game has no error and is runnable, and the GPT agent has finished the game without reporting a bug.
                continue

        for revised_gamefile, stats in perform_code_reflection(gamefile, args):
            reflection_results[os.path.basename(revised_gamefile)] = stats
            with open(args.results_file, 'w') as f:
                json.dump(reflection_results, f, indent=2)

        # Copy the final revised game to a separate folder.
        final_gamefile = pjoin(args.final_folder, os.path.basename(revised_gamefile).replace(".py", "_final.py"))
        shutil.copyfile(revised_gamefile, final_gamefile)


if __name__ == "__main__":
    main()

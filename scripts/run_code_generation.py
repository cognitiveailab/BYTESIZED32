import os
import re
import time
import datetime
import argparse
from os.path import join as pjoin

import pandas as pd
from termcolor import colored

from bytes32.utils import count_tokens, stream_llm_gpt, extract_python_code, load_program


MAX_CONTEXT_LENGTH = 32000
MAX_PROGRAM_LENGTH = 16000


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment_file", help="CSV file")
    parser.add_argument("--data", type=str, default="./data/")
    parser.add_argument("--output-folder", type=str, default=f"./results/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}/generated_games/")
    parser.add_argument("--model", type=str, default="gpt-4-32k")

    parser.add_argument("--strip-comments", action="store_true")
    parser.add_argument("--zero-shot", action="store_true", help="Perform zero-shot generation (no in-context example code).")

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    os.makedirs(args.output_folder, exist_ok=True)

    experiment_name = args.experiment_file.split("/")[-1].split(".csv")[0]
    experiment_df = pd.read_csv(args.experiment_file, header=None)
    for n, row in experiment_df.iterrows():
        # The first prompt includes the desired feature, the second prompt does not
        ablation_games = {"p": row.values[0], "n": row.values[1]}

        for key in ablation_games:
            prompt_task = ablation_games[key]
            fileout_prefix = f"{experiment_name}_test_{n+1}_{key}_{args.model.split('/')[-1]}_{prompt_task[:-3]}"
            if os.path.exists(pjoin(args.output_folder, f'{fileout_prefix}_generation.py')):
                print(colored(f"Skipping: '{fileout_prefix}' already exists!", "yellow"))
                continue

            target_task = f"test_{n+1}.py"

            prompt_program = load_program(pjoin(args.data, "programs", prompt_task))
            if args.strip_comments:
                # Remove Python comments from generated_game.
                prompt_program = re.sub(r'#[^\n]*\n', '', prompt_program)

            print (f"Prompt program: {prompt_task}, total tokens: {count_tokens(prompt_program, args.model)}")

            target_spec = load_program(pjoin(args.data, "test_prompts", target_task))
            print (f"Prompt program: {target_spec}, total tokens: {count_tokens(target_spec, args.model)}")

            # 'DeveloperGPT' prompt from @skirano
            prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out.\n"

            prompt += "Your task is to write a program that: is a text-based simulation.\n"
            prompt += "The program should be written in Python.  It should be challenging to the user, testing their common-sense knowledge, and take multiple steps to complete.  If possible, there should be distractor objects and actions that do not help progress, to measure whether the user really knows what they're doing. You should name all target objects and distractor objects with common-sense names.\n"
            prompt += "Your code must contain a class named TextGame. The TextGame class should have the following member functions:\n"
            prompt += "__init__(self, randomSeed), getTaskDescription(self), generatePossibleActions(self), step(self, actionStr), calculateScore(self)\n"

            if not args.zero_shot:
                prompt += "\nHere is an example of a text-based simulation on a different topic that you can use as a template:\n"
                prompt += "```python\n"
                prompt += prompt_program
                prompt += "```\n"

            prompt += "\nProduce the Python code for the following task specification:\n"
            prompt += "```python\n"
            prompt += target_spec + "\n\n"

            prompt_out_file = pjoin(args.output_folder, f'{fileout_prefix}_prompt_out.txt')
            print(f"Writing prompt to file {prompt_out_file})")
            with open(prompt_out_file, 'w') as f:
                f.write(prompt)

            print(colored(f"Prompting {args.model} for 1-shot generation...", "yellow"))
            context_length = count_tokens(prompt, args.model)
            print(colored(f"  Context length {context_length} tokens.", "yellow"))

            max_new_tokens = min(max(0, MAX_CONTEXT_LENGTH-context_length), MAX_PROGRAM_LENGTH)
            start = time.time()
            response = stream_llm_gpt(prompt, args.model, max_tokens=max_new_tokens)
            print(colored(f"  Response time: {time.time()-start} secs.", "yellow"))

            print(colored(f"  Responded with {count_tokens(response, args.model)} tokens.", "yellow"))
            programOut = extract_python_code(response)

            generation_txt_file = pjoin(args.output_folder,f"{fileout_prefix}_generation.txt")
            print (f"  Saving response to: {generation_txt_file}")
            with open(generation_txt_file, 'w') as f:
                f.write(response)

            generation_py_file = pjoin(args.output_folder,f"{fileout_prefix}_generation.py")
            print (f"  Saving postprocessed program to: {generation_py_file}")
            with open(generation_py_file, 'w') as f:
                f.write(programOut)


if __name__ == "__main__":
    main()

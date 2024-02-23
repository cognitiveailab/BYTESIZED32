import os
import time

import pandas as pd
from termcolor import colored

from bytes32.utils import llm_gpt, count_tokens, load_program


def build_requirement_text(evaluation_form_df, experiment, test_id):
    requirement = evaluation_form_df[experiment][int(test_id)-1]
    requirement_text = ''
    if experiment == 'object':
        requirement_text = f"Does the simulation have the object {requirement}?\n"
    elif experiment == 'distractor':
        requirement_text = f"Are the distractors required by the specification implemented in the simulation?\n"
    elif experiment == 'action':
        requirement_text = f"Does the simulation have the action {requirement}?\n"
    return requirement_text


def parse_game_file_name(game_file_name):
    splits = game_file_name.split("_")
    experiment = splits[1]
    test_id = splits[3]
    fold = splits[4]

    assert experiment in ('object', 'distractor', 'action')
    assert fold in ('p', 'n')
    assert test_id in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16')

    return experiment, test_id, fold


def check_compliance(gamefile, args):
    game_file_name = os.path.basename(gamefile)
    experiment, test_id, fold = parse_game_file_name(game_file_name)
    results = {"fold": fold, "experiment": experiment, "passed": False, "response_msg": ''}

    with open(args.evaluation_form) as f:
        evaluation_form_df = pd.read_csv(f)

    eval_requirement = build_requirement_text(evaluation_form_df, experiment, test_id)

    spec_prompt = load_program(f"{args.test_prompt_input_folder}/test_{test_id}.py")
    print (f"Specification prompt: {count_tokens(spec_prompt)} tokens.")

    generated_game = load_program(f"{gamefile}")
    print (f"Generated program: {count_tokens(generated_game)} tokens.")

    # 'DeveloperGPT' prompt from @skirano
    prompt = "You are DeveloperGPT, the most advanced AI developer tool on the planet.  You answer any coding question, and provide real useful example code using code blocks.  Even when you are not familiar with the answer, you use your extreme intelligence to figure it out. \n"

    prompt += "Your task is to evaluate a program that is a text-based simulation.\n"

    prompt += "Here is a specification of the simulation: \n"
    prompt += "```"
    prompt += spec_prompt
    prompt += "```\n"

    prompt += "Here is the code of the simulation \n"
    prompt += "```"
    prompt += generated_game
    prompt += "```\n"
    prompt += "Answer the following question based on the given specification and the simulation code:\n"
    prompt += eval_requirement

    prompt += "Answer 'Yes' or 'No' first and briefly explain your answer."

    start = time.time()
    print(colored(f"Prompting {args.compliance_model_name} for compliance evaluation (using {args.compliance_majority_vote} votes)...", "yellow"))

    responses = llm_gpt(prompt, model=args.compliance_model_name, n=args.compliance_majority_vote)
    if args.compliance_majority_vote == 1:
        responses = [responses]

    print(colored(f"  Response time: {time.time()-start} secs.", "yellow"))
    print(colored(f"  Responded with {sum(count_tokens(response) for response in responses)} tokens.", "yellow"))
    majority_vote = sum(response.lower().startswith('yes') for response in responses) / args.compliance_majority_vote
    print(colored(f"Majority vote: {majority_vote:.1%}", "green"))
    results["response_msg"] = "\n".join(responses)
    results["passed"] = majority_vote > 0.5

    return results

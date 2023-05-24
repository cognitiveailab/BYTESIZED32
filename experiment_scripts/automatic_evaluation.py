from random import random
import sys
import os
import json

game_folder = sys.argv[1]

sys.path.append(game_folder)

MAX_STEPS = 3

def automatic_evaluation(game_name):
    metrics = {
        "TextGame": False,
        "runnable": False,
        "winnable": False,
        "TextGame": False,
        "getTaskDescription": False,
        "generatePossibleActions": False,
        "step": False, # has the member function step
        "calculateScore": False,
        "num_valid_actions": 0
    }
    try:
        TextGame = __import__(game_name[:-3]).TextGame
        metrics["TextGame"] = True
        print(game_name)
    except Exception as e:
        print(e)
        return metrics

    try:
        game = TextGame(randomSeed=0)
        metrics['TextGame'] = True
        print("Successfully initialized the game.")
        print()
    except Exception as e:
        print(e)
        return metrics


    try:
        task_desc = game.getTaskDescription()
        metrics["getTaskDescription"] = True
        print(f"Task Description: {task_desc}")
        print()
    except Exception as e:
        print(e)
        return metrics

    try:
        game.calculateScore()
        metrics["calculateScore"] = True
        print("calculateScore is implemented.")
        print()
    except Exception as e:
        print(e)
        return metrics

    try:
        possible_actions = game.generatePossibleActions()
        num_first_step_possible_actions = len(possible_actions)
        metrics["num_valid_actions"] = num_first_step_possible_actions
        metrics["generatePossibleActions"] = True
        print()
    except Exception as e:
        print(e)
        return metrics

    # DFS search

    action_stack = []

    for action in possible_actions:
        action_stack.append([action])

    while len(action_stack) > 0:
        action_seq = action_stack.pop()
        game = TextGame(randomSeed=0)
        game.generatePossibleActions()
        for action in action_seq:
            try:
                game.step(action)
                metrics["step"] = True
            except Exception as e:
                print(e)
                metrics["step"] = False
                return metrics

        try:
            if not game.gameOver:
                if len(action_seq) < MAX_STEPS:
                    try:
                        possible_actions = game.generatePossibleActions()
                    except Exception as e:
                        print(e)
                        metrics["generatePossibleActions"] = False
                        return metrics
                    for possible_action in possible_actions:
                        action_stack.append(action_seq + [possible_action])

            elif game.gameWon:
                metrics['winnable'] = True
        except:
            return metrics

    metrics["runnable"] = True
    return metrics

eval_results = {}

if os.path.exists("eval_results.json"):
    with open("eval_results.json") as f:
        eval_results = json.load(f)

for game_name in os.listdir(game_folder):
    if not game_name.endswith(".py"):
        continue
    if game_name[5:] in eval_results:
        metrics = eval_results.pop(game_name[5:])
    else:
        metrics = automatic_evaluation(game_name)
    eval_results[game_name] = metrics

print(eval_results)

with open("eval_results.json", 'w') as f:
    json.dump(eval_results, f)




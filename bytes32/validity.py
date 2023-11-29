import os
import sys
import random
import importlib
import traceback

import signal
import random
from contextlib import contextmanager

# Keep track of special errors
timeoutErrors = []


@contextmanager
def timeout(time):
    # Ref: https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.alarm(time)

    try:
        yield
    except (TimeoutError, KeyboardInterrupt):
        pass
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    print("Timeout")
    raise TimeoutError


def sample_actions(possible_actions, max_num_actions, random_seed):
    actions_dict = {}
    for action in possible_actions:
        action_verb = action.split()[0]
        if action_verb in actions_dict:
            actions_dict[action_verb].append(action)
        else:
            actions_dict[action_verb] = [action]

    for action in actions_dict:
        if len(actions_dict[action]) > max_num_actions:
            downsampled_actions = random.Random(random_seed).sample(actions_dict[action], max_num_actions)
            actions_dict[action] = downsampled_actions

    possible_actions_out = []
    for action in actions_dict:
        possible_actions_out += actions_dict[action]

    return possible_actions_out


def check_validity(gamefile, args):
    """ Check the validty of a game: class, methods, scoring function, runnability."""
    checks = {
        "TextGame": False,
        "runnable": False,
        "winnable": False,
        "getTaskDescription": False,
        "generatePossibleActions": False,
        "step": False, # has the member function step
        "calculateScore": False,
        "num_valid_actions": 0,
        "error_msg": '',
    }

    timedOut = True
    timeoutDuration = 15 * 60   # 15 minutes
    with timeout(timeoutDuration):
        try:
            if os.path.dirname(gamefile) not in sys.path:
                sys.path.append(os.path.dirname(gamefile))

            TextGame = importlib.import_module(os.path.basename(gamefile)[:-3]).TextGame
            print(gamefile)
        except Exception as e:
            print(e)
            checks["error_msg"] = str(e)
            return checks

        try:
            game = TextGame(randomSeed=args.random_seed)
            checks['TextGame'] = True
            print("-> Successfully initialized the game.")
        except Exception as e:
            print(e)
            checks["error_msg"] = str(e)
            return checks

        try:
            task_desc = game.getTaskDescription()
            checks["getTaskDescription"] = True
            print(f"-> Task Description: {task_desc}")
        except Exception as e:
            print(e)
            checks["error_msg"] = str(e)
            return checks

        try:
            game.calculateScore()
            checks["calculateScore"] = True
            print("-> calculateScore() is implemented.")
        except Exception as e:
            print(e)
            checks["error_msg"] = str(e)
            return checks

        try:
            possible_actions = game.generatePossibleActions()
            num_first_step_possible_actions = len(possible_actions)
            checks["num_valid_actions"] = num_first_step_possible_actions
            checks["generatePossibleActions"] = True
            print("-> generatePossibleActions() is implemented.")
        except Exception as e:
            print(e)
            checks["error_msg"] = str(e)
            return checks

        # DFS search
        action_stack = []

        # truncate possible actions if the num of possible actions is too large
        possible_actions = sample_actions(possible_actions, args.max_num_actions, args.random_seed)
        for action in possible_actions:
            action_stack.append([action])

        while len(action_stack) > 0:
            action_seq = action_stack.pop()
            #print(action_seq)
            game = TextGame(randomSeed=args.random_seed)
            game.generatePossibleActions()
            for action in action_seq:
                try:
                    game.step(action)
                    checks["step"] = True
                except Exception as e:
                    stacktrace = [frame.replace(os.getcwd(), "").strip() for frame in traceback.format_tb(e.__traceback__) if gamefile in frame]
                    checks["step"] = False
                    checks["error_msg"] = "\n".join(stacktrace) + "\n" + str(e)
                    return checks

            try:
                if not game.gameOver:
                    if len(action_seq) < args.max_steps:
                        try:
                            possible_actions = game.generatePossibleActions()
                        except Exception as e:
                            stacktrace = [frame.replace(os.getcwd(), "").strip() for frame in traceback.format_tb(e.__traceback__) if gamefile in frame]
                            checks["generatePossibleActions"] = False
                            checks["error_msg"] = "\n".join(stacktrace) + "\n" + str(e)
                            return checks

                        # truncate possible actions if the num of possible actions is too large
                        possible_actions = sample_actions(possible_actions, args.max_num_actions//10, args.random_seed)
                        for possible_action in possible_actions:
                            action_stack.append(action_seq + [possible_action])

                elif game.gameWon:
                    checks['winnable'] = True
            except:
                return checks
        timedOut = False

    # Check to see if the game timed out during evaluation
    if timedOut:
        print("Evaluation timed out after " + str(timeoutDuration) + " seconds.")
        checks["error_msg"] = "Automatic evaluation timed out.  This could be due to an infinite loop in the code, waiting for user input outside the main() function, or some other issue or unusually-long-running procedure."
        # Record this timeout error
        timeoutErrors.append(gamefile)
        return checks

    checks["runnable"] = True
    print("-> game is runnable")
    return checks

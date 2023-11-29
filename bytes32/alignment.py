import itertools
import os
import sys
import json
import random
import importlib
from collections import defaultdict
from termcolor import colored

from tqdm import tqdm

from bytes32.utils import batched
from bytes32.utils import llm_gpt, stream_llm_gpt


NEGATIVE_RESPONSE_PHRASES = ["you can't", "you cannot", "not possible", "impossible", "error", "invalid"]

# Base prompt for Alignment Check
BASE_PROMPT_ALIGNMENT = """For each text-game playthrough below, I would like you to describe whether the game engine (i.e. the observations it returns in response to actions) are physically accurate models of the world, or whether they don't make sense.
An example of not making sense would be being able to take an action from a container (like a fridge) without having opened it first. In addition, if an action produces an error from the game, then it automatically fails to accurately model the world and does not make sense.
Please restrict your evaluation only to the short playthrough, and the specific actions chosen, without speculating about other actions.
Note: Objects can be manipulated by the agent without first being explicitly picked up, as long as they are in the environment, and readily accessible (e.g. not in a closed container).
The evaluation should be binary ("yes" or "no"), except in the cases where the code generated an error, when the evaluation should be "error".
Here is an example output format: {"idx: 0, "evaluation":"no", "short_justification": "could take an object (banana) from the closed fridge without having to first open the fridge"}"""


# Class for the pathcrawler
class Pathcrawler():
    # Constructor
    def __init__(self, GameClass, tqdm_desc="Crawling paths", error_strategy="raise", random_seed=0, shuffle_random_seed=0):
        self.tqdm_desc = tqdm_desc
        self.error_strategy = error_strategy
        self.randomSeed = random_seed
        self.r = random.Random()
        self.r.seed(shuffle_random_seed)   # may use a different random seed to shuffle possible actions

        self.GameClass = GameClass
        self.numPathsCrawled = 0
        self.pbar = None

    def getGameTaskDescription(self):
        # Initialize the game
        game = self.GameClass(randomSeed = self.randomSeed)
        return game.getTaskDescription()

    # Pack the game state into a dictionary
    def packGameState(self, actionStrTaken: str, observationStr: str,
                      numSteps: int, score: int, gameOver: bool, gameWon: bool):

        packed = {
            "actionStrTaken": actionStrTaken,
            "observationStr": observationStr,
            "numSteps": numSteps,
            "score": score,
            "gameOver": gameOver,
            "gameWon": gameWon,
            #"possibleActions": game.generatePossibleActions().keys(),
        }

        return packed

    # Run the game, using a specific series of actions
    def run(self, actionStrList:list):
        out = []
        # Initialize the game
        game = self.GameClass(randomSeed = self.randomSeed)
        game.generatePossibleActions()

        # Initial observation
        out.append(self.packGameState(actionStrTaken = "",
                                      observationStr=game.observationStr,
                                      numSteps=game.numSteps,
                                      score=game.score,
                                      gameOver=game.gameOver,
                                      gameWon=game.gameWon))

        # Run the actions in the game
        for actionStr in actionStrList:
            try:
                game.step(actionStr)
                out.append(self.packGameState(actionStrTaken=actionStr,
                                            observationStr=game.observationStr,
                                            numSteps=game.numSteps,
                                            score=game.score,
                                            gameOver=game.gameOver,
                                            gameWon=game.gameWon))
            except Exception as e:
                # Raise the error to the outer loop, causing the entire game to be skipped
                if self.error_strategy == "raise":
                    raise e

                # Skip the current action and don't add it to the output
                elif self.error_strategy == "skip":
                    continue

                # Treat the error as a failed / unimplemented action
                elif self.error_strategy == "fail":
                    out.append(self.packGameState(actionStrTaken=actionStr,
                                                  observationStr=f"ERROR: {e}",
                                                  numSteps=game.numSteps,
                                                  score=game.score,
                                                  gameOver=True,
                                                  gameWon=False))
                else:
                    raise ValueError(f"Invalid error strategy: {self.error_strategy}")

        # Also store final state
        #out.append(self.packGameState(game, ""))

        return out, game.generatePossibleActions().keys()

    # Crawl the game
    def crawl(self, maxDepth:int = 3, maxPathsToCrawl:int = 1000, maxCrawlsPerAction:int = 10, actionsSoFar:list = []):
        # Initialize the progress bar if it isn't already initialized
        if self.pbar is None:
            self.pbar = tqdm(total=maxPathsToCrawl, desc=self.tqdm_desc, file=sys.stdout)

        out = []

        # If we have reached the maximum depth, or the maximum number of paths to crawl, return
        if (maxDepth < 0) or (self.numPathsCrawled >= maxPathsToCrawl):
            return out

        # Run the game with the current actions, to get the list of possible next actions from this node
        _, possibleActions = self.run([])

        # Get the list of possible action verbs (i.e. the first token of each action string)
        #possibleActionVerbs = list(set([actionStr.split(" ")[0] for actionStr in possibleActions]))
        actionVerbCounts = {}

        # Shuffle possibleActions, so we don't keep subsampling the same random actions at each step
        # Convert possibleActions from dict_keys to list
        possibleActions = list(possibleActions)
        self.r.shuffle(possibleActions)              # This shuffle uses a random seed that's different from the one that's used to generate the game.

        # Run each of the possible actions
        for actionStr in possibleActions:
            # Get this strings action verb
            actionVerb = actionStr.split(" ")[0]

            # Increment the counter on how many times we've run this action verb
            if actionVerb not in actionVerbCounts:
                actionVerbCounts[actionVerb] = 0

            # If we've run this action verb too many times, skip it
            if actionVerbCounts[actionVerb] > maxCrawlsPerAction:
                continue

            actionVerbCounts[actionVerb] += 1

            # Run the game with the current actions, plus the new action
            actionStrList = actionsSoFar + [actionStr]
            gameStates, _ = self.run(actionStrList)

            # Append the game states to the output
            out.append(gameStates)

            self.numPathsCrawled += 1

            # If we've reached the maximum depth or the maximum number of paths to crawl, return
            if (maxDepth < 0) or (self.numPathsCrawled >= maxPathsToCrawl):
                break

            # Update the progress bar
            self.pbar.update(1)

            # Otherwise, if the game isn't over, recurse
            if (len(gameStates) > 0) and (not gameStates[-1]["gameOver"]):
                out.extend(self.crawl(maxDepth-1, maxPathsToCrawl, maxCrawlsPerAction, actionStrList))

        #print("Action verb counts: " + str(actionVerbCounts))

        return out


def extract_initial_action_token(action: str):
    '''
    Helper function to extract just the initial action token from an action string.
    For example: "put apple in fridge" --> "put"
    '''
    return action.split(" ")[0].lower()


def check_alignment(game_file, args):

    metric = {
        "score": 0,
        "error_msg": "",
        "evaluations": [],
    }

    game_name = os.path.basename(game_file)

    try:
        game_module = importlib.import_module(game_name[:-3])
    except SyntaxError as e:
        print(f"Syntax error in {game_name}")
        metric["error_msg"] = str(e)
        return metric
    except NameError as e:
        print(f"Name error in {game_name}")
        metric["error_msg"] = str(e)
        return metric

    # Create the pathcrawler
    pathcrawler = Pathcrawler(game_module.TextGame, tqdm_desc=f"Crawling paths on {game_name}",
                                error_strategy=args.error_strategy, random_seed=args.random_seed,
                                shuffle_random_seed=args.shuffle_random_seed)

    # Crawl the game
    try:
        out = pathcrawler.crawl(maxDepth=args.max_depth, maxPathsToCrawl=args.max_paths)       # Hyperparameters, can change these
    except Exception as e:
        pathcrawler.pbar.leave = False
        pathcrawler.pbar.close()
        print(f"Encountered the following error while crawling {game_name}: {e}")
        metric["error_msg"] = str(e)
        return metric

    packed = {
            "gameName": game_name,
            "gameTask": pathcrawler.getGameTaskDescription(),
            "paths": out,
        }

    game_task = packed["gameTask"]

    all_paths = packed["paths"]
    negative_response_paths = [path for path in packed["paths"] if path[-1]["observationStr"] is None or
                            any([phrase in str(path[-1]["observationStr"]).lower() for phrase in NEGATIVE_RESPONSE_PHRASES])]
    positive_response_paths = [path for path in packed["paths"] if not (path[-1]["observationStr"] is None or
                            any([phrase in str(path[-1]["observationStr"]).lower() for phrase in NEGATIVE_RESPONSE_PHRASES]))]

    paths_by_action = defaultdict(list)
    for path in packed["paths"]:
        paths_by_action[extract_initial_action_token(path[-1]["actionStrTaken"])].append(path)

    # Subsample a specified number of paths to pass to OpenAI, based on selected strategy
    sampled_paths = []

    # Sample paths evenly between those with a 'positive' and 'negative' final console response
    if args.sample_strategy == "pos_neg_even":
        sampled_paths.extend(random.sample(negative_response_paths, min(args.num_samples_per_game // 2, len(negative_response_paths))))
        sampled_paths.extend(random.sample(positive_response_paths, min(args.num_samples_per_game // 2, len(positive_response_paths))))

        num_samples_added = min(args.num_samples_per_game // 2, len(negative_response_paths)) + min(args.num_samples_per_game // 2, len(positive_response_paths))

    # Sample paths proportionally to the number of paths in each category
    elif args.sample_strategy == "pos_neg_proportional":
        num_negative_samples = int(len(negative_response_paths) / len(out["paths"]) * args.num_samples_per_game)
        num_positive_samples = int(len(positive_response_paths) / len(out["paths"]) * args.num_samples_per_game)

        sampled_paths.extend(random.sample(negative_response_paths, min(num_negative_samples, len(negative_response_paths))))
        sampled_paths.extend(random.sample(positive_response_paths, min(num_positive_samples, len(positive_response_paths))))

        num_samples_added = min(num_negative_samples, len(negative_response_paths)) + min(num_positive_samples, len(positive_response_paths))

    # Sample paths evenly between each final action (as determined by the first action token)
    elif args.sample_strategy == "action_even":
        samples_per_action = args.num_samples_per_game // len(paths_by_action)

        num_samples_added = 0
        for action, action_paths in paths_by_action.items():
            num_samples_added += min(samples_per_action, len(action_paths))
            sampled_paths.extend(random.sample(action_paths, min(samples_per_action, len(action_paths))))

    else:
        raise ValueError(f"Invalid SAMPLE_STRATEGY: {args.sample_strategy}")

    # After subsampling paths, if we failed to add enough samples, add more randomly
    # NOTE: this has the potential for sampling the same path more than once.
    if num_samples_added < args.num_samples_per_game:
        sampled_paths.extend(random.sample(all_paths, min(args.num_samples_per_game - num_samples_added, len(all_paths))))

    def _parse_response(response):
        data = []
        for json_data in response.split("\n"):
            if json_data.strip() == "":
                continue  # Skip empty lines

            data.append(json.loads(json_data))
        return data

    evaluations = []
    pbar = iter(tqdm(sampled_paths, desc="Querying OpenAI API", total=len(sampled_paths), leave=False))
    for paths in batched(pbar, args.alignment_batch_size):
        playthroughs = []
        for i, path in enumerate(paths):
            playthrough = []
            for datapoint in path:
                action = str(datapoint["actionStrTaken"]).strip()
                observation = str(datapoint["observationStr"]).strip()

                playthrough.append({"action": action, "observation": observation})

            playthroughs.append(f'{{"idx": {i}, "playthrough": {playthrough}}}')

        playthroughs_text = "\n".join(playthroughs)
        full_prompt = f"{BASE_PROMPT_ALIGNMENT}\n\nGame Task: {game_task}\n\nHere are the playthroughs to evaluate:\n{playthroughs_text}\n\n"
        full_prompt += "Evaluation:\n"

        response = stream_llm_gpt(full_prompt, model=args.alignment_model_name)
        response_data = _parse_response(response)

        idx = 0
        for data in response_data:
            if idx != data['idx']:
                print(colored(f"Warning: missing response for playthrough {idx}. Recomputing...", "yellow"))
                full_prompt = f"{BASE_PROMPT_ALIGNMENT}\n\nGame Task: {game_task}\n\nHere are the playthroughs to evaluate:\n{playthroughs[idx]}\n\n"
                full_prompt += "Evaluation:\n"
                response = stream_llm_gpt(full_prompt, model=args.alignment_model_name)
                data = _parse_response(response)
                assert idx == data['idx'], "TODO: Retry?"

            data.pop("idx")
            data["playthrough"] = eval(playthroughs[idx])["playthrough"]
            evaluations.append(data)
            idx += 1

    assert len(sampled_paths) == len(evaluations), "For some reason, we don't have the right amount of evaluations."

    metric["score"] = sum(e['evaluation'].lower().strip().startswith('yes') for e in evaluations) / len(evaluations)
    metric["evaluations"] = evaluations
    return metric

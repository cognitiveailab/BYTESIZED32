import re
import json

import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("--results", default="./results/GPT-4-32k/results.json")
args = parser.parse_args()

with open(args.results) as f:
    data = json.load(f)

# If we are missing reflections, it means a previous reflection (or the original) game worked.
# So, we copy the previous values.
for k, v in list(data.items()):
    if "_v0.py" not in k:
        continue

    for reflection in range(3+1):
        game_reflection = f"{k[:-6]}_v{reflection}.py"
        if game_reflection not in data:
            if reflection == 0:
                data[game_reflection] = v.copy()
            else:
                data[game_reflection] = data[f"{k[:-6]}_v{reflection-1}.py"].copy()

        elif data[game_reflection]["metrics"]["validity"]["error_msg"].startswith("STOP:"):
            data[game_reflection] = data[f"{k[:-6]}_v{reflection-1}.py"].copy()

def parse_game_file_name(game_file_name):
    splits = game_file_name.split("_")
    experiment = splits[1]
    test_id = splits[3]
    fold = splits[4]

    assert experiment in ('object', 'distractor', 'action')
    assert fold in ('p', 'n')
    assert test_id in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16')

    return experiment, test_id, fold

results = []
for k, v in data.items():
    v = v["metrics"]["compliance"]
    experiment, _, fold = parse_game_file_name(k)
    v["experiment"] = v["experiment"] or experiment
    v["fold"] = v["fold"] or fold
    try:
        game_name, reflection, _ = re.split(r"_v(\d+).py", k)
    except:
        game_name, reflection = k, 0
    results.append(dict(filename=k, game_name=game_name, reflection=int(reflection), **v))

results = pd.DataFrame(results)

# Change value names
values_mapping = {
    "object": "Task-critical objects",
    "action": "Task-critical actions",
    "distractor": "Distractors",
    "p": "In template",
    "n": "Not in template",
}
results = results.replace(values_mapping)

# Sort rows with experiment order being object, action, distractor
results["experiment"] = pd.Categorical(results["experiment"], ["Task-critical objects", "Task-critical actions", "Distractors"])
results = results.sort_values("experiment")

# print(results.groupby(["experiment", "fold"])["passed"].mean().round(4).unstack().to_latex(float_format="{:02.1%}".format))
# print(results.groupby(["experiment", "fold"])["passed"].mean().round(4).unstack().to_markdown())
#print(results.groupby(["experiment", "reflection"])["passed"].mean().round(4).unstack().to_latex(float_format="{:02.1%}".format))
print(results.groupby(["experiment", "reflection"])["passed"].mean().round(4).unstack().to_markdown())

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

results = []
for k, v in data.items():
    v = v["metrics"]["validity"]
    try:
        game_name, reflection, _ = re.split(r"_v(\d+).py", k)
    except:
        game_name, reflection = k, 0
    results.append(dict(filename=k, game_name=game_name, reflection=int(reflection), **v))

results = pd.DataFrame(results)

# Change columns names
columns_mapping = {
    "TextGame": "Game Initialization",
    "getTaskDescription": "Task Description Generation",
    "calculateScore": "Score Calculation",
    "generatePossibleActions": "Possible Actions Generation",
    "runnable": "Runnable Game",
}
results = results.rename(columns=columns_mapping)

# Report mean of all columns except for error_msg and filename.
# columns = ["Game Initialization", "Task Description Generation", "Score Calculation", "Possible Actions Generation", "Runnable Game"]
columns = ["Game Initialization", "Possible Actions Generation", "Runnable Game"]
# print(results.groupby(["reflection"])[columns].mean().round(4).T.to_latex(float_format="{:02.1%}".format))
print(results.groupby(["reflection"])[columns].mean().round(4).T.to_markdown())

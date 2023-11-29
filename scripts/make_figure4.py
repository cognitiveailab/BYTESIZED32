import re
import json
import argparse

import numpy as np
import pandas as pd
import plotly.express as px

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
            data[game_reflection] = data[f"{k[:-6]}_v{reflection-1}.py"].copy()

        elif data[game_reflection]["metrics"]["validity"]["error_msg"].startswith("STOP:"):
            data[game_reflection] = data[f"{k[:-6]}_v{reflection-1}.py"].copy()

results = []
for k, v in data.items():
    try:
        game_name, reflection, _ = re.split(r"_v(\d+).py", k)
    except:
        game_name, reflection = k, 0

    results.append(dict(filename=k, game_name=game_name, reflection=int(reflection), **v["metrics"]["alignment"]))

results = pd.DataFrame(results)

# Change columns names
columns_mapping = {
    "score": "Alignment Score",
}
results = results.rename(columns=columns_mapping)

# Report mean of all columns except for error_msg and filename.
columns = ["Alignment Score"]
print(results.groupby(["reflection"])[columns].mean().round(4).T.to_markdown())

scores_pre_reflection = results[results["reflection"] == 0]["Alignment Score"].values.tolist()
scores_post_reflection = results[results["reflection"] == 3]["Alignment Score"].values.tolist()

df = pd.DataFrame({
    "series": np.concatenate((["Pre-Reflection"]*len(scores_pre_reflection), ["Post-Reflection"]*len(scores_post_reflection))),
    "data":  np.concatenate((scores_pre_reflection, scores_post_reflection))
})

fig = px.histogram(df, x="data", color="series", barmode="overlay", histnorm='probability',
                   color_discrete_map={"Pre-Reflection": "red", "Post-Reflection": "blue"})
fig.update_yaxes(title_text="Proportion of games", showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_xaxes(title_text="Physical Reality Alignment Score", showline=True, linewidth=2, linecolor='black', mirror=True)

# Change the background color of the plot and the overall figure to white
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        title='',         # this removes the "Series" title
        orientation='v',  # this puts the legend items in a horizontal orientation
        yanchor="bottom", # this and next line places the legend at the top
        y=0.85,
        xanchor="right",
        x=1
    )
)

# Plot mean as scatter point (asterisks) on the top of the bars
mean_pre_reflection = np.mean(scores_pre_reflection)
mean_post_reflection = np.mean(scores_post_reflection)
fig.add_scatter(
    x=[mean_pre_reflection, mean_post_reflection],
    y=[0.2, 0.2],
    mode="markers",
    marker=dict(color=["red", "blue"], size=10, symbol="star"),
    showlegend=False
)

# Save the figure as a PDF
fig.write_image("figure4.png")
fig.show()

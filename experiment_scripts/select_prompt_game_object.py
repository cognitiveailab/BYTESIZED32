import pandas as pd
import sys

data_file = sys.argv[1]

df = pd.read_csv(data_file)
result = []
for col_name in df.keys()[1:]:
    cols = df[["Game Name", col_name]]
    na_rows = cols[cols[col_name].isna()]
    value_rows = cols[~cols[col_name].isna()]
    positive_game = value_rows.sample()["Game Name"].values[0]
    negative_game = na_rows.sample()["Game Name"].values[0]
    result.append((positive_game, negative_game))

df_out = pd.DataFrame(result)
with open("prompt_games_object.csv", "w") as f:
    df_out.to_csv(f,index=False, header=False)
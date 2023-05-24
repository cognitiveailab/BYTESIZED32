import pandas as pd
import sys

train_data_file = sys.argv[1]
test_data_file = sys.argv[2]

train_df = pd.read_csv(train_data_file)
test_df = pd.read_csv(test_data_file, header=None)

result = []
for _, row in test_df.iterrows():
    col_name = row.values[1]
    cols = train_df[["Game Name", col_name]]
    na_rows = cols[cols[col_name].isna()]
    value_rows = cols[~cols[col_name].isna()]
    positive_game = value_rows.sample()["Game Name"].values[0]
    negative_game = na_rows.sample()["Game Name"].values[0]
    result.append((positive_game, negative_game))

df_out = pd.DataFrame(result)
with open("prompt_games_action.csv", "w") as f:
    df_out.to_csv(f,index=False, header=False)
import pandas as pd
import sys

data_file = sys.argv[1]

df = pd.read_csv(data_file)

# if df has more than 3 instances, sample 3
# else select all and then sample to 3
def sample_3(df):
    if len(df.index) >= 3:
        samples = df.sample(n=3)
        sample_0 = samples["Game Name"].iloc[0]
        sample_1 = samples["Game Name"].iloc[1]
        sample_2 = samples["Game Name"].iloc[2]
    elif len(df.index) == 2:
        samples = df.sample(n=2)
        sample_0 = samples["Game Name"].iloc[0]
        sample_1 = samples["Game Name"].iloc[1]
        sample_2 = samples.sample()["Game Name"].iloc[0]
    else:
        sample_0 = df["Game Name"].iloc[0]
        sample_1 = df["Game Name"].iloc[0]
        sample_2 = df["Game Name"].iloc[0]
    return sample_0, sample_1, sample_2

result = []
for i in range(2):
    for n, col_name in enumerate(df.keys()[1:]):
        # There are only one test prompt for electrical objects and objects with state changes
        if i == 1 and n in [5,6]:
            continue
        cols = df[["Game Name", col_name]]
        na_rows = cols[cols[col_name].isna()]
        value_rows = cols[~cols[col_name].isna()]
        # 3 positive
        positive_0, positive_1, positive_2 = sample_3(value_rows)
        # 3 negative
        negative_0, negative_1, negative_2 = sample_3(na_rows)
        result.append((positive_0, positive_1, positive_2, negative_2, negative_1, negative_0))

df_out = pd.DataFrame(result)
with open("prompt_games_object_2.csv", "w") as f:
    df_out.to_csv(f,index=False, header=False)
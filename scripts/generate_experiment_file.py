import sys
import argparse
from os.path import join as pjoin

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("experiment-name", choices=["object", "action", "distractor"])
    parser.add_argument("--data", default="./data/")
    parser.add_argument("--output", help="Name of the experiment file. Default: experiment{experiment-name}.csv")
    args = parser.parse_args()
    return args


def gen_experiment_file_action(args):
    train_data_file = pjoin(args.data, f"{args.experiment_name}_train.csv")
    test_data_file = pjoin(args.data, f"{args.experiment_name}_test.csv")

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
    with open(args.output, "w") as f:
        df_out.to_csv(f, index=False, header=False)


def gen_experiment_file_distractor(args):
    train_data_file = pjoin(args.data, f"{args.experiment_name}_train.csv")
    test_data_file = pjoin(args.data, f"{args.experiment_name}_test.csv")

    train_df = pd.read_csv(train_data_file)
    test_df = pd.read_csv(test_data_file, header=None)

    result = []
    for _, row in test_df.iterrows():
        method_idx = row.values[1]
        col_name = train_df.keys()[method_idx+1]
        cols = train_df[["Game Name", col_name]]
        na_rows = cols[cols[col_name].isna()]
        value_rows = cols[~cols[col_name].isna()]
        positive_game = value_rows.sample()["Game Name"].values[0]
        negative_game = na_rows.sample()["Game Name"].values[0]
        result.append((positive_game, negative_game))

    df_out = pd.DataFrame(result)
    with open(args.output, "w") as f:
        df_out.to_csv(f, index=False, header=False)


def gen_experiment_file_object(args):
    train_data_file = pjoin(args.data, f"{args.experiment_name}_train.csv")
    test_data_file = pjoin(args.data, f"{args.experiment_name}_test.csv")

    df_train = pd.read_csv(train_data_file, header=0)
    df_test = pd.read_csv(test_data_file, header=0)

    result = []
    for _, row in df_test.iterrows():
        for key in row.keys()[1:]:
            if row[key] == 2:
                col_name = key

        cols = df_train[["Game Name", col_name]]
        na_rows = cols[cols[col_name].isna()]
        value_rows = cols[cols[col_name].isna()]
        positive_game = value_rows.sample()["Game Name"].values[0]
        negative_game = na_rows.sample()["Game Name"].values[0]
        result.append((positive_game, negative_game))

    df_out = pd.DataFrame(result)
    with open(args.output, "w") as f:
        df_out.to_csv(f, index=False, header=False)

def main():
    args = parse_args()
    args.output = args.output or f"experiment_{args.experiment_name}.csv"

    if args.experiment_name == "action":
        gen_experiment_file_action(args)
    elif args.experiment_name == "distractor":
        gen_experiment_file_distractor(args)
    elif args.experiment_name == "object":
        gen_experiment_file_object(args)


if __name__ == "__main__":
    main()

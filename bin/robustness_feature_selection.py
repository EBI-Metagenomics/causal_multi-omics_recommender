#!/usr/bin/env python3

import argparse
import random
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

start_time = time.time()

parser = argparse.ArgumentParser(description="Robustness feature selection")
parser.add_argument("-b", "best_features", required=True, help="The best features csv")
parser.add_argument("-x", "xy_file", required=True, help="XY file")
parser.add_argument(
    "-p", "phenotype_col", type=str, required=True, help="Name of the phenotype column"
)
parser.add_argument(
    "-o", "output_name", type=str, required=True, help="Output name csv file"
)
args = parser.parse_args()

# Constants
NUM_ITERATIONS = 10000
NUM_HOLDOUT_SAMPLES = 50
N_FEATURES_FOR_REGRESSION = 10

# Load the best training features
best_training_features = pd.read_csv(
    args.best_features,
    index_col=0,
)["features"].tolist()

# Load the XY data
XY = pd.read_csv(args.xy_file, index_col=0)
y = XY[args.phenotype_col]
X = XY.drop(args.phenotype_col, axis=1)

# Add random features
random_strings = [f"Random_{i}" for i in range(20)]
for random_string in random_strings:
    random_column = random.choice(XY.columns)
    shuffled_values = XY[random_column].sample(frac=1).values
    XY[random_string] = shuffled_values
    best_training_features.append(random_string)

mae_list = []
feature_combination_list = []
update_here = []

best_mae = np.inf
best_gene_set = None

for j in range(NUM_ITERATIONS):
    choose_n = random.sample(best_training_features, N_FEATURES_FOR_REGRESSION)
    X_only_n = X[choose_n]
    holdout_sample_mae_list = []
    update = 0
    for k in range(NUM_HOLDOUT_SAMPLES):
        X_train, X_test, y_train, y_test = train_test_split(X_only_n, y, test_size=0.33)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        holdout_sample_mae_list.append(mae)
    mean_mae = np.mean(holdout_sample_mae_list)

    if mean_mae < best_mae:
        best_mae = mean_mae
        update = 1
        best_gene_set = choose_n

    update_here.append(update)
    mae_list.append(mean_mae)
    feature_combination_list.append(choose_n)

print(f"End step 3. Best score {best_mae:.4f} with genes:")
for gene in best_gene_set:
    print(gene)

result_df = pd.DataFrame()
result_df["MAE"] = mae_list
result_df["Features"] = feature_combination_list
result_df["Update"] = update_here
result_df.to_csv(f"{args.output}_unsorted.csv")

result_df.sort_values(by="MAE", inplace=True, ascending=False)
result_df.reset_index(drop=True, inplace=True)
result_df.to_csv(f"{args.output}_sorted.csv")

end_time = time.time()
elapsed_time = np.round((end_time - start_time) / 60, 2)
print(f"Program ran in: {elapsed_time} minutes")

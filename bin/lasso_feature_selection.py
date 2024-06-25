#!/usr/bin/env python3

import argparse
import sys
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split

start_time = time.time()

NUM_ITERATIONS = 2  # 50

parser = argparse.ArgumentParser(
    description="Select the best features using Lasso regression"
)
parser.add_argument(
    "-a", "--alpha-mae", help="Alpha mae lasso regression parquet file."
)
parser.add_argument("-x", "--xy-file", help="XY file")
parser.add_argument(
    "-p", "--phenotype-col", type=str, help="Name of the phenotype column"
)
parser.add_argument("-o", "--output", help="Output csv file")
args = parser.parse_args()


# Load the alpha-MAE dataframe
alpha_mae = pd.read_parquet(args.alpha_mae)

# Find the best alpha
error_low = []
error_high = []
min_mae = np.inf
best_alpha = None
best_alpha_stdev = None
for index, row in alpha_mae.iterrows():
    cv = row["all_maes"]
    error_low.append(np.percentile(cv, 5))
    error_high.append(np.percentile(cv, 95))
    mean_mae = row["mae_list"]
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_alpha = row["alphas"]
        best_alpha_stdev = np.std(cv)

best_alpha_plus_std = min_mae + best_alpha_stdev

# Choose the best alpha
chosen_alpha_df = alpha_mae[alpha_mae["mae_list"] < best_alpha_plus_std]
chosen_alpha_df = chosen_alpha_df[chosen_alpha_df["alphas"] > best_alpha]
chosen_alpha_df.sort_values(by="mae_list", inplace=True)

if chosen_alpha_df.empty:
    # TODO: improve error message
    print("The filtered db is empty.", file=sys.stderr)
    sys.exit(1)

chosen_alpha = chosen_alpha_df["alphas"].iloc[0]

# Load the XY data
XY = pd.read_csv(args.xy_file, index_col=0)
y = XY[args.phenotype_col]
X = XY.drop(args.phenotype_col, axis=1)

# Find the non-zero coefficients
nonzero_coefs = set()
for i in range(NUM_ITERATIONS):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    model = Lasso(alpha=chosen_alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    coefs = model.coef_
    col_list = []
    for col, coef in zip(X.columns, coefs):
        if coef != 0:
            col_list.append(col)
    nonzero_coefs = nonzero_coefs.union(set(col_list))

# Save the best features
new_best_features = pd.DataFrame()
new_best_features["features"] = list(nonzero_coefs)
new_best_features.to_csv(args.output)

print(f"Finished step 2. {len(nonzero_coefs)} features remain.")

end_time = time.time()
elapsed_time = np.round((end_time - start_time) / 60, 2)
print(f"Program ran in: {elapsed_time} minutes")

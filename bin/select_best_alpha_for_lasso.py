#!/usr/bin/env python3

import argparse
import time

import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

start_time = time.time()

parser = argparse.ArgumentParser(
    description="Select the best alpha for Lasso regression"
)
parser.add_argument("-x", "xy_file", type=str, help="Path to the XY file")
parser.add_argument(
    "-p", "phenotype_col", type=str, help="Name of the phenotype column"
)
parser.add_argument("-l", "alpha_low", type=float, help="Lower bound for alpha")
parser.add_argument("-t", "alpha_high", type=float, help="Upper bound for alpha")
parser.add_argument("-o", "output", help="Output csv file")

args = parser.parse_args()

NUM_ITERATIONS = 50

XY = pd.read_csv(args.xy_file, index_col=0)
y = XY[args.phenotype_col]
X = XY.drop(args.phenotype_col, axis=1)

alphas = np.linspace(args.alpha_low, args.alpha_high, num=100)

rsquared_list = []
mae_list = []
all_cv_maes_for_alpha = []
top_10_coeffs = []
num_repeated_holdout_samples = NUM_ITERATIONS
for alpha in alphas:
    holdout_sample_mae_list = []
    holdout_sample_r2_list = []
    for i in range(num_repeated_holdout_samples):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        model = Lasso(alpha=alpha)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        holdout_sample_r2_list.append(r2_score(y_test, y_pred))
        holdout_sample_mae_list.append(mean_absolute_error(y_test, y_pred))
    rsquared_list.append(np.mean(holdout_sample_r2_list))
    mae_list.append(np.mean(holdout_sample_mae_list))
    all_cv_maes_for_alpha.append(holdout_sample_mae_list)

alpha_mae_df = pd.DataFrame()
alpha_mae_df["alphas"] = alphas
alpha_mae_df["mae_list"] = mae_list
alpha_mae_df["rsquared"] = rsquared_list
alpha_mae_df["all_maes"] = all_cv_maes_for_alpha
alpha_mae_df.to_csv(f"alpha_mae_df_{args.output_id}.csv")

end_time = time.time()
elapsed_time = (end_time - start_time) / 60
print(f"Program ran in: {elapsed_time} minutes")

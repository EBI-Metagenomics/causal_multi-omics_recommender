import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from  sklearn.metrics import mean_absolute_error, r2_score
import os
import sys

ROOT = sys.argv[1]
XY_FILE = sys.argv[2]
PHENOTYPE_COL = sys.argv[3]
OUTPUT_ID = sys.argv[4]

NUM_ITERATIONS = 50

XY = pd.read_csv( ROOT + os.sep + "data" + os.sep + XY_FILE, index_col=0)
y = XY[PHENOTYPE_COL]
X = XY.drop(PHENOTYPE_COL, axis=1)

alphas = np.linspace(0.01, 1, num=100)

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
        # # Uncomment to view regular outputs
        # if i % 10 == 0:
        #     print(mean_absolute_error(y_test, y_pred))
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
alpha_mae_df.to_csv(ROOT + os.sep + f"data/alpha_mae_df_{OUTPUT_ID}.csv")

# Uncomment to plot
# plt.scatter(x=alphas, y= mae_list)
# plt.xlabel("Alpha")
# plt.ylabel("MAE")
# plt.savefig(ROOT + os.sep + f"figures/alpha_vs_mae_{OUTPUT_ID}.png")
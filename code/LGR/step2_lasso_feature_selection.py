import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import numpy as np
import sys
import os
import ast
import time
start_time = time.time()

"""

Example usage: python step3_robustness_feature_selection.py ../.. transcriptome_XY.csv gutted.weight.kg 1 salmon_data

"""

id = sys.argv[1]
ROOT = sys.argv[1] #"../.." #
XY_FILE = sys.argv[2]#f"magnet_dataset_x_positions_{id}.csv" # 
PHENOTYPE_COL = sys.argv[3]#"phenotype" #"gutted.weight.kg" #sys.argv[3]
OUTPUT_ID = sys.argv[4]#f"{id}" # sys.argv[4]
SUBFOLDER = sys.argv[5]#"magnets_20k_features_300_samples_v18may_v2"#"#"transcriptome_with_random" #sys.argv[5]

NUM_ITERATIONS = 50

alpha_mae = pd.read_csv(ROOT + os.sep + f"data/{SUBFOLDER}/alpha_mae_df_{OUTPUT_ID}.csv")

error_low = []
error_high = []
min_mae = np.inf
best_alpha = None
best_alpha_stdev = None
for index, row in alpha_mae.iterrows():
    cv =  ast.literal_eval(row["all_maes"])
    error_low.append(np.percentile(cv, 5))
    error_high.append(np.percentile(cv, 95))
    mean_mae = row["mae_list"]
    if mean_mae < min_mae:
        min_mae = mean_mae
        best_alpha = row["alphas"]
        best_alpha_stdev = np.std(cv)

best_alpha_plus_std = min_mae + best_alpha_stdev

chosen_alpha_df = alpha_mae[alpha_mae["mae_list"] < best_alpha_plus_std]
chosen_alpha_df = chosen_alpha_df[chosen_alpha_df["alphas"] > best_alpha]
chosen_alpha_df.sort_values(by="mae_list", inplace=True)
chosen_alpha = chosen_alpha_df["alphas"].iloc[0]

XY = pd.read_csv( ROOT + os.sep + "data"+ os.sep + SUBFOLDER + os.sep + XY_FILE, index_col=0)
y = XY[PHENOTYPE_COL]
X = XY.drop(PHENOTYPE_COL, axis=1)

nonzero_coefs = set()

for i in range(NUM_ITERATIONS):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    model = Lasso(alpha=chosen_alpha)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    coefs = model.coef_
    col_list = []
    coef_list = []
    i = 0
    for col in X.columns:
        coef = coefs[i]
        i+=1
        if coef != 0:
            coef_list.append(coef)
            # if ALT_PHENO != 2:
            #     col_list.append(col[1]) # TODO change here
            # else:
            col_list.append(col)

    nonzero_coefs = nonzero_coefs.union(set(col_list))

new_best_features = pd.DataFrame()
new_best_features["features"] = list(nonzero_coefs)
new_best_features.to_csv(ROOT + os.sep + f"data/{SUBFOLDER}/best_features_{OUTPUT_ID}.csv")

print(f"Finished step 2. {len(nonzero_coefs)} features remain.")

end_time = time.time()
elapsed_time = np.round((end_time - start_time)/60, 2)
print(f"Program ran in: {elapsed_time} minutes")

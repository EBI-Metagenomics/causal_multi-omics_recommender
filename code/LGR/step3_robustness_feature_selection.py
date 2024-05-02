import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
from  sklearn.metrics import mean_absolute_error
import sys
import os

"""
This project received funding from the European Union’s Horizon 2020 research and innovation programme [952914] (FindingPheno).
"""

ROOT = sys.argv[1]
XY_FILE = sys.argv[2]
PHENOTYPE_COL = sys.argv[3]
OUTPUT_ID = sys.argv[4]

NUM_ITERATIONS = 1000 # 10000
NUM_HOLDOUT_SAMPLES = 10
n_features_for_regression = 10

best_training_features = pd.read_csv(ROOT + os.sep + f"data/best_features_{OUTPUT_ID}.csv", index_col=0)

XY = pd.read_csv( ROOT + os.sep + "data" + os.sep + XY_FILE, index_col=0)
y = XY[PHENOTYPE_COL]
X = XY.drop(PHENOTYPE_COL, axis=1)

mae_list = []
feature_combination_list = []
update_here = []

best_mae = np.inf
best_gene_set = None

# print("Start search")
for j in range(NUM_ITERATIONS):
    choose_n = best_training_features.sample(n=n_features_for_regression).values.flatten()
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

    ## Uncomment to monitor progress
    if mean_mae < best_mae:
        # print(mean_mae)
        best_mae = mean_mae
        update = 1
        best_gene_set = choose_n
    # if j % 1000 == 0:
    #     print(j)
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
result_df.to_csv(ROOT + os.sep + f"data/result_unsorted_{OUTPUT_ID}.csv")
result_df.sort_values(by="MAE", inplace=True, ascending=False)
result_df.reset_index(drop=True, inplace=True)
result_df.to_csv(ROOT + os.sep + f"data/result_sorted_{OUTPUT_ID}.csv")
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

ROOT =  "../.." # sys.argv[1] # ".." 
OUTPUT_ID = "1" # sys.argv[2] # "1" 
ALT_PHENO =  0 # sys.argv[3] # 0 if no, 1 if yes
NUM_ITERATIONS = 300 # 10000
NUM_HOLDOUT_SAMPLES = 10
n_features_for_regression = 15

best_training_features = pd.read_csv(ROOT + os.sep + f"data/best_features_altpheno_{ALT_PHENO}_{OUTPUT_ID}.csv", index_col=0)
df = pd.read_csv(ROOT + os.sep + "data/processed/all_chromosomes.csv", index_col=0)

# Pivot the DataFrame
pivoted_df = df.pivot_table(index='sample.id', columns='gene', values=["gene.expression"],  aggfunc='mean')
X = pivoted_df

# Pivot the DataFrame
pivoted_df = df.pivot_table(index='sample.id', values=["gutted.weight.kg"],  aggfunc='mean')
y = pivoted_df

if ALT_PHENO == 1:
    metabolome_pheno = pd.read_csv(ROOT + os.sep + "data/processed/metabolome_pca.csv", index_col=0)
    y = metabolome_pheno["principal component 1"]
    X.columns = X.columns.droplevel(0)
    XY = pd.merge(left=X, right=y, left_on=X.index, right_on=y.index)
    XY.index = XY["key_0"]
    X = XY.drop(["principal component 1", "key_0"], axis=1)
    y = XY["principal component 1"]
elif ALT_PHENO == 2:
    metadata = pd.read_csv("../../data/raw/HoloFish_FishVariables_20221116.csv")
    y = metadata[["Sample.ID", "Tapeworm.index"]]
    y.index = y["Sample.ID"]
    y.drop("Sample.ID", axis=1, inplace=True)
    X.columns = X.columns.droplevel(0)
    XY = pd.merge(left=X, right=y, left_on=X.index, right_on=y.index)
    XY.index = XY["key_0"]
    X = XY.drop(["Tapeworm.index", "key_0"], axis=1)
    y = XY["Tapeworm.index"]

mae_list = []
feature_combination_list = []
update_here = []

best_mae = np.inf
best_gene_set = None

# print("Start search")
for j in range(NUM_ITERATIONS):
    choose_n = best_training_features.sample(n=n_features_for_regression).values.flatten()
    if ALT_PHENO != 2:
        X_only_n = X["gene.expression"][choose_n]
    else:
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
result_df.to_csv(ROOT + os.sep + f"data/result_unsorted_{ALT_PHENO}_{OUTPUT_ID}.csv")
result_df.sort_values(by="MAE", inplace=True, ascending=False)
result_df.reset_index(drop=True, inplace=True)
result_df.to_csv(ROOT + os.sep + f"data/result_sorted_{ALT_PHENO}_{OUTPUT_ID}.csv")
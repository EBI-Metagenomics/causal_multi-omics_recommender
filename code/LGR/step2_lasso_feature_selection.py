import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import numpy as np
import sys
import os

ROOT =  "../.." # sys.argv[1] # ".." 
OUTPUT_ID = "1" # sys.argv[2] # "1" 
ALT_PHENO =  0 # sys.argv[3] # 0 if no, 1 if yes
NUM_ITERATIONS = 10

df = pd.read_csv(ROOT + os.sep + "data/processed/all_chromosomes.csv", index_col=0)

alpha_mae = pd.read_csv(ROOT + os.sep + f"data/alpha_mae_altpheno_{ALT_PHENO}_df_{OUTPUT_ID}.csv")
alpha_mae_sorted = alpha_mae.sort_values(by="mae_list")
alpha_min = alpha_mae_sorted.iloc[0]["alphas"]
alpha_mae_arr = alpha_mae["mae_list"].values
alpha_std = np.std(alpha_mae_arr)

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

nonzero_coefs = set()

for i in range(NUM_ITERATIONS):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
    model = Lasso(alpha=alpha_min+alpha_std) #TODO there is probably a better way to select alpha
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
            if ALT_PHENO != 2:
                col_list.append(col[1]) # TODO change here
            else:
                col_list.append(col)

    nonzero_coefs = nonzero_coefs.union(set(col_list))

new_best_features = pd.DataFrame()
new_best_features["features"] = list(nonzero_coefs)
new_best_features.to_csv(ROOT + os.sep + f"data/best_features_altpheno_{ALT_PHENO}_{OUTPUT_ID}.csv")

print(f"Finished step 2. {len(nonzero_coefs)} features remain.")

import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from  sklearn.metrics import mean_absolute_error, r2_score
import os
import sys

"""
This project received funding from the European Union’s Horizon 2020 research and innovation programme [952914] (FindingPheno).
"""

ROOT = "../.." #sys.argv[1] # ".." 
OUTPUT_ID = "1" #sys.argv[2] # "1" 
ALT_PHENO = "4" # sys.argv[3] # 0 if no, 1 if yes
NUM_ITERATIONS = 20 # make this smaller for quick debugging
NUM_ALPHAS = 100

directory_names = [ROOT + os.sep + f"figures"]
for directory_name in directory_names:
    # Check if the directory exists
    if not os.path.exists(directory_name):
        # Create the directory if it doesn't exist
        os.makedirs(directory_name)

if ALT_PHENO == 0:
    # Pivot the DataFrame
    df = pd.read_csv(ROOT + os.sep + "data/processed/all_chromosomes.csv", index_col=0)
    pivoted_df = df.pivot_table(index='sample.id', columns='gene', values=["gene.expression"],  aggfunc='mean')
    X = pivoted_df

    # Pivot the DataFrame
    pivoted_df = df.pivot_table(index='sample.id', values=["gutted.weight.kg"],  aggfunc='mean')
    y = pivoted_df

elif ALT_PHENO == 1:
    df = pd.read_csv(ROOT + os.sep + "data/processed/all_chromosomes.csv", index_col=0)
    pivoted_df = df.pivot_table(index='sample.id', columns='gene', values=["gene.expression"],  aggfunc='mean')
    X = pivoted_df
    metabolome_pheno = pd.read_csv(ROOT + os.sep + "data/processed/metabolome_pca.csv", index_col=0)
    y = metabolome_pheno["principal component 1"]
    X.columns = X.columns.droplevel(0)
    XY = pd.merge(left=X, right=y, left_on=X.index, right_on=y.index)
    XY.index = XY["key_0"]
    X = XY.drop(["principal component 1", "key_0"], axis=1)
    y = XY["principal component 1"]

elif ALT_PHENO == 2:
    df = pd.read_csv(ROOT + os.sep + "data/processed/all_chromosomes.csv", index_col=0)
    pivoted_df = df.pivot_table(index='sample.id', columns='gene', values=["gene.expression"],  aggfunc='mean')
    X = pivoted_df
    metadata = pd.read_csv("../../data/raw/HoloFish_FishVariables_20221116.csv")
    y = metadata[["Sample.ID", "Tapeworm.index"]]
    y.index = y["Sample.ID"]
    y.drop("Sample.ID", axis=1, inplace=True)
    X.columns = X.columns.droplevel(0)
    XY = pd.merge(left=X, right=y, left_on=X.index, right_on=y.index)
    XY.index = XY["key_0"]
    X = XY.drop(["Tapeworm.index", "key_0"], axis=1)
    y = XY["Tapeworm.index"]
elif ALT_PHENO == "3":
    #XY = pd.read_csv("../../data/magnet_dataset_7_april.csv", index_col=0)
    XY = pd.read_csv("../../data/magnet_dataset_21_apr_v7.csv", index_col=0)
    y = XY["phenotype"]
    X = XY.drop("phenotype", axis=1)
elif ALT_PHENO == "4":
    XY = pd.read_csv("../../data/scaled_salmon_holofood_dataset.csv", index_col=0)
    print(XY)
    y = XY["Salmon gutted weight---SAMPLE"]
    print(y)
    X = XY.drop("Salmon gutted weight---SAMPLE", axis=1)
    print(X)
else:
    raise NotImplementedError

alphas = np.linspace(0.01, 1, num=NUM_ALPHAS) # TODO would be better to do logspace or something that explores lower numbers more

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
alpha_mae_df.to_csv(ROOT + os.sep + f"data/alpha_mae_altpheno_{ALT_PHENO}_df_{OUTPUT_ID}.csv")

# Uncomment to plot
plt.scatter(x=alphas, y= mae_list)
plt.xlabel("Alpha")
plt.ylabel("MAE")
plt.savefig(ROOT + os.sep + f"figures/alpha_vs_mae_altpheno_{ALT_PHENO}_{OUTPUT_ID}.png")

print("Finished step 1")
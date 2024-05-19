from scipy.stats import mannwhitneyu
import sys
import pandas as pd
import os
from multiprocessing import Pool

"""
 Example usage: python run_GFGWA_on_XY.py ../.. magnet_dataset_polarisation_1.csv phenotype 1 magnets_20k_features_300_samples
"""

ROOT = sys.argv[1]
XY_FILE = sys.argv[2]
PHENOTYPE_COL = sys.argv[3]
OUTPUT_ID = sys.argv[4]
SUBFOLDER_ID = sys.argv[5]

XY = pd.read_csv( ROOT + os.sep + "data" + os.sep + SUBFOLDER_ID + os.sep + XY_FILE, index_col=0)
y = XY[PHENOTYPE_COL]
X = XY.drop(PHENOTYPE_COL, axis=1)

def calculate_pval(feature):
    feature_col = X[feature]
    feature_col = feature_col > 0.5

    groupA = y[feature_col]
    groupB = y[~feature_col]

    _,pg = mannwhitneyu( groupA,groupB, alternative="greater" )
    _,pl = mannwhitneyu( groupA,groupB, alternative="less" )
    return min(pg, pl) * 2 # multiply by two for two-sided result

with Pool(10) as p:
    minpval_list = p.map(calculate_pval, list(X.columns))


# minpval_list = []
# for feature in X.columns:
#     feature_col = X[feature]
#     feature_col = feature_col > 0.5

#     groupA = y[feature_col]
#     groupB = y[~feature_col]

#     _,pg = mannwhitneyu( groupA,groupB, alternative="greater" )
#     _,pl = mannwhitneyu( groupA,groupB, alternative="less" )
#     minpval_list.append(min(pg, pl))

result_df = pd.DataFrame()
result_df["Feature"] = list(X.columns)
result_df["p-value"] = minpval_list
result_df.sort_values(by="p-value", inplace=True)
result_df.to_csv(ROOT + os.sep + "data" + os.sep + SUBFOLDER_ID + os.sep + f"GFGWA_{OUTPUT_ID}.csv")
print(result_df.head(10))
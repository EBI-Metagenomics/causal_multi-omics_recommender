from scipy.stats import mannwhitneyu
import sys
import pandas as pd
import os

ROOT = sys.argv[1]
XY_FILE = sys.argv[2]
PHENOTYPE_COL = sys.argv[3]
OUTPUT_ID = sys.argv[4]

XY = pd.read_csv( ROOT + os.sep + "data" + os.sep + XY_FILE, index_col=0)
y = XY[PHENOTYPE_COL]
X = XY.drop(PHENOTYPE_COL, axis=1)

minpval_list = []
for feature in X.columns:
    feature_col = X[feature]
    feature_col = feature_col > 0

    groupA = y[feature_col]
    groupB = y[~feature_col]
    #print(groupA.shape, groupB.shape)

    _,pg = mannwhitneyu( groupA,groupB, alternative="greater" )
    _,pl = mannwhitneyu( groupA,groupB, alternative="less" )
    minpval_list.append(min(pg, pl))

result_df = pd.DataFrame()
result_df["Feature"] = list(X.columns)
result_df["Minimum p-value"] = minpval_list
result_df.sort_values(by="Minimum p-value", inplace=True)
print(result_df.head(10))
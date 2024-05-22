import pandas as pd
import re
import sys
import numpy as np
import os
import time
start_time = time.time()

"""

Example usage: python step4_aggregate_MAEs.py ../.. 1 salmon_data

"""

ROOT = sys.argv[1]
OUTPUT_ID = sys.argv[2]
SUBFOLDER = sys.argv[3] #"magnets_20k_features_300_samples_v18may_v2"#"transcriptome_with_random" #sys.argv[5]

df = pd.read_csv(ROOT + os.sep + f"data/{SUBFOLDER}/result_unsorted_{OUTPUT_ID}_lgb.csv", index_col=0)

def extract_list(input_string):
    extracted_strings = re.findall(r"'(.*?)'", input_string)
    return extracted_strings

all_genes = pd.read_csv(ROOT + os.sep + f"data/{SUBFOLDER}/best_features_{OUTPUT_ID}.csv", index_col=0)
all_genes = list(all_genes["features"].values)

for i in range(20):
    all_genes.append(f"Random_{i}")

ave_mae_list = []
covered_genes = []
for gene in all_genes:
    focal_gene = gene
    focal_gene_count = 0
    mae_sum = 0
    for index, row in df.iterrows():
        features = extract_list(row["Features"])
        mae = row["MAE"]
        if focal_gene in features:
            focal_gene_count += 1
            mae_sum += mae

    if focal_gene_count > 0:
        average_mae = mae_sum/focal_gene_count
        ave_mae_list.append(average_mae)
        covered_genes.append(focal_gene)
    else:
        print(f"Gene {focal_gene} not covered")

result_df = pd.DataFrame()
result_df["Gene"] = covered_genes
result_df["ave_MAE"] = ave_mae_list
result_df.to_csv(ROOT + os.sep + f"data/{SUBFOLDER}/results_ave_mae_{OUTPUT_ID}_lgb.csv")

end_time = time.time()
elapsed_time = np.round((end_time - start_time)/60, 2)
print(f"Program ran in: {elapsed_time} minutes")
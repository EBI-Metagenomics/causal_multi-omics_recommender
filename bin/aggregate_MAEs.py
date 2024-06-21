#!/usr/bin/env python3

import argparse
import pandas as pd
import re
import numpy as np
import time

start_time = time.time()

parser = argparse.ArgumentParser(description="Aggregate MAEs")
parser.add_argument("-r", "results_unsorted_lgb", required=True, help="")
parser.add_argument("-b", "best_features", required=True, help="The best features csv")
parser.add_argument(
    "-o", "output_name", type=str, required=True, help="Output name csv file"
)
args = parser.parse_args()

# Load the data
# f"result_unsorted_{args.output_id}_lgb.csv"
df = pd.read_csv(args.results_unsorted_lgb, index_col=0)


def extract_list(input_string):
    extracted_strings = re.findall(r"'(.*?)'", input_string)
    return extracted_strings


# Load the best features
# f"best_features_{args.output_id}.csv"
all_genes = pd.read_csv(args.best_features, index_col=0)
all_genes = list(all_genes["features"].values)

# Add random features
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
        average_mae = mae_sum / focal_gene_count
        ave_mae_list.append(average_mae)
        covered_genes.append(focal_gene)
    else:
        print(f"Gene {focal_gene} not covered")

result_df = pd.DataFrame()
result_df["Gene"] = covered_genes
result_df["ave_MAE"] = ave_mae_list
# "results_ave_mae_{args.output_id}_lgb.csv" #
result_df.to_csv(args.output)

end_time = time.time()
elapsed_time = np.round((end_time - start_time) / 60, 2)
print(f"Program ran in: {elapsed_time} minutes")

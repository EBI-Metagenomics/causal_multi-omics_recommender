import subprocess
import sys

data_id = sys.argv[1]

scripts_with_args = [
    ("step1_select_best_alpha_for_lasso.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", f"_{data_id}", "magnets_20k_10_runs"]),
    ("step2_lasso_feature_selection.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", f"_{data_id}", "magnets_20k_10_runs"]),
    ("step3_robustness_feature_selection.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", f"_{data_id}", "magnets_20k_10_runs"]),
    ("step4_aggregate_MAEs.py", ["../..", f"_{data_id}", "magnets_20k_10_runs"])

]

i = 0
for script, args in scripts_with_args:
    print(f"Running {script}")
    subprocess.run(["python", script] + args, check=True)
    print(f"Finished {script}")
    i += 1

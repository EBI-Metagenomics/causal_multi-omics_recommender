import subprocess

# List of commands with their arguments
scripts_with_args = [
    ("step1_select_best_alpha_for_lasso.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", "magnet"]),
    ("step2_lasso_feature_selection.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", "magnet"]),
    ("step3_robustness_feature_selection.py", ["../..", "magnet_dataset_x_positions.csv", "phenotype", "magnet"]),
    ("step4_aggregate_MAEs.py", ["../..", "magnet"])

]

    # ["step3_robustness_feature_selection.py", "../..", "magnet_dataset_x_positions.csv", "phenotype", "magnet"],
    # ["step4_aggregate_MAEs.py", "../..", "magnet"]

i = 0
for script, args in scripts_with_args:
    print(f"Running {script}")
    subprocess.run(["python", script] + args, check=True)
    print(f"Finished {script}")
    i += 1

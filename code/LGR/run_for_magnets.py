import subprocess

# List of commands with their arguments
commands = [
    ["python", "step1_select_best_alpha_for_lasso.py", "../..", "1", "3"],
    ["python", "step2_lasso_feature_selection.py", "../..", "1", "3"],
    ["python", "step3_robustness_feature_selection.py", "../..", "1", "3"],
    ["python", "step4_aggregate_MAEs.py", "../..", "1", "3"]
]

# Run subprocesses
processes = []
for command in commands:
    processes.append(subprocess.Popen(command))

# Wait for all processes to finish
for process in processes:
    process.wait()

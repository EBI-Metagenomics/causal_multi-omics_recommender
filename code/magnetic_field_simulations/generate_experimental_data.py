import matplotlib.pyplot as plt
import numpy as np
import magpylib as magpy
import random
import pandas as pd
import sys
import time

start_time = time.time()

output_id = sys.argv[1]
num_samples = sys.argv[2]

output_folder = f"magnets_20k_features_{num_samples}_samples"

number_causal_genes = 5
number_total_genes = 20000

# Choose positions of causal genes
magnet_positions = [random.randint(0, number_total_genes) for _ in range(number_causal_genes)]
magnet_positions_df = pd.DataFrame(magnet_positions)
magnet_positions_df.to_csv(f"../../data/{output_folder}/magnet_positions_run_{output_id}.csv")
print("List of positions:", magnet_positions)

# Initialise magnets
pol = 2
size = 1
cube1 = magpy.magnet.Cuboid(polarization=(pol, 0, 0), dimension=(size, size, 1))
cube2 = magpy.magnet.Cuboid(polarization=(pol, 0, 0), dimension=(size, size, 1))
cube3 = magpy.magnet.Cuboid(polarization=(pol, 0, 0), dimension=(size, size, 1))
cube4 = magpy.magnet.Cuboid(polarization=(pol, 0, 0), dimension=(size, size, 1))
cube5 = magpy.magnet.Cuboid(polarization=(pol, 0, 0), dimension=(size, size, 1))
magnets_list = [cube1, cube2, cube3, cube4, cube5]

magnets_used = 0
duds_list = []
for i in range(number_total_genes):
    y_pos = i
    # Choose a strength (nearness to dashed line)
    x_pos = random.randint(-40, 0)
    if i in magnet_positions:
        # Update position of magnet
        magnets_list[magnets_used].position = (x_pos,y_pos,0)
        magnets_used += 1
    else:
        # Make a dud
        duds_list.append([x_pos,y_pos])

zero_threshold = 0.0001

col_titles = ["Feature_" + str(i) for i in range(number_total_genes)]
col_titles.append("phenotype")

coll_exp = magpy.Collection(magnets_list, override_parent=True)



polarisation_levels = [0.5,1,2]
polarisation_probabilities = [0.6487, 0.3115, 0.0397] # taken from experimental data

NUM_SAMPLES = num_samples
data_df = pd.DataFrame()
polarisation_df = pd.DataFrame()

for j in range(NUM_SAMPLES):

    magnets_used = 0
    duds_list = []
    overall_list = [] # List does not discriminate between magnet and dud
    polarisation_list = []
    for i in range(number_total_genes):
        y_pos = i
        # Choose a strength (nearness to dashed line)
        x_pos = np.random.uniform(-40,5)
        pol =  random.choices(polarisation_levels, weights=polarisation_probabilities, k=1)[0],0,0 #(random.randint(0,2),0,0)
        if i in magnet_positions:
            # Update position of magnet
            magnets_list[magnets_used].position = (x_pos,y_pos,0)
            magnets_list[magnets_used].polarization = pol
            magnets_used += 1
        else:
            # Make a dud
            duds_list.append([x_pos,y_pos])
        overall_list.append(x_pos)
        polarisation_list.append(pol[0])
    
    # Create an observer grid in the xz-symmetry plane
    X, Y = np.mgrid[-50:50:1000j, 0:number_total_genes:1000j].transpose((0, 2, 1))
    grid = np.stack([X, Y, np.zeros((1000, 1000))], axis=2)

    H = coll_exp.getH(grid)

    phenotype =  np.mean(H[:,700,0])
    overall_list.append(phenotype)
    polarisation_list.append(phenotype)

    data_df = pd.concat([data_df, pd.DataFrame(overall_list).T])
    polarisation_df = pd.concat([polarisation_df, pd.DataFrame(polarisation_list).T])
    print(j, phenotype)

data_df_renames = data_df.rename(columns=dict(zip(data_df.columns, col_titles)))
data_df_renames = data_df_renames.reset_index(drop=True)
data_df_renames.to_csv(f"../../data/{output_folder}/magnet_dataset_x_positions_{output_id}.csv")

polarisation_df_renames = polarisation_df.rename(columns=dict(zip(polarisation_df.columns, col_titles)))
polarisation_df_renames = polarisation_df_renames.reset_index(drop=True)
polarisation_df_renames.to_csv(f"../../data/{output_folder}/magnet_dataset_polarisation_{output_id}.csv")

end_time = time.time()
elapsed_time = (end_time - start_time)/60
print(f"Program ran in: {elapsed_time} minutes")
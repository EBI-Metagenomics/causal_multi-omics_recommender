import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

ROOT =  sys.argv[1] # ".." 
OUTPUT_ID = sys.argv[2] # "1"
ALT_PHENO = sys.argv[3] 

"""
This project received funding from the European Union’s Horizon 2020 research and innovation programme [952914] (FindingPheno).
"""

df = pd.read_csv(ROOT + f"/data/results_ave_mae_{OUTPUT_ID}.csv", index_col=0)
df.sort_values(by="ave_MAE", inplace=True)

print(df.head())

plt.scatter(x= np.linspace(0, len(df), len(df)),   y = df["ave_MAE"])
plt.show()
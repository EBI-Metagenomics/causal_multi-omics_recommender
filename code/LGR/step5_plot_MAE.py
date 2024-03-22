import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

"""
This project received funding from the European Union’s Horizon 2020 research and innovation programme [952914] (FindingPheno).
"""

df = pd.read_csv("results_ave_mae.csv", index_col=0)
df.sort_values(by="ave_MAE", inplace=True)
df.head(10).reset_index(drop=True)
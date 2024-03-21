import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("results_ave_mae.csv", index_col=0)
df.sort_values(by="ave_MAE", inplace=True)
df.head(10).reset_index(drop=True)
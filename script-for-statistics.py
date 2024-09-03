import numpy as np
from scipy import stats
import pandas as pd

existing_file = "comparison-results/result-active.xlsx"
df = pd.read_excel(existing_file, header=[0,1])
df_without_rows = df.drop(df.index[0:len(df)//2])
df_without_columns = df_without_rows.drop(df_without_rows.columns[0:len(df)//2], axis=1)
df = df_without_columns
print(df)




# colors = [(1, 1, 1), (0, 1, 0), (0, 0, 1), (1, 0, 0)] # white, green, blue, red
# values = [0, 1, 2, 3]
# cmap = mcolors.LinearSegmentedColormap.from_list("Custom", colors, N=256)

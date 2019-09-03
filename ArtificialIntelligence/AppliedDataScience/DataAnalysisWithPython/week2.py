#### week 2 ####
import pandas as pd
import numpy as np

np.nan
df = pd.DataFrame()
df.rename(column={"original": "rename"}, inplace=True)

# Normalization: z-score
df["length"] = (df["length"] - df["length"].mean)/df["length"].std()
df["height"] = df["height"]/df["height"].max()

# Categorical Var to Numerical Value: one-hot encoding
pd.get_dummies(df["fuel"])

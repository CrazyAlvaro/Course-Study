#### week 1 ####
import pandas as pd
import numpy as np
df = pd.DataFrame()
df = pd.read_csv("file_name", names=["header1", "header2"])
df.describe(include="all")

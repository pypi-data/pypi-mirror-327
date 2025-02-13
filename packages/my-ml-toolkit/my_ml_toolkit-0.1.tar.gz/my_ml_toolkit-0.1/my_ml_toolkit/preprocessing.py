import pandas as pd
import numpy as np

def fill_missing_values(df, strategy="mean"):
    for col in df.select_dtypes(include=[np.number]):
        if strategy == "mean":
            df[col].fillna(df[col].mean(), inplace=True)
        elif strategy == "median":
            df[col].fillna(df[col].median(), inplace=True)
    return df

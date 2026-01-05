import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess(df, numeric_cols):
    df = df[numeric_cols].dropna()
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

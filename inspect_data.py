import pandas as pd

df = pd.read_csv("data/raw_reviews.csv")
print(df.columns.tolist())
import pandas as pd
import plotly.express as px

df = pd.read_csv("temperature_daily.csv")

df.dropna(inplace=True)

df['date'] = pd.to_datetime(df['date'])

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

print(df)
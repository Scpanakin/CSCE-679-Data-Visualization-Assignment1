import pandas as pd
import plotly.express as px

df = pd.read_csv("temperature_daily.csv")

df.dropna(inplace=True)

df['date'] = pd.to_datetime(df['date'])

# rows will be months and columns will be year
matrix = df.groupby([df.date.dt.year, df.date.dt.month]).agg(
    tmax=('max_temperature', 'max'), tmin=('min_temperature', 'min')
)
grid_max = matrix['tmax'].unstack(0)
grid_min = matrix['tmin'].unstack(0)


import pandas as pd
import plotly.graph_objects as go
import numpy as np


df = pd.read_csv("temperature_daily.csv")

df.dropna(inplace=True)

df['date'] = pd.to_datetime(df['date'])

# rows will be months and columns will be year
matrix = df.groupby([df.date.dt.year, df.date.dt.month]).agg(
    tmax=('max_temperature', 'max'), tmin=('min_temperature', 'min')
)
grid_max = matrix['tmax'].unstack(0)
grid_min = matrix['tmin'].unstack(0)

month_names = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']


common = dict(
    x=grid_max.columns, y=month_names,
    customdata=np.dstack([grid_max, grid_min]),
    hovertemplate='Date: %{x}-%{y}<br>max: %{customdata[0]} min: %{customdata[1]}<extra></extra>',
    colorscale='spectral', zmin=-40, zmax=0,
    colorbar=dict(title='Celsius', tickvals=[0,-10,-20,-30,-40], ticktext=['0°', '10°', '20°', '30°', '40°'],),
    xgap=8, ygap=8, hoverongaps=False,
)

fig = go.Figure([
    go.Heatmap(z=-grid_max, visible=True, **common),
    go.Heatmap(z=-grid_min, visible=False, **common),
])

fig.update_layout(updatemenus=[dict(buttons=[
    dict(label='Max', method='update', args=[{'visible': [True, False]}]),
    dict(label='Min', method='update', args=[{'visible': [False, True]}]),
])])
fig.update_xaxes(side='top', tickmode="linear", dtick=1, ticks='outside', showline=True, linecolor='black',)
fig.update_yaxes(autorange='reversed', ticks='outside', showline=True, linecolor='black',)

fig.write_html("plot1.html")
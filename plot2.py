import calendar
import numpy as np
import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('temperature_daily.csv', parse_dates=['date'])
df['year'] = df.date.dt.year
df['month'] = df.date.dt.month


# change to this format to make the scatter plots easier
monthly = df.groupby(['year', 'month']).agg(
    tmax=('max_temperature', 'max'),
    tmin=('min_temperature', 'min'),
)
months = list(range(1, 13))
grid_max = monthly['tmax'].unstack(0).reindex(months)
grid_min = monthly['tmin'].unstack(0).reindex(months)
month_names = list(calendar.month_name)[1:]

common = dict(
    x=grid_max.columns,
    y=months,
    customdata=np.dstack([grid_max, grid_min]),
    hovertemplate='Date: %{x}-%{y:02d}<br>max: %{customdata[0]} min: %{customdata[1]}<extra></extra>',
    colorscale='spectral',
    zmin=-40, zmax=0,
    colorbar=dict(title='Celsius',
                  tickvals=[0, -10, -20, -30, -40],
                  ticktext=['0°', '10°', '20°', '30°', '40°']),
    xgap=4, ygap=4,
    hoverongaps=False,
)

heat_max = go.Heatmap(z=-grid_max, visible=True, **common)
heat_min = go.Heatmap(z=-grid_min, visible=False, **common)

lo = df.min_temperature.min()
hi = df.max_temperature.max()
pad = 0.4

def cell_coords(g, col):
    n = len(g)
    xs = g.year.iloc[0] - pad + 2 * pad * np.arange(n) / max(n - 1, 1)
    ys = g.month.iloc[0] + pad - 2 * pad * (g[col].values - lo) / (hi - lo)
    return list(xs) + [None], list(ys) + [None]

xmax, ymax, xmin, ymin = [], [], [], []
for _, g in df.sort_values('date').groupby(['year', 'month']):
    x, y = cell_coords(g, 'max_temperature'); xmax += x; ymax += y
    x, y = cell_coords(g, 'min_temperature'); xmin += x; ymin += y

max_line = go.Scatter(x=xmax, y=ymax, mode='lines',
                      line=dict(color='green', width=1),
                      hoverinfo='skip', showlegend=False)
min_line = go.Scatter(x=xmin, y=ymin, mode='lines',
                      line=dict(color='lightblue', width=1),
                      hoverinfo='skip', showlegend=False)

fig = go.Figure([heat_max, heat_min, max_line, min_line])


fig.update_layout(updatemenus=[dict(
    type='buttons', direction='right',
    x=0, y=1.12, xanchor='left', yanchor='bottom',
    buttons=[
        dict(label='Max', method='update', args=[{'visible': [True, False, True, True]}]),
        dict(label='Min', method='update', args=[{'visible': [False, True, True, True]}]),
    ],
)])

fig.update_xaxes(side='top', tickmode='linear', dtick=1,
                 ticks='outside', showline=True, linecolor='black',
                 showgrid=False)
fig.update_yaxes(tickvals=months, ticktext=month_names, autorange='reversed',
                 ticks='outside', showline=True, linecolor='black',
                 showgrid=False)
fig.update_layout(plot_bgcolor='white',
                  margin=dict(t=120),
                  title='Monthly Temperature with Daily Max/Min Lines')

fig.write_html('plot2.html')
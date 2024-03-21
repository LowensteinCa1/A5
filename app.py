# %%
# import dependencies
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
#from jupyter_dash import JupyterDash

# %%
# import data
gdp= pd.read_csv('/Users/carolinelowenstein/Desktop/everything/DS/assignment 4/A4_student/gdp_pcap.csv')

# %%
#change data from wide to long

long_gdp= pd.melt(gdp, id_vars='country', var_name='years', value_name='gdp')
long_gdp

# %%
#looking to see if years are an object or integer
long_gdp.info()

# %%
#since years are objects, here I make them an integer so I can use on the slider
long_gdp['years'] = long_gdp['years'].astype(int)
long_gdp.info()

# %%
#get rid of the "k"s in the gdp data column in order to make it into an integer
for index, row in long_gdp.iterrows():
    if 'k' in str(row['gdp']):
        long_gdp.at[index, 'gdp'] = float(row['gdp'].replace('k', '')) * 1000

# %%
#make gdp an integer
long_gdp['gdp'] = long_gdp['gdp'].astype(int)

# %%
# build a line chart
fig = px.line(long_gdp, 
        x = 'years', 
        y = 'gdp',
        color = 'country')
fig.update_layout(
    title_text='GDP Over Time',
    xaxis_title="Year",
    yaxis_title='GDP per Capita',
)

# display the chart
fig.show()

# %%
#my final app
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

app.layout = html.Div([
        html.Div(
        className="app-header",
        children=[
            html.Div('Assignment 4', className="app-header--title") 
        ]
    ),
    html.Div(
        children=html.Div([
            html.H1('GDP Data'),
            html.Div(''' This app displays three interactive activties.  1. A dropdown menu where you can select multiple countries 2. 
                     A slider where you can select a range of years in which the data corresponds to (1800-2100). and 3. A graph that has the year on the x axis and the GDP per capita
                     on the y axis, with each country it labeled by color. Enjoy!!
            ''')
        ])
    ),
    html.Div(children = [
        html.H2(children = 'Countries'),
        dcc.Dropdown(
            id = 'Country',
            multi = True,
            options=gdp.country.unique(),
            value='country',
            placeholder = "Select Countries to Compare Their GDPs"
            )
    ], style = {'display': 'inline-block', 'width': '50%'}),
    html.Div([
        html.H2(children = 'Year Range'),
        dcc.RangeSlider(
            id = 'range-slider-1',
            min = long_gdp['years'].min(), 
            max = long_gdp['years'].max(),
            step = 1, 
            marks={year: {'label': str(year), 'style': {'writingMode': 'vertical-rl'}} 
                   for year in range(long_gdp['years'].min(), long_gdp['years'].max() + 1, 10)}, 
            value = [long_gdp['years'].min(),long_gdp['years'].max()], 
            tooltip = {'always_visible': True}
    )
], style = {'display': 'inline-block', 'width': '50%'},),
    html.Div(
        dcc.Graph(
        id='GDP Over Time',
        figure = fig,
        style= {'marginTop': '25px'}
    )
    )
])

@app.callback(
    Output('GDP Over Time', 'figure'),  
    Input('Country', 'value'),
    Input('range-slider-1', 'value')) #cannot have a space here
def update_graph(selected_countries, year_range):
    #making sure that selected_countries is a list of strings, not just a singular string
    if not isinstance(selected_countries, list):
        selected_countries = [selected_countries]
    #updating new df to make sure the output fall in the chosen range of years and the chosen countries
    dff = long_gdp[(long_gdp['years'] >= year_range[0]) & (long_gdp['years'] <= year_range[1]) &
                   (long_gdp['country'].isin(selected_countries))]
    #creating the new updatable figure
    fig = px.line(
        data_frame=dff,
        x='years',
        y='gdp',
        color='country',
        hover_name='country'
    )

    return fig


# run app
if __name__ == '__main__':
    app.run_server(debug=True)



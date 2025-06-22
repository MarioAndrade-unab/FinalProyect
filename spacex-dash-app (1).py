# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown para selección de sitio
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [
            {'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart de lanzamientos exitosos
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # TASK 3: Control deslizante de carga útil
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        value=[min_payload, max_payload],
        marks={i: f'{i} kg' for i in range(0, 10001, 2500)},
        tooltip={'placement': 'bottom', 'always_visible': True}
    ),

    # TASK 4: Gráfico de dispersión
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Gráfico de pastel que muestra el total de éxitos por sitio
        fig = px.pie(
            spacex_df, 
            values='class', 
            names='Launch Site', 
            title='Total de lanzamientos exitosos por sitio'
        )
        return fig
    else:
        # Filtra por sitio seleccionado
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Cuenta de éxitos (class=1) y fracasos (class=0)
        fig = px.pie(
            filtered_df, 
            names='class',
            title=f'Éxitos vs Fracasos en {entered_site}',
            hole=0.3
        )
        fig.update_traces(labels=['Fracaso (0)', 'Éxito (1)'])  # opcional: personalizar etiquetas
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if selected_site == 'ALL':
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Resultados de misiones por carga útil (Todos los sitios)'
        )
    else:
        filtered_site_df = filtered_df[filtered_df['Launch Site'] == selected_site]
        fig = px.scatter(
            filtered_site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Resultados de misiones en {selected_site} por carga útil'
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run()

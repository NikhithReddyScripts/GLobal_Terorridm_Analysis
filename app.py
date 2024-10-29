import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load the cleaned dataset
# the daataset is compressed using gzip

df = pd.read_csv("/Users/saitejasriyerramsetti/Desktop/global/data/cleaned_data.csv", compression='gzip', encoding='utf-8')

#server  = app.server
# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Terrorism Data Insights"
# Import layout functions from each feature file
from pages.temporal_analysis_layout import temporal_analysis_layout
from pages.geospatial_analysis_layout import geospatial_analysis_layout
from pages.attack_weapon_analysis_layout import attack_weapon_analysis_layout
from pages.perpetrator_target_analysis_layout import perpetrator_target_analysis_layout
from pages.success_failure_analysis_layout import success_failure_analysis_layout

# App layout with Tabs for each feature
app.layout = html.Div([
    html.H1("Global Terrorism Data Analysis"),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Temporal Analysis', value='tab-1'),
        dcc.Tab(label='Geospatial Analysis', value='tab-2'),
        dcc.Tab(label='Attack Type & Weapon Analysis', value='tab-3'),
        dcc.Tab(label='Perpetrator & Target Analysis', value='tab-4'),
        dcc.Tab(label='Success/Failure Analysis', value='tab-5'),
    ]),
    html.Div(id='tabs-content')
])

# Callbacks to render content based on the selected tab
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return temporal_analysis_layout(df)
    elif tab == 'tab-2':
        return geospatial_analysis_layout(df)
    elif tab == 'tab-3':
        return attack_weapon_analysis_layout(df)
    elif tab == 'tab-4':
        return perpetrator_target_analysis_layout(df)
    elif tab == 'tab-5':
        return success_failure_analysis_layout(df)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

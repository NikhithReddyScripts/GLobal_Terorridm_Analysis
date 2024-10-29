import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("data/cleaned_data.csv", compression='gzip', encoding='utf-8')

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Global Terrorism Data Insights"

# Import layout functions from each feature file
from pages.temporal_analysis_layout import temporal_analysis_layout
from pages.geospatial_analysis_layout import geospatial_analysis_layout
from pages.attack_weapon_analysis_layout import attack_weapon_analysis_layout
from pages.perpetrator_target_analysis_layout import perpetrator_target_analysis_layout
from pages.success_failure_analysis_layout import success_failure_analysis_layout

# Home page layout
def home_page_layout():
    return html.Div([
        html.H1("Global Terrorism Patterns Unveiled", className="main-title"),
        html.H2("BDA594 Final Project - Team Cipher Syndicate", className="subtitle"),
        html.Div([
            html.P("Team Members:", className="team-header"),
            html.Div([
                html.P("Nikith Reddy", className='team-member'),
                html.P("Sai Tejasri Yerramsetti", className='team-member'),
                html.P("Rupali Donde", className='team-member'),
                html.P("Ashish Patel", className='team-member'),
            ], className="team-list"),
        ], className="team-section"),
        html.P("Welcome to the Global Terrorism Data Analysis application. Use the navigation to explore various analyses.",
               className="welcome-message"),
    ], className="home-container")

# App layout with Sidebar using dcc.Tabs
app.layout = html.Div([
    html.Div([
        html.H2("Navigation", className="sidebar-header"),
        dcc.Tabs(id="tabs", value='home', vertical=True, children=[
            dcc.Tab(label='Home', value='home', className="nav-link"),
            dcc.Tab(label='Temporal Analysis', value='tab-1', className="nav-link"),
            dcc.Tab(label='Geospatial Analysis', value='tab-2', className="nav-link"),
            dcc.Tab(label='Attack Type & Weapon Analysis', value='tab-3', className="nav-link"),
            dcc.Tab(label='Perpetrator & Target Analysis', value='tab-4', className="nav-link"),
            dcc.Tab(label='Success/Failure Analysis', value='tab-5', className="nav-link"),
        ]),
    ], className="sidebar"),

    # Content Area
    html.Div(id='tabs-content', className="content-area"),
])

# Callback to render content based on the selected tab
@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'home':
        return home_page_layout()
    elif tab == 'tab-1':
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

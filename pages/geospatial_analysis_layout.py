import plotly.express as px
from dash import html, dcc

def geospatial_analysis_layout(df):
    # Example visualization: Geospatial heatmap
    fig = px.density_mapbox(df, lat='latitude', lon='longitude', z='nkill',
                            radius=10, mapbox_style="stamen-terrain", zoom=1,
                            title="Geospatial Heatmap of Attacks")

    return html.Div([
        html.H3("Geospatial Analysis"),
        dcc.Graph(figure=fig),
        # Additional visualizations for regional hotspots and clusters
    ])


def create_geospatial_analysis_graph(df):
    fig = px.scatter_geo(df, locations="country", color="region_txt",
                         hover_name="country_txt", size="count", 
                         title="Geospatial Distribution of Attacks")
    
    # Dark theme settings
    fig.update_layout(
        paper_bgcolor="#1e1e2f",
        plot_bgcolor="#282a36",
        font=dict(color="#e0e0e0"),
        title=dict(font=dict(size=24, color="#ff2e63")),
        geo=dict(
            bgcolor="#1e1e2f"
        ),
    )
    return fig

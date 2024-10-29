import plotly.express as px
from dash import html, dcc
import plotly.express as px

def create_temporal_analysis_graph(df):
    fig = px.line(df, x="iyear", y="count", title="Number of Attacks Over Time")
    
    # Dark theme settings
    fig.update_layout(
        paper_bgcolor="#1e1e2f",
        plot_bgcolor="#282a36",
        font=dict(color="#e0e0e0"),
        title=dict(font=dict(size=24, color="#ff2e63")),
        xaxis=dict(
            title="Year",
            showgrid=False,
            zeroline=False,
            color="#e0e0e0",
        ),
        yaxis=dict(
            title="Count",
            showgrid=False,
            zeroline=False,
            color="#e0e0e0",
        ),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig

def temporal_analysis_layout(df):
    # Example visualization: Number of attacks over time
    attacks_by_year = df.groupby('iyear').size().reset_index(name='count')
    fig = px.line(attacks_by_year, x='iyear', y='count', title="Number of Attacks Over Time")

    return html.Div([
        html.H3("Temporal Analysis"),
        dcc.Graph(figure=fig),
        # Add more visualizations and detailed insights here
    ])

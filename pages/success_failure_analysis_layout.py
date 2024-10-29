import plotly.express as px
from dash import html, dcc

def success_failure_analysis_layout(df):
    # Prepare necessary data for each visualization

    # 1. Success/Failure Pie Chart
    success_counts = df['success'].value_counts().reset_index()
    success_counts.columns = ['Outcome', 'Count']
    success_counts['Outcome'] = success_counts['Outcome'].map({1: 'Success', 0: 'Failure'})
    pie_chart = px.pie(success_counts, names='Outcome', values='Count', title="Success/Failure Rates")

    # Insights for success and failure rates
    total_attacks = success_counts['Count'].sum()
    success_percentage = round((success_counts[success_counts['Outcome'] == 'Success']['Count'].values[0] / total_attacks) * 100, 2)
    failure_percentage = 100 - success_percentage

    # 2. Success Rate Over Time
    yearly_data = df.groupby(['iyear', 'success']).size().unstack().fillna(0)
    yearly_data['success_rate'] = yearly_data[1] / (yearly_data[1] + yearly_data[0]) * 100
    line_chart = px.line(yearly_data, x=yearly_data.index, y='success_rate', title="Success Rate Over Time")

    # Insight for success rate over time
    avg_success_rate = round(yearly_data['success_rate'].mean(), 2)

    # 3. Success Rate by Region
    region_data = df.groupby(['region_txt', 'success']).size().unstack().fillna(0)
    region_data['success_rate'] = region_data[1] / (region_data[1] + region_data[0]) * 100
    region_bar_chart = px.bar(region_data, x=region_data.index, y='success_rate', title="Success Rate by Region")

    # Insight for success rate by region
    top_region = region_data['success_rate'].idxmax()
    top_region_success = round(region_data['success_rate'].max(), 2)

    # 4. Success Rate by Attack Type
    attack_data = df.groupby(['attacktype1_txt', 'success']).size().unstack().fillna(0)
    attack_data['success_rate'] = attack_data[1] / (attack_data[1] + attack_data[0]) * 100
    attack_bar_chart = px.bar(attack_data, x=attack_data.index, y='success_rate', title="Success Rate by Attack Type")

    # Insight for success rate by attack type
    top_attack_type = attack_data['success_rate'].idxmax()
    top_attack_type_success = round(attack_data['success_rate'].max(), 2)

    # 5. Success Rate by Target Type
    target_data = df.groupby(['targtype1_txt', 'success']).size().unstack().fillna(0)
    target_data['success_rate'] = target_data[1] / (target_data[1] + target_data[0]) * 100
    target_bar_chart = px.bar(target_data, x=target_data.index, y='success_rate', title="Success Rate by Target Type")

    # Insight for success rate by target type
    top_target_type = target_data['success_rate'].idxmax()
    top_target_type_success = round(target_data['success_rate'].max(), 2)

    # 6. Impact of Success on Casualties
    casualty_data = df.groupby('success').agg({'nkill': 'mean', 'nwound': 'mean'}).reset_index()
    casualty_data['Outcome'] = casualty_data['success'].map({1: 'Success', 0: 'Failure'})
    casualty_bar_chart = px.bar(casualty_data, x='Outcome', y=['nkill', 'nwound'], title="Impact of Success on Casualties")

    # Insight for impact of success on casualties
    avg_kills_success = round(casualty_data[casualty_data['Outcome'] == 'Success']['nkill'].values[0], 2)
    avg_kills_failure = round(casualty_data[casualty_data['Outcome'] == 'Failure']['nkill'].values[0], 2)

    # 7. Successful vs Unsuccessful Attacks Over Time (Stacked Area Chart)
    stacked_area_data = df.groupby(['iyear', 'success']).size().unstack().fillna(0)
    stacked_area_chart = px.area(stacked_area_data, x=stacked_area_data.index, y=[0, 1], 
                                 labels={'value': 'Count', 'iyear': 'Year'}, 
                                 title="Successful vs Unsuccessful Attacks Over Time",
                                 color_discrete_map={0: 'red', 1: 'green'})
    stacked_area_chart.update_layout(legend_title_text='Outcome', xaxis_title="Year", yaxis_title="Count")

    # Insight for successful vs unsuccessful attacks over time
    most_successful_year = stacked_area_data[1].idxmax()
    highest_success_count = stacked_area_data[1].max()

    # Additional insights can be added for remaining plots similarly

    # Returning the layout with all the plots and findings
    return html.Div([
        html.H3("Success/Failure Analysis", className="page-title"),

        html.Div([
            html.H4("Overall Success/Failure Rates"),
            dcc.Graph(figure=pie_chart),
            html.P(f"Success rate: {success_percentage}%, Failure rate: {failure_percentage}%. A high success rate suggests serious concerns for global security."),
        ], className="graph-container"),

        html.Div([
            html.H4("Success Rate Over Time"),
            dcc.Graph(figure=line_chart),
            html.P(f"Average success rate over the years: {avg_success_rate}%. There have been fluctuations, indicating shifts in counter-terrorism effectiveness."),
        ], className="graph-container"),

        html.Div([
            html.H4("Success Rate by Region"),
            dcc.Graph(figure=region_bar_chart),
            html.P(f"The region with the highest success rate is {top_region} at {top_region_success}%. Regional disparities suggest different levels of vulnerability."),
        ], className="graph-container"),

        html.Div([
            html.H4("Success Rate by Attack Type"),
            dcc.Graph(figure=attack_bar_chart),
            html.P(f"The most successful attack type is {top_attack_type} with a success rate of {top_attack_type_success}%. Certain attack methods are more likely to succeed."),
        ], className="graph-container"),

        html.Div([
            html.H4("Success Rate by Target Type"),
            dcc.Graph(figure=target_bar_chart),
            html.P(f"Attacks targeting {top_target_type} have the highest success rate at {top_target_type_success}%. This suggests certain groups are more vulnerable."),
        ], className="graph-container"),

        html.Div([
            html.H4("Impact of Success on Casualties"),
            dcc.Graph(figure=casualty_bar_chart),
            html.P(f"Average kills in successful attacks: {avg_kills_success}. Unsuccessful attacks have lower casualties at {avg_kills_failure}, emphasizing the need for prevention."),
        ], className="graph-container"),

        html.Div([
            html.H4("Successful vs Unsuccessful Attacks Over Time"),
            dcc.Graph(figure=stacked_area_chart),
            html.P(f"The year with the highest number of successful attacks is {most_successful_year} with {highest_success_count} incidents."),
        ], className="graph-container"),

        # Add insights for remaining plots as needed
    ])

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def plot_global_trends(day_wise_df):
    """
    Create a plot showing global COVID-19 trends.
    
    Args:
        day_wise_df: Processed day-wise COVID-19 data
        
    Returns:
        Plotly figure
    """
    fig = make_subplots(rows=2, cols=2, 
                        subplot_titles=("Global Confirmed Cases", "Global Deaths", 
                                        "Global Recovered Cases", "Global Active Cases"),
                        shared_xaxes=True)

    fig.add_trace(go.Scatter(x=day_wise_df['Date'], y=day_wise_df['Confirmed'], 
                             mode='lines', name='Confirmed', line=dict(color='#0072B2')), row=1, col=1)
    
    fig.add_trace(go.Scatter(x=day_wise_df['Date'], y=day_wise_df['Deaths'], 
                             mode='lines', name='Deaths', line=dict(color='#D55E00')), row=1, col=2)
    
    fig.add_trace(go.Scatter(x=day_wise_df['Date'], y=day_wise_df['Recovered'], 
                             mode='lines', name='Recovered', line=dict(color='#009E73')), row=2, col=1)
    
    fig.add_trace(go.Scatter(x=day_wise_df['Date'], y=day_wise_df['Active'], 
                             mode='lines', name='Active', line=dict(color='#CC79A7')), row=2, col=2)

    fig.update_layout(height=600, showlegend=False)
    
    return fig

def plot_daily_statistics(day_wise_df):
    """
    Create a plot showing daily COVID-19 statistics.
    
    Args:
        day_wise_df: Processed day-wise COVID-19 data
        
    Returns:
        Plotly figure
    """
    fig = make_subplots(rows=1, cols=3, 
                        subplot_titles=("Daily New Cases", "Daily New Deaths", "Daily New Recovered"),
                        shared_xaxes=True)

    fig.add_trace(go.Bar(x=day_wise_df['Date'], y=day_wise_df['New cases'], 
                         name='New Cases', marker_color='#0072B2'), row=1, col=1)
    
    fig.add_trace(go.Bar(x=day_wise_df['Date'], y=day_wise_df['New deaths'], 
                         name='New Deaths', marker_color='#D55E00'), row=1, col=2)
    
    fig.add_trace(go.Bar(x=day_wise_df['Date'], y=day_wise_df['New recovered'], 
                         name='New Recovered', marker_color='#009E73'), row=1, col=3)

    fig.update_layout(height=400, showlegend=False)
    
    return fig

def plot_global_map(latest_data):
    """
    Create a choropleth map showing global distribution of COVID-19 cases.
    
    Args:
        latest_data: Latest COVID-19 data by country
        
    Returns:
        Plotly figure
    """
    # Use log scale for better visualization of the distribution
    fig = px.choropleth(latest_data, 
                        locations="Country/Region", 
                        locationmode="country names",
                        color=np.log10(latest_data["Confirmed"] + 1),  # +1 to avoid log(0)
                        hover_name="Country/Region",
                        hover_data=["Confirmed", "Deaths", "Recovered", "Active"],
                        color_continuous_scale=px.colors.sequential.Plasma,
                        labels={"color": "Log10(Confirmed Cases)"})

    fig.update_layout(
        title_text="Global Distribution of COVID-19 Cases (log scale)",
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        ),
        height=500
    )
    
    return fig

def plot_top_countries(latest_data):
    """
    Create a horizontal bar chart showing top countries by confirmed cases.
    
    Args:
        latest_data: Latest COVID-19 data by country
        
    Returns:
        Plotly figure
    """
    # Sort by confirmed cases and get top 10
    top_countries = latest_data.sort_values('Confirmed', ascending=False).head(10)
    
    fig = px.bar(top_countries, y='Country/Region', x='Confirmed', 
                 color='WHO Region', orientation='h',
                 labels={'Confirmed': 'Total Confirmed Cases', 'Country/Region': 'Country'},
                 height=500)
    
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    
    return fig

def plot_country_comparison(filtered_data, metric):
    """
    Create a bar chart comparing selected countries on a specific metric.
    
    Args:
        filtered_data: Data filtered for selected countries
        metric: The metric to compare (e.g., 'Confirmed', 'Deaths')
        
    Returns:
        Plotly figure
    """
    # Sort data by the selected metric
    sorted_data = filtered_data.sort_values(metric, ascending=False)
    
    fig = px.bar(sorted_data, x='Country/Region', y=metric,
                 color='WHO Region',
                 labels={'Country/Region': 'Country'},
                 height=500)
    
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    
    return fig

def plot_country_trends(country_data, metric):
    """
    Create a line chart showing trends for selected countries on a specific metric.
    
    Args:
        country_data: Time series data for selected countries
        metric: The metric to plot (e.g., 'Confirmed', 'Deaths')
        
    Returns:
        Plotly figure
    """
    fig = px.line(country_data, x='Date', y=metric, color='Country/Region',
                  labels={metric: f'Total {metric} Cases', 'Date': 'Date', 'Country/Region': 'Country'},
                  height=500)
    
    return fig

def plot_region_distribution(region_data):
    """
    Create pie charts showing distribution of COVID-19 cases by WHO Region.
    
    Args:
        region_data: Data grouped by WHO Region
        
    Returns:
        Plotly figure
    """
    fig = make_subplots(rows=2, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}],
                                               [{'type': 'domain'}, {'type': 'domain'}]],
                        subplot_titles=("Confirmed Cases", "Deaths", 
                                        "Recovered Cases", "Active Cases"))

    fig.add_trace(go.Pie(labels=region_data['WHO Region'], values=region_data['Confirmed'], 
                         name="Confirmed"), 1, 1)
    
    fig.add_trace(go.Pie(labels=region_data['WHO Region'], values=region_data['Deaths'], 
                         name="Deaths"), 1, 2)
    
    fig.add_trace(go.Pie(labels=region_data['WHO Region'], values=region_data['Recovered'], 
                         name="Recovered"), 2, 1)
    
    fig.add_trace(go.Pie(labels=region_data['WHO Region'], values=region_data['Active'], 
                         name="Active"), 2, 2)

    fig.update_layout(height=700)
    
    return fig

def plot_continent_analysis(continent_data):
    """
    Create bar charts showing COVID-19 impact by continent.
    
    Args:
        continent_data: Data grouped by continent
        
    Returns:
        Plotly figure
    """
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Cases per Million", "Deaths per Million"))

    fig.add_trace(go.Bar(x=continent_data['Continent'], y=continent_data['Cases per Million'], 
                         name="Cases per Million", marker_color='#0072B2'), 1, 1)
    
    fig.add_trace(go.Bar(x=continent_data['Continent'], y=continent_data['Deaths per Million'], 
                         name="Deaths per Million", marker_color='#D55E00'), 1, 2)

    fig.update_layout(height=500)
    
    return fig

def plot_global_metric_trend(day_wise_df, metric):
    """
    Create a line chart showing global trend for a specific metric.
    
    Args:
        day_wise_df: Day-wise COVID-19 data
        metric: The metric to plot (e.g., 'Confirmed', 'Deaths')
        
    Returns:
        Plotly figure
    """
    fig = px.line(day_wise_df, x='Date', y=metric,
                  labels={metric: f'Total {metric} Cases', 'Date': 'Date'},
                  height=500)
    
    # Add markers at important points
    max_date = day_wise_df['Date'].max()
    max_value = day_wise_df[day_wise_df['Date'] == max_date][metric].values[0]
    
    fig.add_trace(go.Scatter(
        x=[max_date],
        y=[max_value],
        mode="markers+text",
        text=[f"{int(max_value):,}"],
        textposition="top right",
        marker=dict(color="red", size=10),
        showlegend=False
    ))
    
    return fig

def plot_global_daily_trend(day_wise_df, metric):
    """
    Create a bar chart showing global daily trend for a specific metric.
    
    Args:
        day_wise_df: Day-wise COVID-19 data
        metric: The daily metric to plot (e.g., 'New cases', 'New deaths')
        
    Returns:
        Plotly figure
    """
    fig = px.bar(day_wise_df, x='Date', y=metric,
                 labels={metric: f'Daily {metric}', 'Date': 'Date'},
                 height=500)
    
    # Add moving average
    window_size = 7
    day_wise_df[f'{metric} (7-day MA)'] = day_wise_df[metric].rolling(window=window_size).mean()
    
    fig.add_trace(go.Scatter(
        x=day_wise_df['Date'],
        y=day_wise_df[f'{metric} (7-day MA)'],
        mode='lines',
        name=f'7-day Moving Average',
        line=dict(color='red', width=2)
    ))
    
    return fig

def plot_countries_trend(country_data, metric):
    """
    Create a line chart showing trends for selected countries on a specific metric.
    
    Args:
        country_data: Time series data for selected countries
        metric: The metric to plot (e.g., 'Confirmed', 'Deaths')
        
    Returns:
        Plotly figure
    """
    fig = px.line(country_data, x='Date', y=metric, color='Country/Region',
                  labels={metric: f'Total {metric} Cases', 'Date': 'Date', 'Country/Region': 'Country'},
                  height=500)
    
    # Option to use log scale
    fig.update_layout(
        yaxis_type="log"
    )
    
    return fig

def plot_growth_rate(country_data):
    """
    Create a line chart showing growth rate for selected countries.
    
    Args:
        country_data: Time series data for selected countries
        
    Returns:
        Plotly figure
    """
    # Calculate daily growth rate for each country
    countries = country_data['Country/Region'].unique()
    growth_data = pd.DataFrame()
    
    for country in countries:
        country_df = country_data[country_data['Country/Region'] == country].sort_values('Date')
        country_df['Growth Rate (%)'] = country_df['Confirmed'].pct_change() * 100
        growth_data = pd.concat([growth_data, country_df])
    
    # Create line chart
    fig = px.line(growth_data, x='Date', y='Growth Rate (%)', color='Country/Region',
                  labels={'Growth Rate (%)': 'Daily Growth Rate (%)', 'Date': 'Date', 'Country/Region': 'Country'},
                  height=500)
    
    return fig

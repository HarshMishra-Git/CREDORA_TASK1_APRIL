import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import data_processor
import visualization

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("COVID-19 Data Analysis Dashboard")
st.markdown("""
This dashboard provides interactive visualizations of COVID-19 data from around the world.
Explore trends, compare regions, and gain insights into the pandemic's impact globally.
""")

# Load data
@st.cache_data
def load_data():
    try:
        # Load datasets
        day_wise_df = pd.read_csv('attached_assets/day_wise.csv')
        full_grouped_df = pd.read_csv('attached_assets/full_grouped.csv')
        worldometer_df = pd.read_csv('attached_assets/worldometer_data.csv')
        
        # Process datasets
        processed_data = data_processor.process_all_datasets(day_wise_df, full_grouped_df, worldometer_df)
        
        return processed_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Main function to run the app
def main():
    # Load and process data
    data = load_data()
    if not data:
        st.error("Failed to load data. Please check the data files and try again.")
        return
    
    day_wise_df = data['day_wise']
    full_grouped_df = data['full_grouped']
    worldometer_df = data['worldometer']
    latest_data = data['latest_data']
    
    # Sidebar for navigation and filters
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Global Overview", "Country Analysis", "Regional Comparison", "Time Series Analysis", "Data Explorer"]
    )
    
    # Global filters
    st.sidebar.title("Filters")
    
    # Date range filter for time series
    if 'Date' in day_wise_df.columns:
        min_date = day_wise_df['Date'].min()
        max_date = day_wise_df['Date'].max()
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_day_wise = day_wise_df[(day_wise_df['Date'] >= pd.to_datetime(start_date)) & 
                                          (day_wise_df['Date'] <= pd.to_datetime(end_date))]
        else:
            filtered_day_wise = day_wise_df
    else:
        filtered_day_wise = day_wise_df
    
    # Country filter for country analysis
    all_countries = sorted(latest_data['Country/Region'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select Countries to Compare",
        all_countries,
        default=latest_data.sort_values('Confirmed', ascending=False).head(5)['Country/Region'].tolist()
    )
    
    # WHO Region filter
    if 'WHO Region' in latest_data.columns:
        all_regions = sorted(latest_data['WHO Region'].unique())
        selected_regions = st.sidebar.multiselect(
            "Select WHO Regions",
            all_regions,
            default=all_regions
        )
        
        region_filtered_data = latest_data[latest_data['WHO Region'].isin(selected_regions)]
    else:
        region_filtered_data = latest_data
    
    # Handle page selection
    if page == "Global Overview":
        display_global_overview(filtered_day_wise, region_filtered_data)
    
    elif page == "Country Analysis":
        if selected_countries:
            display_country_analysis(full_grouped_df, latest_data, selected_countries)
        else:
            st.warning("Please select at least one country in the sidebar.")
    
    elif page == "Regional Comparison":
        display_regional_comparison(region_filtered_data, worldometer_df)
    
    elif page == "Time Series Analysis":
        display_time_series_analysis(filtered_day_wise, full_grouped_df, selected_countries)
    
    elif page == "Data Explorer":
        display_data_explorer(latest_data, worldometer_df)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <p>COVID-19 Dashboard | Data sourced from public datasets</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Page functions
def display_global_overview(day_wise_df, latest_data):
    st.header("Global COVID-19 Overview")
    
    # Get latest global numbers
    latest_date = day_wise_df['Date'].max()
    latest_global = day_wise_df[day_wise_df['Date'] == latest_date].iloc[0]
    
    # Create key metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Confirmed Cases", f"{int(latest_global['Confirmed']):,}", 
                 f"{int(latest_global['New cases']):,}")
        
    with col2:
        st.metric("Deaths", f"{int(latest_global['Deaths']):,}", 
                 f"{int(latest_global['New deaths']):,}")
        
    with col3:
        st.metric("Recovered", f"{int(latest_global['Recovered']):,}", 
                 f"{int(latest_global['New recovered']):,}")
        
    with col4:
        st.metric("Active Cases", f"{int(latest_global['Active']):,}")
    
    # Global trends chart
    st.subheader("Global COVID-19 Trends")
    global_trend_chart = visualization.plot_global_trends(day_wise_df)
    st.plotly_chart(global_trend_chart, use_container_width=True)
    
    # Daily statistics chart
    st.subheader("Daily COVID-19 Statistics")
    daily_stats_chart = visualization.plot_daily_statistics(day_wise_df)
    st.plotly_chart(daily_stats_chart, use_container_width=True)
    
    # Top countries map
    st.subheader("Global Distribution of COVID-19 Cases")
    global_map = visualization.plot_global_map(latest_data)
    st.plotly_chart(global_map, use_container_width=True)
    
    # Top 10 countries
    st.subheader("Top 10 Countries by Confirmed Cases")
    top_countries_chart = visualization.plot_top_countries(latest_data)
    st.plotly_chart(top_countries_chart, use_container_width=True)

def display_country_analysis(full_grouped_df, latest_data, selected_countries):
    st.header("Country-wise COVID-19 Analysis")
    
    if not selected_countries:
        st.warning("Please select at least one country to display analysis.")
        return
    
    # Filter data for selected countries
    filtered_latest = latest_data[latest_data['Country/Region'].isin(selected_countries)]
    
    # Create comparison table
    st.subheader("Country Comparison")
    
    # Sort by confirmed cases
    comparison_data = filtered_latest.sort_values('Confirmed', ascending=False)
    
    # Calculate additional metrics
    comparison_data['Mortality Rate (%)'] = (comparison_data['Deaths'] / comparison_data['Confirmed'] * 100).round(2)
    comparison_data['Recovery Rate (%)'] = (comparison_data['Recovered'] / comparison_data['Confirmed'] * 100).round(2)
    
    # Display comparison table
    st.dataframe(comparison_data[['Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 
                                'Mortality Rate (%)', 'Recovery Rate (%)', 'WHO Region']])
    
    # Country comparison chart
    st.subheader("Comparison of COVID-19 Statistics")
    metric_options = ["Confirmed", "Deaths", "Recovered", "Active", "Mortality Rate (%)", "Recovery Rate (%)"]
    selected_metric = st.selectbox("Select Metric to Compare", metric_options)
    
    comparison_chart = visualization.plot_country_comparison(comparison_data, selected_metric)
    st.plotly_chart(comparison_chart, use_container_width=True)
    
    # Time series for selected countries
    st.subheader("COVID-19 Trends for Selected Countries")
    trend_metric = st.selectbox("Select Metric for Trend Analysis", ["Confirmed", "Deaths", "Recovered", "Active"])
    
    # Filter time series data for selected countries
    country_time_series = full_grouped_df[full_grouped_df['Country/Region'].isin(selected_countries)]
    
    # Plot time series
    country_trend_chart = visualization.plot_country_trends(country_time_series, trend_metric)
    st.plotly_chart(country_trend_chart, use_container_width=True)

def display_regional_comparison(latest_data, worldometer_df):
    st.header("Regional COVID-19 Comparison")
    
    # Group data by WHO Region
    region_data = latest_data.groupby('WHO Region').agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum',
        'Active': 'sum'
    }).reset_index()
    
    # Calculate mortality and recovery rates
    region_data['Mortality Rate (%)'] = (region_data['Deaths'] / region_data['Confirmed'] * 100).round(2)
    region_data['Recovery Rate (%)'] = (region_data['Recovered'] / region_data['Confirmed'] * 100).round(2)
    
    # Display region data
    st.subheader("COVID-19 Statistics by WHO Region")
    st.dataframe(region_data.sort_values('Confirmed', ascending=False))
    
    # Regional distribution charts
    st.subheader("Regional Distribution of COVID-19 Cases")
    region_charts = visualization.plot_region_distribution(region_data)
    st.plotly_chart(region_charts, use_container_width=True)
    
    # Continental analysis if available
    if 'Continent' in worldometer_df.columns:
        st.subheader("COVID-19 Impact by Continent")
        
        # Group by continent
        continent_data = worldometer_df.groupby('Continent').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Recovered': 'sum',
            'Active': 'sum',
            'Population': 'sum'
        }).reset_index()
        
        # Calculate per million metrics
        continent_data['Cases per Million'] = (continent_data['Confirmed'] / continent_data['Population'] * 1000000).round(2)
        continent_data['Deaths per Million'] = (continent_data['Deaths'] / continent_data['Population'] * 1000000).round(2)
        
        # Display continent data
        st.dataframe(continent_data.sort_values('Confirmed', ascending=False))
        
        # Continent charts
        continent_charts = visualization.plot_continent_analysis(continent_data)
        st.plotly_chart(continent_charts, use_container_width=True)

def display_time_series_analysis(day_wise_df, full_grouped_df, selected_countries):
    st.header("Time Series Analysis")
    
    # Global trends
    st.subheader("Global COVID-19 Cumulative Trends")
    cumulative_metrics = ["Confirmed", "Deaths", "Recovered", "Active"]
    selected_cumulative = st.selectbox("Select Metric (Cumulative)", cumulative_metrics)
    
    global_cumulative_chart = visualization.plot_global_metric_trend(day_wise_df, selected_cumulative)
    st.plotly_chart(global_cumulative_chart, use_container_width=True)
    
    # Global daily trends
    st.subheader("Global COVID-19 Daily Trends")
    daily_metrics = ["New cases", "New deaths", "New recovered"]
    selected_daily = st.selectbox("Select Metric (Daily)", daily_metrics)
    
    global_daily_chart = visualization.plot_global_daily_trend(day_wise_df, selected_daily)
    st.plotly_chart(global_daily_chart, use_container_width=True)
    
    # Country trends
    if selected_countries:
        st.subheader("COVID-19 Trends for Selected Countries")
        country_metric = st.selectbox("Select Metric for Country Comparison", cumulative_metrics)
        
        # Filter time series data for selected countries
        country_time_series = full_grouped_df[full_grouped_df['Country/Region'].isin(selected_countries)]
        
        # Plot time series
        countries_chart = visualization.plot_countries_trend(country_time_series, country_metric)
        st.plotly_chart(countries_chart, use_container_width=True)
        
        # Growth rate analysis
        st.subheader("Growth Rate Analysis for Selected Countries")
        growth_chart = visualization.plot_growth_rate(country_time_series)
        st.plotly_chart(growth_chart, use_container_width=True)
    else:
        st.info("Please select countries from the sidebar to view country-specific time series.")

def display_data_explorer(latest_data, worldometer_df):
    st.header("COVID-19 Data Explorer")
    
    # Allow user to select dataset
    dataset_choice = st.radio(
        "Select Dataset to Explore",
        ["Latest Country Data", "Worldometer Data (with additional metrics)"]
    )
    
    if dataset_choice == "Latest Country Data":
        data_to_explore = latest_data
        st.subheader("Latest COVID-19 Data by Country")
    else:
        data_to_explore = worldometer_df
        st.subheader("Worldometer COVID-19 Data with Additional Metrics")
    
    # Allow searching and filtering
    search_term = st.text_input("Search for a country")
    
    if search_term:
        filtered_data = data_to_explore[data_to_explore['Country/Region'].str.contains(search_term, case=False)]
    else:
        filtered_data = data_to_explore
    
    # Display data
    st.dataframe(filtered_data)
    
    # Download option
    st.download_button(
        label="Download this data as CSV",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name=f"covid19_data_{dataset_choice.lower().replace(' ', '_')}.csv",
        mime="text/csv"
    )
    
    # Custom visualization
    st.subheader("Create Custom Visualization")
    
    # Get numeric columns for x and y selection
    numeric_columns = [col for col in data_to_explore.columns if data_to_explore[col].dtype in ['int64', 'float64']]
    
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox("Select X-axis", numeric_columns, index=numeric_columns.index("Confirmed") if "Confirmed" in numeric_columns else 0)
    
    with col2:
        y_axis = st.selectbox("Select Y-axis", numeric_columns, index=numeric_columns.index("Deaths") if "Deaths" in numeric_columns else min(1, len(numeric_columns)-1))
    
    # Color option
    color_by = st.selectbox("Color by", ["None"] + ["WHO Region", "Continent"] if "WHO Region" in data_to_explore.columns else ["None"])
    
    # Create custom visualization
    if color_by == "None":
        fig = px.scatter(
            filtered_data, x=x_axis, y=y_axis,
            hover_name="Country/Region",
            size=x_axis if len(filtered_data) > 1 else None,
            log_x=True if st.checkbox("Log Scale X-axis") else False,
            log_y=True if st.checkbox("Log Scale Y-axis") else False,
            title=f"{y_axis} vs {x_axis}"
        )
    else:
        fig = px.scatter(
            filtered_data, x=x_axis, y=y_axis,
            hover_name="Country/Region",
            color=color_by,
            size=x_axis if len(filtered_data) > 1 else None,
            log_x=True if st.checkbox("Log Scale X-axis") else False,
            log_y=True if st.checkbox("Log Scale Y-axis") else False,
            title=f"{y_axis} vs {x_axis} by {color_by}"
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Run the app
if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
from datetime import datetime

def process_day_wise_data(day_wise_df):
    """
    Process the day-wise COVID-19 data.
    
    Args:
        day_wise_df: DataFrame containing day-wise COVID-19 data
        
    Returns:
        Processed DataFrame
    """
    # Make a copy to avoid modifying the original
    df = day_wise_df.copy()
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df

def process_full_grouped_data(full_grouped_df):
    """
    Process the country-wise COVID-19 data.
    
    Args:
        full_grouped_df: DataFrame containing country-wise COVID-19 data
        
    Returns:
        Processed DataFrame
    """
    # Make a copy to avoid modifying the original
    df = full_grouped_df.copy()
    
    # Convert Date column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Remove records where confirmed cases are less than 15
    df = df[df['Confirmed'] >= 15]
    
    # Keep only relevant columns
    relevant_columns = ['Date', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered', 'Active', 'WHO Region']
    df = df[relevant_columns]
    
    return df

def process_worldometer_data(worldometer_df):
    """
    Process the worldometer COVID-19 data.
    
    Args:
        worldometer_df: DataFrame containing worldometer COVID-19 data
        
    Returns:
        Processed DataFrame
    """
    # Make a copy to avoid modifying the original
    df = worldometer_df.copy()
    
    # Remove rows with confirmed cases less than 15
    df = df[df['TotalCases'] >= 15]
    
    # Rename columns for consistency
    df = df.rename(columns={
        'TotalCases': 'Confirmed',
        'TotalDeaths': 'Deaths',
        'TotalRecovered': 'Recovered',
        'ActiveCases': 'Active'
    })
    
    # Handle missing values in numeric columns
    numeric_columns = ['Confirmed', 'Deaths', 'Recovered', 'Active']
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0)
    
    return df

def get_latest_data(full_grouped_df):
    """
    Get the latest available data for each country.
    
    Args:
        full_grouped_df: Processed country-wise COVID-19 data
        
    Returns:
        DataFrame containing the latest data for each country
    """
    # Find the latest date in the dataset
    latest_date = full_grouped_df['Date'].max()
    
    # Filter data for the latest date
    latest_data = full_grouped_df[full_grouped_df['Date'] == latest_date]
    
    # Calculate additional metrics
    if 'Confirmed' in latest_data.columns and 'Deaths' in latest_data.columns:
        latest_data['Mortality Rate (%)'] = (latest_data['Deaths'] / latest_data['Confirmed'] * 100).round(2)
    
    if 'Confirmed' in latest_data.columns and 'Recovered' in latest_data.columns:
        latest_data['Recovery Rate (%)'] = (latest_data['Recovered'] / latest_data['Confirmed'] * 100).round(2)
    
    return latest_data

def process_all_datasets(day_wise_df, full_grouped_df, worldometer_df):
    """
    Process all datasets and return a dictionary of processed data.
    
    Args:
        day_wise_df: Day-wise COVID-19 data
        full_grouped_df: Country-wise COVID-19 data
        worldometer_df: Worldometer COVID-19 data
        
    Returns:
        Dictionary containing all processed datasets
    """
    processed_day_wise = process_day_wise_data(day_wise_df)
    processed_full_grouped = process_full_grouped_data(full_grouped_df)
    processed_worldometer = process_worldometer_data(worldometer_df)
    latest_data = get_latest_data(processed_full_grouped)
    
    return {
        'day_wise': processed_day_wise,
        'full_grouped': processed_full_grouped,
        'worldometer': processed_worldometer,
        'latest_data': latest_data
    }

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
from smolagents import tool, Tool, CodeAgent, OpenAIServerModel
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# Load HDB resale price data with proper error handling
@st.cache_data
def load_hdb_data():
    """Load and combine all HDB resale price data files"""
    try:
        # Files without remaining_lease column
        csv_files = [
            'data/csv/ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv', 
            'data/csv/ResaleFlatPricesBasedonApprovalDate19901999.csv',
            'data/csv/ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv'
        ]
        
        # Files with remaining_lease column (need to drop it)
        csv_remaining_lease_files = [
            'data/csv/ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv',
            'data/csv/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv'
        ]
        
        df_list = []
        
        # Load files without remaining_lease
        for file in csv_files:
            if os.path.exists(file):
                temp_df = pd.read_csv(file)
                temp_df['source_file'] = file
                df_list.append(temp_df)
        
        # Load files with remaining_lease and drop the column
        for file in csv_remaining_lease_files:
            if os.path.exists(file):
                temp_df = pd.read_csv(file)
                if 'remaining_lease' in temp_df.columns:
                    temp_df = temp_df.drop('remaining_lease', axis=1)
                temp_df['source_file'] = file
                df_list.append(temp_df)
        
        if not df_list:
            st.error("No CSV files found. Please check your data directory.")
            return pd.DataFrame()
        
        # Combine all dataframes
        df = pd.concat(df_list, ignore_index=True)
        
        # Data preprocessing
        df['month'] = pd.to_datetime(df['month'])
        df['year'] = df['month'].dt.year
        df['resale_price'] = pd.to_numeric(df['resale_price'], errors='coerce')
        df['floor_area_sqm'] = pd.to_numeric(df['floor_area_sqm'], errors='coerce')
        df['lease_commence_date'] = pd.to_numeric(df['lease_commence_date'], errors='coerce')
        
        # Calculate price per sqm
        df['price_per_sqm'] = df['resale_price'] / df['floor_area_sqm']
        
        # Calculate remaining lease (approximate)
        current_year = datetime.now().year
        df['remaining_lease_years'] = 99 - (current_year - df['lease_commence_date'])
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


# Custom tools for HDB price analysis
@tool
def analyze_price_trends(town: str = None, flat_type: str = None, years: int = 5) -> str:
    """
    Analyze price trends for a specific town and flat type over the specified number of years.
    
    Args:
        town: The town to analyze (optional, if not provided analyzes all towns)
        flat_type: The flat type to analyze (optional, if not provided analyzes all types)
        years: Number of years to look back (default: 5)
    
    Returns:
        String containing analysis results
    """
    try:
        df = load_hdb_data()
        if df.empty:
            return "No data available for analysis."
        
        # Filter data
        end_date = df['month'].max()
        start_date = end_date - pd.DateOffset(years=years)
        filtered_df = df[df['month'] >= start_date].copy()
        
        if town:
            filtered_df = filtered_df[filtered_df['town'].str.upper() == town.upper()]
        if flat_type:
            filtered_df = filtered_df[filtered_df['flat_type'].str.upper() == flat_type.upper()]
        
        if filtered_df.empty:
            return f"No data found for the specified criteria: town={town}, flat_type={flat_type}"
        
        # Calculate trend metrics
        monthly_avg = filtered_df.groupby('month')['resale_price'].mean().reset_index()
        
        if len(monthly_avg) < 2:
            return "Insufficient data for trend analysis."
        
        # Calculate percentage change
        start_price = monthly_avg['resale_price'].iloc[0]
        end_price = monthly_avg['resale_price'].iloc[-1]
        total_change = ((end_price - start_price) / start_price) * 100
        
        # Calculate recent trend (last 12 months)
        recent_data = monthly_avg.tail(12)
        if len(recent_data) >= 2:
            recent_start = recent_data['resale_price'].iloc[0]
            recent_end = recent_data['resale_price'].iloc[-1]
            recent_change = ((recent_end - recent_start) / recent_start) * 100
        else:
            recent_change = 0
        
        analysis = f"""
        Price Trend Analysis ({years} years):
        - Location: {town if town else 'All Towns'}
        - Flat Type: {flat_type if flat_type else 'All Types'}
        - Total transactions: {len(filtered_df):,}
        - Average price: ${filtered_df['resale_price'].mean():,.0f}
        - Price range: ${filtered_df['resale_price'].min():,.0f} - ${filtered_df['resale_price'].max():,.0f}
        - {years}-year change: {total_change:+.1f}%
        - Recent 12-month trend: {recent_change:+.1f}%
        - Current average price per sqm: ${filtered_df['price_per_sqm'].mean():,.0f}
        """
        
        return analysis
        
    except Exception as e:
        return f"Error in price trend analysis: {str(e)}"


@tool
def compare_locations(locations: list, flat_type: str = None) -> str:
    """
    Compare average prices across multiple locations.
    
    Args:
        locations: List of town names to compare
        flat_type: Specific flat type to compare (optional)
    
    Returns:
        String containing comparison results
    """
    try:
        df = load_hdb_data()
        if df.empty:
            return "No data available for analysis."
        
        # Filter by flat type if specified
        if flat_type:
            df = df[df['flat_type'].str.upper() == flat_type.upper()]
        
        comparison_data = []
        
        for location in locations:
            location_data = df[df['town'].str.upper() == location.upper()]
            if not location_data.empty:
                comparison_data.append({
                    'Location': location,
                    'Avg_Price': location_data['resale_price'].mean(),
                    'Avg_Price_Per_Sqm': location_data['price_per_sqm'].mean(),
                    'Transaction_Count': len(location_data),
                    'Price_Range': f"${location_data['resale_price'].min():,.0f} - ${location_data['resale_price'].max():,.0f}"
                })
        
        if not comparison_data:
            return "No data found for the specified locations."
        
        # Sort by average price
        comparison_data.sort(key=lambda x: x['Avg_Price'], reverse=True)
        
        result = f"Location Comparison ({flat_type if flat_type else 'All Flat Types'}):\n\n"
        
        for i, data in enumerate(comparison_data, 1):
            result += f"{i}. {data['Location']}\n"
            result += f"   Average Price: ${data['Avg_Price']:,.0f}\n"
            result += f"   Price per sqm: ${data['Avg_Price_Per_Sqm']:,.0f}\n"
            result += f"   Transactions: {data['Transaction_Count']:,}\n"
            result += f"   Range: {data['Price_Range']}\n\n"
        
        return result
        
    except Exception as e:
        return f"Error in location comparison: {str(e)}"


@tool
def analyze_flat_characteristics(town: str = None, flat_type: str = None) -> str:
    """
    Analyze how flat characteristics affect pricing.
    
    Args:
        town: Specific town to analyze (optional)
        flat_type: Specific flat type to analyze (optional)
    
    Returns:
        String containing characteristic analysis
    """
    try:
        df = load_hdb_data()
        if df.empty:
            return "No data available for analysis."
        
        # Filter data
        filtered_df = df.copy()
        if town:
            filtered_df = filtered_df[filtered_df['town'].str.upper() == town.upper()]
        if flat_type:
            filtered_df = filtered_df[filtered_df['flat_type'].str.upper() == flat_type.upper()]
        
        if filtered_df.empty:
            return "No data found for the specified criteria."
        
        analysis = f"Flat Characteristics Analysis:\n"
        analysis += f"Location: {town if town else 'All Towns'}\n"
        analysis += f"Flat Type: {flat_type if flat_type else 'All Types'}\n\n"
        
        # Storey range analysis
        storey_analysis = filtered_df.groupby('storey_range').agg({
            'resale_price': ['mean', 'count'],
            'price_per_sqm': 'mean'
        }).round(0)
        
        analysis += "Price by Storey Range:\n"
        for storey in storey_analysis.index:
            avg_price = storey_analysis.loc[storey, ('resale_price', 'mean')]
            count = storey_analysis.loc[storey, ('resale_price', 'count')]
            price_per_sqm = storey_analysis.loc[storey, ('price_per_sqm', 'mean')]
            analysis += f"  {storey}: ${avg_price:,.0f} (${price_per_sqm:,.0f}/sqm, {count} transactions)\n"
        
        # Floor area analysis
        analysis += f"\nFloor Area Statistics:\n"
        analysis += f"  Average: {filtered_df['floor_area_sqm'].mean():.1f} sqm\n"
        analysis += f"  Range: {filtered_df['floor_area_sqm'].min():.1f} - {filtered_df['floor_area_sqm'].max():.1f} sqm\n"
        
        # Lease analysis
        analysis += f"\nLease Information:\n"
        analysis += f"  Average remaining lease: {filtered_df['remaining_lease_years'].mean():.1f} years\n"
        analysis += f"  Range: {filtered_df['remaining_lease_years'].min():.1f} - {filtered_df['remaining_lease_years'].max():.1f} years\n"
        
        return analysis
        
    except Exception as e:
        return f"Error in characteristic analysis: {str(e)}"


@tool
def get_market_insights(town: str = None, flat_type: str = None) -> str:
    """
    Generate market insights and recommendations.
    
    Args:
        town: Specific town to analyze (optional)
        flat_type: Specific flat type to analyze (optional)
    
    Returns:
        String containing market insights
    """
    try:
        df = load_hdb_data()
        if df.empty:
            return "No data available for analysis."
        
        # Filter data
        filtered_df = df.copy()
        if town:
            filtered_df = filtered_df[filtered_df['town'].str.upper() == town.upper()]
        if flat_type:
            filtered_df = filtered_df[filtered_df['flat_type'].str.upper() == flat_type.upper()]
        
        if filtered_df.empty:
            return "No data found for the specified criteria."
        
        # Recent data (last 2 years)
        recent_cutoff = filtered_df['month'].max() - pd.DateOffset(years=2)
        recent_df = filtered_df[filtered_df['month'] >= recent_cutoff]
        
        insights = f"Market Insights:\n"
        insights += f"Location: {town if town else 'All Towns'}\n"
        insights += f"Flat Type: {flat_type if flat_type else 'All Types'}\n\n"
        
        # Transaction volume
        total_transactions = len(filtered_df)
        recent_transactions = len(recent_df)
        insights += f"Transaction Volume:\n"
        insights += f"  Total transactions: {total_transactions:,}\n"
        insights += f"  Recent 2 years: {recent_transactions:,}\n"
        
        # Price percentiles
        p25 = filtered_df['resale_price'].quantile(0.25)
        p50 = filtered_df['resale_price'].quantile(0.50)
        p75 = filtered_df['resale_price'].quantile(0.75)
        
        insights += f"\nPrice Distribution:\n"
        insights += f"  25th percentile: ${p25:,.0f}\n"
        insights += f"  Median: ${p50:,.0f}\n"
        insights += f"  75th percentile: ${p75:,.0f}\n"
        
        # Most active periods
        monthly_counts = filtered_df.groupby(filtered_df['month'].dt.to_period('M')).size()
        peak_month = monthly_counts.idxmax()
        insights += f"\nMarket Activity:\n"
        insights += f"  Peak transaction month: {peak_month}\n"
        insights += f"  Peak transactions: {monthly_counts.max()} units\n"
        
        # Value recommendations
        avg_price_per_sqm = filtered_df['price_per_sqm'].mean()
        good_value_threshold = avg_price_per_sqm * 0.9  # 10% below average
        
        insights += f"\nValue Indicators:\n"
        insights += f"  Average price per sqm: ${avg_price_per_sqm:,.0f}\n"
        insights += f"  Good value threshold: <${good_value_threshold:,.0f}/sqm\n"
        
        return insights
        
    except Exception as e:
        return f"Error generating market insights: {str(e)}"


def create_analytics_agent():
    """Create and configure the analytics agent with custom tools"""
    try:
        # Load environment variables
        # load_dotenv()
        OPENAI_KEY = st.secrets.get("OPENAI_API_KEY")
        
        if not OPENAI_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Create the model
        model = "gpt-4o-mini"
        agent_model = OpenAIServerModel(model_id=model, api_key=OPENAI_KEY)
        
        # Define custom tools
        custom_tools = [
            analyze_price_trends,
            compare_locations,
            analyze_flat_characteristics,
            get_market_insights
        ]
        
        # Create agent with custom tools
        agent = CodeAgent(
            tools=custom_tools,
            model=agent_model,
            add_base_tools=True,
            additional_authorized_imports=[
                "pandas", "numpy", "datetime", "matplotlib", "plotly", "seaborn"
            ],
            max_steps=5
        )
        
        print(f"Analytics agent created successfully with {len(custom_tools)} custom tools")
        return agent
        
    except Exception as e:
        print(f"Error creating analytics agent: {str(e)}")
        raise


def query_analytics_agent(agent, question: str, conversation_context: str = "") -> str:
    """
    Query the analytics agent with enhanced prompts for HDB price analysis
    
    Args:
        agent: The configured analytics agent
        question: User's question
        conversation_context: Previous conversation context
    
    Returns:
        Agent's response
    """
    try:
        # Enhanced system prompt for price analysis
        system_prompt = """
        You are a specialized HDB Resale Price Analysis expert with access to comprehensive Singapore HDB resale transaction data.
        
        Your data contains these columns:
        - month: Transaction date
        - town: Location/town name
        - flat_type: Type of flat (1 ROOM, 2 ROOM, 3 ROOM, 4 ROOM, 5 ROOM, EXECUTIVE)
        - block: Block number
        - street_name: Street name
        - storey_range: Floor level range (e.g., "01 TO 03", "04 TO 06")
        - floor_area_sqm: Floor area in square meters
        - flat_model: Flat model type
        - lease_commence_date: Year the lease started
        - resale_price: Transaction price in SGD
        
        Available analysis tools:
        1. analyze_price_trends() - Analyze price trends over time
        2. compare_locations() - Compare prices across different towns
        3. analyze_flat_characteristics() - Analyze how flat features affect pricing
        4. get_market_insights() - Generate comprehensive market insights
        
        When answering questions:
        1. Use the appropriate tools based on the user's query
        2. Provide specific data-backed insights
        3. Include relevant price ranges, trends, and comparisons
        4. Consider factors like location, flat type, storey range, and lease remaining
        5. Offer practical advice for buyers/sellers when appropriate
        
        Always cite specific numbers and trends from the data in your responses.
        """
        
        # Combine context and question
        full_prompt = f"""
        {system_prompt}
        
        {conversation_context}
        
        User Question: {question}
        
        Please provide a comprehensive analysis using the available tools and data.


        GUIDELINES:
        - Present your answer in a clear, concise paragraph format.
        - Present data in a structured way, and proper formatting.
        - Answer in a professional and helpful manner.
        """
        
        # Query the agent
        response = agent.run(full_prompt)
        return response
        
    except Exception as e:
        return f"Error querying analytics agent: {str(e)}"


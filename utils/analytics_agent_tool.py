import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from smolagents import tool, Tool, CodeAgent, OpenAIServerModel


# Load HDB resale price data
# Method 1: Load single CSV (current approach)
df = pd.read_csv('data/csv/ResaleflatpricesbasedonregistrationdatefromJan2017onwards.csv')

# Remove remaining_lease column
df = df.drop('remaining_lease', axis=1)


# Method 4: Load and combine with source tracking
csv_files = ['data/csv/ResaleFlatPricesBasedonApprovalDate2000Feb2012.csv', 
             'data/csv/ResaleFlatPricesBasedonApprovalDate19901999.csv',
             'data/csv/ResaleFlatPricesBasedonRegistrationDateFromMar2012toDec2014.csv']
csv_remaining_lease_files = ['data/csv/ResaleFlatPricesBasedonRegistrationDateFromJan2015toDec2016.csv',
                             'data/csv/ResaleFlatPricesBasedonRegistrationDateFromJan2017onwards.csv']
df_list = []

for i, file in enumerate(csv_files):
    temp_df = pd.read_csv(file)
    temp_df['source_file'] = file  # Add source tracking
    df_list.append(temp_df)
    
for i, file in enumerate(csv_remaining_lease_files):
    temp_df = pd.read_csv(file)
    temp_df = temp_df.drop('remaining_lease', axis=1)  # Remove column
    temp_df['source_file'] = file  # Add source tracking
    df_list.append(temp_df)    

df = pd.concat(df_list, ignore_index=True)


def create_analytics_agent():
    # Load environment variables
    load_dotenv()
    OPENAI_KEY = os.getenv('OPENAI_API_KEY')
    
    if not OPENAI_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Load an agent model
    model = "gpt-4o-mini"  # Fixed model name
    
    # Create the model for the agent to use
    agent_model = OpenAIServerModel(model_id=model, api_key=OPENAI_KEY)
    
    # agent = CodeAgent(tools, model=agent_model, add_base_tools=False, max_steps=5)

    agent = CodeAgent(
    tools=[],  # Empty list since we'll use built-in tools only
    model=agent_model,  # Connect to our GPT-4 Mini model
    add_base_tools=True,  # Enable standard Python execution capabilities
    additional_authorized_imports=[  # SECURITY: Strictly limit allowed libraries
        "pandas", "numpy", "datetime",
        "matplotlib", "plotly", "seaborn", "sklearn"]
    )

    print(f"Agent created with model: {model}")
    return agent

# System Prompt for Price Analysis Agent
SYSTEM_PROMPT = """You are a HDB Resale Price Analysis Specialist. 
Your role is to:
1. Analyze historical price trends
2. Identify price patterns
3. Consider location factors
4. Account for flat characteristics
5. Provide data-backed insights

Base all analysis on the provided resale transaction data."""

# Chain of Analysis Prompts
ANALYSIS_CHAIN = [
    {
        "role": "price_analyzer",
        "prompt": """Analyze the following aspects for {location} and {flat_type}:
        1. Price trends over past {timeframe}
        2. Price variations by storey range
        3. Impact of remaining lease
        4. Comparison with similar units"""
    },
    {
        "role": "insight_generator",
        "prompt": """Based on the analysis, provide:
        1. Key price factors
        2. Notable patterns
        3. Market position
        4. Value indicators"""
    },
    {
        "role": "advisor",
        "prompt": """Generate recommendations considering:
        1. Price trends
        2. Market timing
        3. Value proposition
        4. Risk factors"""
    }
]


def query_analytics_agent(agent, question):
    prompt = f"""
    ## Instructions
    You are acting as a expert data analyst.
    Given a pandas DataFrame.

    ## Analytics Steps
    1. Load the provided CSV file into a pandas DataFrame.
    2. Analyse the trends in the data.
    3. Provide a summary of the findings.

    ## Data information
    # [Provide column names, data types (numerical/categorical), and brief descriptions here]

    ## User Question:
    {question}
    """
    return agent.run(prompt)
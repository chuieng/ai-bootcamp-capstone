import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="About Us - HDB Resale Assistant",
    page_icon="ℹ️"
)

st.title('ℹ️ About Us')

# Project Overview Section
st.header("🏠 Project Overview")
st.markdown("""
Welcome to the **HDB Resale Assistant** - an AI-powered application designed to simplify and enhance the HDB resale flat buying process in Singapore. This comprehensive platform combines cutting-edge artificial intelligence with extensive data analysis to provide users with intelligent assistance throughout their HDB resale journey.

Our application serves as your trusted digital companion, offering expert guidance on complex procedures, market insights, and data-driven recommendations to help you make informed decisions in Singapore's HDB resale market.
""")

# Project Scope Section
st.header("🎯 Project Scope")
st.markdown("""
This project encompasses two main areas of the HDB resale ecosystem:

### 1. **Process Guidance & Documentation**
- Comprehensive guidance through HDB resale procedures
- Intelligent document analysis and information retrieval
- Step-by-step assistance for buyers and sellers
- Policy clarifications and regulatory compliance support

### 2. **Market Analysis & Price Intelligence**
- Historical price trend analysis spanning over 30 years (1990-present)
- Location-based market insights and comparisons
- Budget optimization and affordability assessments
- Predictive analytics for future market trends
""")

# Objectives Section
st.header("🎪 Project Objectives")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### **Primary Objectives**
    - **Democratize Information Access**: Make complex HDB policies and procedures easily accessible to all users
    - **Enhance Decision Making**: Provide data-driven insights for better purchasing decisions
    - **Streamline Process**: Simplify the traditionally complex HDB resale process
    - **Reduce Information Asymmetry**: Bridge knowledge gaps between buyers, sellers, and industry professionals
    """)

with col2:
    st.markdown("""
    ### **Secondary Objectives**
    - **Educational Enhancement**: Improve public understanding of HDB policies and market dynamics
    - **Technology Innovation**: Demonstrate practical applications of AI in real estate
    - **User Empowerment**: Enable users to become more informed and confident participants in the market
    - **Process Optimization**: Identify inefficiencies and suggest improvements in current procedures
    """)

# Data Sources Section
st.header("📊 Data Sources")
st.markdown("""
Our application leverages comprehensive and authoritative data sources to ensure accuracy and reliability:
""")

tab1, tab2 = st.tabs(["📈 Transactional Data", "📋 Policy Documents"])

with tab1:
    st.markdown("""
    ### **HDB Resale Transaction Data**
    Our price analysis engine utilizes official HDB resale transaction datasets covering:
    
    - **1990-1999**: Resale Flat Prices (Approval Date basis) - Foundation historical data
    - **2000-2012**: Resale Flat Prices (Approval Date basis) - Pre-COV era transactions
    - **2012-2014**: Resale Flat Prices (Registration Date basis) - COV introduction period
    - **2015-2016**: Resale Flat Prices (Registration Date basis) - Market stabilization
    - **2017-Present**: Resale Flat Prices (Registration Date basis) - Current market dynamics
    
    **Total Dataset Coverage**: Over 800,000 transactions spanning 30+ years
    
    **Data Fields Include**:
    - Transaction dates and prices
    - Flat types and floor areas
    - Location details (town, street name, block)
    - Lease commencement dates
    - Storey ranges
    """)

with tab2:
    st.markdown("""
    ### **Official HDB Policy Documents**
    Our knowledge base incorporates official HDB documentation:
    
    - **📋 Overview**: General introduction to HDB resale processes
    - **🏗️ Buying Procedure**: Step-by-step purchasing guidelines
    - **📋 Option to Purchase**: OTP procedures and requirements
    - **💰 Mode of Financing**: Financing options and loan procedures
    - **🏠 Managing Flat Purchase**: Post-purchase management guidelines
    - **📏 Planning Considerations**: Space planning and renovation guidelines
    - **📊 Request for Value**: Property valuation procedures
    - **🏘️ EIP & SPR Quota**: Ethnic Integration Policy and quota information
    """)

# Features Section
st.header("🚀 Key Features")

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    ### **🤖 HDB Resale Process Assistant**
    
    **Intelligent Document Q&A**
    - Natural language querying of HDB policies
    - Context-aware responses with source citations
    - Multi-document cross-referencing
    - Real-time policy interpretation
    
    **Process Guidance**
    - Step-by-step procedure walkthroughs
    - Requirement checklists and timelines
    - Common pitfall warnings
    - Personalized advice based on user scenarios
    
    **Technology Stack**
    - ChromaDB for efficient document retrieval
    - OpenAI GPT models for intelligent responses
    - RAG (Retrieval-Augmented Generation) architecture
    - Streamlit for interactive user experience
    """)

with feature_col2:
    st.markdown("""
    ### **📈 Price Analysis & Market Insights**
    
    **Advanced Analytics Engine**
    - Multi-dimensional price trend analysis
    - Location-based market comparisons
    - Statistical modeling and forecasting
    - Interactive data visualizations
    
    **Intelligent Market Insights**
    - Budget optimization recommendations
    - Affordability assessments
    - Market timing advice
    - Investment potential analysis
    
    **Technology Stack**
    - Pandas for data processing
    - AI agents for intelligent analysis
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<b>HDB Resale Assistant</b><br>
AI Champions Bootcamp Capstone Project<br>
© 2025 - Educational Use Only
</div>
""", unsafe_allow_html=True)
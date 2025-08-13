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
    - Pandas and NumPy for data processing
    - Plotly and Matplotlib for visualizations
    - Statistical modeling libraries
    - AI agents for intelligent analysis
    """)

# Technical Architecture Section
st.header("⚙️ Technical Architecture")
st.markdown("""
Our application is built on a robust, scalable architecture leveraging modern AI and data science technologies:
""")

arch_col1, arch_col2, arch_col3 = st.columns(3)

with arch_col1:
    st.markdown("""
    ### **🤖 AI & Machine Learning**
    - **OpenAI GPT Models**: Advanced language understanding and generation
    - **Sentence Transformers**: Semantic document embeddings
    - **RAG Architecture**: Retrieval-Augmented Generation for accurate responses
    - **Agent-based Systems**: Specialized AI agents for different domains
    """)

with arch_col2:
    st.markdown("""
    ### **📊 Data Processing**
    - **Pandas**: Efficient data manipulation and analysis
    - **NumPy**: Numerical computing and statistical operations
    - **ChromaDB**: Vector database for semantic search
    - **SQLAlchemy**: Database abstraction and management
    """)

with arch_col3:
    st.markdown("""
    ### **🖥️ User Interface**
    - **Streamlit**: Interactive web application framework
    - **Plotly**: Dynamic and interactive visualizations
    - **Matplotlib/Seaborn**: Statistical plotting and charts
    - **Responsive Design**: Multi-device compatibility
    """)

# Team & Development Section
st.header("👥 Development Information")
st.markdown("""
### **Project Development**
This application was developed as part of the **AI Champions Bootcamp Capstone Project**, demonstrating practical applications of artificial intelligence in solving real-world problems in Singapore's housing market.

### **Development Approach**
- **User-Centric Design**: Focused on solving real user problems and pain points
- **Data-Driven Development**: Extensive analysis of user needs and market requirements
- **Iterative Improvement**: Continuous refinement based on testing and feedback
- **Ethical AI Practices**: Responsible development with transparency and user safety in mind

### **Educational Purpose**
This application serves as a prototype and educational tool, demonstrating the potential of AI in real estate technology while providing valuable insights into Singapore's HDB market dynamics.
""")

# Important Notice Section
st.header("⚠️ Important Notice")
st.warning("""
**EDUCATIONAL PROTOTYPE DISCLAIMER**

This web application is a prototype developed for educational purposes only. The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, especially those related to financial, legal, or real estate matters.

Please be aware that:
- AI models may generate inaccurate or incorrect information
- Market data may not reflect current conditions
- Legal and financial advice should be obtained from qualified professionals
- Users assume full responsibility for how they use any generated output

Always consult with qualified real estate professionals, lawyers, and financial advisors for accurate and personalized advice regarding HDB transactions.
""")

# Contact & Feedback Section
st.header("📧 Feedback & Contact")
st.markdown("""
We value your feedback and suggestions for improving this application. As this is an educational project, your insights help us understand the potential and limitations of AI applications in real estate technology.

For any questions about this project or its technical implementation, please feel free to reach out through the appropriate academic channels.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<b>HDB Resale Assistant</b><br>
AI Champions Bootcamp Capstone Project<br>
Powered by OpenAI, Streamlit, and ChromaDB<br>
© 2024 - Educational Use Only
</div>
""", unsafe_allow_html=True)
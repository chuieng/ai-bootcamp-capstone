import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    layout="wide",
    page_title="Methodology - HDB Resale Assistant",
    page_icon="⚙️"
)

st.title('⚙️ Methodology')

# Use Case Flowcharts
st.header("🔄 Use Case Implementation Flows")

# Use Case 1: Document Q&A System
st.subheader("Use Case 1: HDB Document Q&A System (RAG-based)")

st.markdown("""
This use case enables users to ask natural language questions about HDB policies and procedures, receiving accurate answers sourced from official documentation.

### **Technical Implementation:**
- **Architecture**: Retrieval-Augmented Generation (RAG)
- **Vector Database**: ChromaDB with persistent storage
- **Embedding Model**: BAAI/bge-small-en-v1.5
- **LLM**: OpenAI GPT-4o-mini with specialized system prompts
- **Agent Framework**: SmolagentS with custom tools
            
#### **Document Data (PDF Processing)**
- **Source**: 8 official HDB policy documents
- **Processing**: PyPDFLoader → Text extraction → Chunking (300 chars)
- **Storage**: ChromaDB vector database with BGE embeddings
""")

st.image("documentation/UserCase1.png")


# Use Case 2: Price Analysis System
st.subheader("Use Case 2: HDB Price Analysis & Market Insights (Agent-based)")

st.markdown("""
This use case provides intelligent analysis of HDB resale market data, offering insights on price trends, location comparisons, and budget recommendations through specialized AI agents.

### **Technical Implementation:**
- **Architecture**: Multi-agent system with specialized analytical tools
- **Data Processing**: Real-time statistical analysis on 800K+ transactions
- **AI Agents**: Task-specific agents for different analytical functions
- **Statistical Models**: Trend analysis, correlation studies, predictive modeling
            
#### **Transactional Data (CSV Processing)**
- **Source**: 5 HDB datasets spanning 1990-present
- **Volume**: 800,000+ transaction records
- **Processing**: Schema harmonization, type conversion, feature engineering
- **Storage**: In-memory pandas DataFrames with caching
""")

st.image("documentation/UserCase2.png")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
<b>Methodology Documentation</b><br>
HDB Resale Assistant - Technical Implementation Guide<br>
AI Champions Bootcamp Capstone Project<br>
© 2025 - Educational Use Only
</div>
""", unsafe_allow_html=True)
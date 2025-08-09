import streamlit as st
import sys
import os

# Add the utils directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from analytics_agent_tool_new import create_analytics_agent, query_analytics_agent, load_hdb_data
from utils.helper import sanitize_response

# Title
st.set_page_config(
    layout="wide",
    page_title="HDB Resale Price Analysis and Insights",
    page_icon="🏠"
)

st.title("🏠 HDB Resale Price Analysis and Insights")
st.markdown("*Powered by AI Agent with comprehensive HDB resale data analysis*")

# # Sidebar for quick filters and info
# with st.sidebar:
#     st.header("📊 Data Overview")
    
#     # Load and display data summary
#     try:
#         df = load_hdb_data()
#         if not df.empty:
#             st.metric("Total Transactions", f"{len(df):,}")
#             st.metric("Date Range", f"{df['month'].min().strftime('%Y-%m')} to {df['month'].max().strftime('%Y-%m')}")
#             st.metric("Towns Covered", df['town'].nunique())
#             st.metric("Flat Types", df['flat_type'].nunique())
            
#             # Quick stats
#             st.subheader("💰 Price Statistics")
#             st.write(f"**Average Price:** ${df['resale_price'].mean():,.0f}")
#             st.write(f"**Median Price:** ${df['resale_price'].median():,.0f}")
#             st.write(f"**Price Range:** ${df['resale_price'].min():,.0f} - ${df['resale_price'].max():,.0f}")
            
#         else:
#             st.error("No data available")
#     except Exception as e:
#         st.error(f"Error loading data: {str(e)}")
    
#     st.markdown("---")
#     st.subheader("💡 Analysis Examples")
#     st.markdown("""
#     **Try asking:**
#     - "What are the price trends for 4-room flats in Tampines?"
#     - "Compare prices between Bishan and Toa Payoh"
#     - "How does storey range affect pricing in Punggol?"
#     - "What are the market insights for executive flats?"
#     - "Show me price trends over the last 3 years"
#     """)

# Main content area
# col1, col2 = st.columns([2, 1])

# with col2:
#     st.subheader("🎯 Quick Analysis")
    
#     # Quick analysis buttons
#     if st.button("📈 Overall Market Trends", use_container_width=True):
#         with st.spinner("Analyzing market trends..."):
#             if 'agent' not in st.session_state:
#                 st.session_state.agent = create_analytics_agent()
#             response = query_analytics_agent(st.session_state.agent, "Analyze the overall HDB resale market trends over the past 5 years")
#             st.info(sanitize_response(response))
    
#     if st.button("🏘️ Popular Locations", use_container_width=True):
#         with st.spinner("Analyzing popular locations..."):
#             if 'agent' not in st.session_state:
#                 st.session_state.agent = create_analytics_agent()
#             response = query_analytics_agent(st.session_state.agent, "Compare the top 5 most expensive and most affordable towns for HDB resale")
#             st.info(sanitize_response(response))
    
#     if st.button("📏 Flat Size Impact", use_container_width=True):
#         with st.spinner("Analyzing flat characteristics..."):
#             if 'agent' not in st.session_state:
#                 st.session_state.agent = create_analytics_agent()
#             response = query_analytics_agent(st.session_state.agent, "Analyze how different flat types and sizes affect pricing across Singapore")
#             st.info(sanitize_response(response))

# with col1:
st.subheader("💬 Chat with HDB Price Analyst")

# Add welcome message
st.write("""Hello! I'm your HDB Resale Price Analysis specialist. I have access to comprehensive Singapore HDB resale transaction data.

I can help you with:
- 📈 Price trends analysis for specific locations and flat types
- 🏘️ Location comparisons and recommendations  
- 🏠 Impact of flat characteristics on pricing
- 💡 Market insights and value indicators
- 📊 Historical data analysis and forecasting

What would you like to know about the HDB resale market?""")

# Create a session state variable to store the chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create a chat input field to allow the user to enter a message
if prompt := st.chat_input("What would you like to ask about HDB prices?"):

    # Store and display the current prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a response using the analytics agent
    with st.chat_message("assistant"):
        with st.spinner("Analyzing HDB data..."):
            try:
                # Create agent if not in session state
                if 'agent' not in st.session_state:
                    st.session_state.agent = create_analytics_agent()
                
                # Build context from conversation history
                conversation_context = ""
                if len(st.session_state.messages) > 1:  # If there are previous messages
                    conversation_context = "\nPrevious conversation:\n"
                    # Get last few messages for context (excluding the current user message)
                    recent_messages = st.session_state.messages[-6:-1]  # Last 3 exchanges
                    for msg in recent_messages:
                        role = "User" if msg["role"] == "user" else "Assistant"
                        conversation_context += f"{role}: {msg['content']}\n"
                
                # Query the analytics agent
                response = query_analytics_agent(st.session_state.agent, prompt, conversation_context)
                sanitized_response = sanitize_response(response)
                st.write(sanitized_response)
                
                # Store the response
                st.session_state.messages.append({"role": "assistant", "content": sanitized_response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Additional features
# st.markdown("---")
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.subheader("📋 Recent Data Sample")
#     try:
#         df = load_hdb_data()
#         if not df.empty:
#             # Show recent transactions
#             recent_data = df.nlargest(10, 'month')[['month', 'town', 'flat_type', 'resale_price', 'price_per_sqm']]
#             recent_data['resale_price'] = recent_data['resale_price'].apply(lambda x: f"${x:,.0f}")
#             recent_data['price_per_sqm'] = recent_data['price_per_sqm'].apply(lambda x: f"${x:,.0f}")
#             st.dataframe(recent_data, hide_index=True)
#     except Exception as e:
#         st.error(f"Error displaying data: {str(e)}")

# with col2:
#     st.subheader("🏆 Top Towns by Volume")
#     try:
#         df = load_hdb_data()
#         if not df.empty:
#             top_towns = df.groupby('town').size().nlargest(10)
#             for town, count in top_towns.items():
#                 st.write(f"**{town}:** {count:,} transactions")
#     except Exception as e:
#         st.error(f"Error displaying top towns: {str(e)}")

# with col3:
#     st.subheader("💎 Flat Type Distribution")
#     try:
#         df = load_hdb_data()
#         if not df.empty:
#             flat_types = df['flat_type'].value_counts()
#             for flat_type, count in flat_types.items():
#                 percentage = (count / len(df)) * 100
#                 st.write(f"**{flat_type}:** {percentage:.1f}% ({count:,})")
#     except Exception as e:
#         st.error(f"Error displaying flat types: {str(e)}")

# Footer
st.markdown("---")
st.markdown("*This analysis is powered by AI and based on historical HDB resale transaction data. Always consult with property professionals for investment decisions.*")


import streamlit as st
import sys
import os
from utils.check_pw import check_password

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

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("🏠 HDB Resale Price Analysis and Insights")

# Welcome message
st.write("""Hello! I'm your HDB Resale Price Analysis specialist. I have access to comprehensive Singapore HDB resale transaction data.

I can help you with:
- 📈 Price trends analysis for specific locations and flat types
- 🏘️ Location comparisons and recommendations  
- 🏠 Impact of flat characteristics on pricing
- 💡 Market insights and value indicators
- 📊 Historical data analysis and forecasting

Example questions: "What are the price trends for 4-room flats in Bukit Timah?" or "With a budget of $400k can I get a 4-room flat in Tampines?" or "Which area is cheaper in price? Tampines or Woodland 3-room flat?".""")

# Create a session state variable to store the chat messages
if "price_ai_messages" not in st.session_state:
    st.session_state.price_ai_messages = []

# Display the existing chat messages
for message in st.session_state.price_ai_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create a chat input field to allow the user to enter a message
if prompt := st.chat_input("What would you like to know about the HDB resale market?"):

    # Store and display the current prompt
    st.session_state.price_ai_messages.append({"role": "user", "content": prompt})
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
                if len(st.session_state.price_ai_messages) > 1:  # If there are previous messages
                    conversation_context = "\nPrevious conversation:\n"
                    # Get last few messages for context (excluding the current user message)
                    recent_messages = st.session_state.price_ai_messages[-6:-1]  # Last 3 exchanges
                    for msg in recent_messages:
                        role = "User" if msg["role"] == "user" else "Assistant"
                        conversation_context += f"{role}: {msg['content']}\n"
                
                # Query the analytics agent
                response = query_analytics_agent(st.session_state.agent, prompt, conversation_context)
                sanitized_response = sanitize_response(response)
                st.write(sanitized_response)
                
                # Store the response
                st.session_state.price_ai_messages.append({"role": "assistant", "content": sanitized_response})
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.price_ai_messages.append({"role": "assistant", "content": error_msg})
# Footer
st.markdown("---")
st.markdown("*This analysis is powered by AI and based on historical HDB resale transaction data. Always consult with property professionals for investment decisions.*")


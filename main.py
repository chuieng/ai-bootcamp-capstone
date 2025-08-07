import streamlit as st
import chromadb
import os

from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils import embedding_functions
from utils.agent_tool import create_agent, query_agent

# Initialize ChromaDB collection in session state
if 'hdb_documents_collection' not in st.session_state:
    # Connect to persistent ChromaDB client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create the same embedding function used during collection creation
    embed_model_name = "BAAI/bge-small-en-v1.5"
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model_name)
    
    # Get the existing collection and store in session state
    st.session_state.hdb_documents_collection = client.get_collection(name="hdb_documents", embedding_function=embed_func)

# agent = create_agent()
# response = query_agent(agent, "What is Option to Purchase?")
# print(f"hihi Response from agent is ...: {response}")
# st.set_page_config(
#     layout="centered",
#     page_title="HDB Resale Assistant"
# )

st.title("HDB Resale Process Assistant")

load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
 # Create an OpenAI client.
client = OpenAI(api_key=OPENAI_KEY)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What would you like to ask?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


# mass comment below

# # Welcome message
# st.markdown("### Welcome! How can I help you today?")
# st.write("")

# # Main options as bullet list
# # st.markdown("""
# # - 📊 Price Analysis & Insights
# # - ✅ Eligibility & Requirements
# # """)

# # Create three columns for the main action buttons
# col1, col2, col3 = st.columns(3)

# # Initialize session state for price analysis visibility
# if 'show_price_analysis' not in st.session_state:
#     st.session_state.show_price_analysis = False

# with col1:
#     if st.button("📊 Price Analysis & Insights", use_container_width=True):
#         st.session_state.show_price_analysis = not st.session_state.show_price_analysis

# with col2:
#     if st.button("✅ Eligibility & Requirements", use_container_width=True):
#         st.success("You selected Eligibility & Requirements!")

# with col3:
#     if st.button("📋 Process Guidelines", use_container_width=True):
#         st.success("You selected Process Guidelines!")
        
#         # Load and process HDB documents using RAG functions
#         with st.spinner("Loading HDB documents..."):
#             try:
#                 # Process HDB documents and get chunks
#                 chunks = process_hdb_documents(print_info=False)  # Don't print to console in Streamlit
                
#                 st.success(f"Successfully loaded {len(chunks)} document chunks!")
                
#                 # Display some chunk information
#                 if chunks:
#                     st.write("**Document Processing Summary:**")
#                     st.write(f"- Total chunks: {len(chunks)}")
#                     st.write(f"- First chunk preview: {chunks[0].page_content[:200]}...")
                    
#                     # Optionally show more details in an expander
#                     with st.expander("View chunk details"):
#                         for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
#                             st.write(f"**Chunk {i+1}:**")
#                             st.write(f"Content: {chunk.page_content[:150]}...")
#                             if hasattr(chunk, 'metadata'):
#                                 st.write(f"Metadata: {chunk.metadata}")
#                             st.write("---")
                            
#             except Exception as e:
#                 st.error(f"Error loading documents: {str(e)}")

# st.write("")

# # Show/hide Price Analysis & Insights section based on button state
# if st.session_state.show_price_analysis:
#     #START: Price Analysis & Insights
#     # Filter options
#     st.markdown("**Select Location:**")
#     towns = ["All Towns", "Ang Mo Kio", "Bedok", "Bishan", "Bukit Batok", "Bukit Merah", 
#              "Bukit Panjang", "Bukit Timah", "Central Area", "Choa Chu Kang", "Clementi",
#              "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang/Whampoa",
#              "Marine Parade", "Pasir Ris", "Punggol", "Queenstown", "Sembawang",
#              "Sengkang", "Serangoon", "Tampines", "Toa Payoh", "Woodlands", "Yishun"]
#     selected_town = st.selectbox("Choose a town", towns, label_visibility="collapsed")

#     st.write("")
#     st.markdown("**Flat Type:**")
#     flat_col1, flat_col2, flat_col3, flat_col4, flat_col5, flat_col6, flat_col7 = st.columns(7)
#     with flat_col1:
#         room_1 = st.checkbox("1-Room")
#     with flat_col2:
#         room_2 = st.checkbox("2-Room")
#     with flat_col3:
#         room_3 = st.checkbox("3-Room")
#     with flat_col4:
#         room_4 = st.checkbox("4-Room")
#     with flat_col5:
#         room_5 = st.checkbox("5-Room")
#     with flat_col6:
#         executive = st.checkbox("Executive")
#     with flat_col7:
#         multi_gen = st.checkbox("Multi-Generation")

#     st.write("")
#     st.markdown("**Price Range:**")
#     price_range = st.slider("Price range selector", min_value=300000, max_value=1500000, value=(300000, 1500000), 
#                             format="$%d", label_visibility="collapsed")
#     st.write(f"Selected range: ${price_range[0]:,} - ${price_range[1]:,}")

#     #add a button "Analyze" to show the analysis results
#     if st.button("Analyze", use_container_width=True):
#         st.success("Analysis results will be displayed here!")
#         # Here you can add the logic to perform the analysis based on selected filters
#         # For now, we will just display a placeholder message
#         st.write(f"Analyzing resale prices for {selected_town} with the following criteria:")
#         st.write(f"- Flat Types: {', '.join([ft for ft, sel in zip(['1-Room', '2-Room', '3-Room', '4-Room', '5-Room', 'Executive', 'Multi-Generation'], 
#                                                             [room_1, room_2, room_3, room_4, room_5, executive, multi_gen]) if sel])}")
#         st.write(f"- Price Range: ${price_range[0]:,} - ${price_range[1]:,}")
#     #END: Price Analysis & Insights

# st.write("")
import streamlit as st
from utils.rag import process_all_hdb_documents, process_hdb_documents, load_and_split_pdf, print_chunk_info

# to call the utility functions in rag.py
process_all_hdb_documents(True)

st.set_page_config(
    layout="centered",
    page_title="HDB Resale Assistant"
)

st.title("HDB Resale Assistant")

# Welcome message
st.markdown("### Welcome! How can I help you today?")
st.write("")

# Main options as bullet list
# st.markdown("""
# - 📊 Price Analysis & Insights
# - ✅ Eligibility & Requirements
# """)

# Create three columns for the main action buttons
col1, col2, col3 = st.columns(3)

# Initialize session state for price analysis visibility
if 'show_price_analysis' not in st.session_state:
    st.session_state.show_price_analysis = False

with col1:
    if st.button("📊 Price Analysis & Insights", use_container_width=True):
        st.session_state.show_price_analysis = not st.session_state.show_price_analysis

with col2:
    if st.button("✅ Eligibility & Requirements", use_container_width=True):
        st.success("You selected Eligibility & Requirements!")

with col3:
    if st.button("📋 Process Guidelines", use_container_width=True):
        st.success("You selected Process Guidelines!")
        
        # Load and process HDB documents using RAG functions
        with st.spinner("Loading HDB documents..."):
            try:
                # Process HDB documents and get chunks
                chunks = process_hdb_documents(print_info=False)  # Don't print to console in Streamlit
                
                st.success(f"Successfully loaded {len(chunks)} document chunks!")
                
                # Display some chunk information
                if chunks:
                    st.write("**Document Processing Summary:**")
                    st.write(f"- Total chunks: {len(chunks)}")
                    st.write(f"- First chunk preview: {chunks[0].page_content[:200]}...")
                    
                    # Optionally show more details in an expander
                    with st.expander("View chunk details"):
                        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
                            st.write(f"**Chunk {i+1}:**")
                            st.write(f"Content: {chunk.page_content[:150]}...")
                            if hasattr(chunk, 'metadata'):
                                st.write(f"Metadata: {chunk.metadata}")
                            st.write("---")
                            
            except Exception as e:
                st.error(f"Error loading documents: {str(e)}")

st.write("")

# Show/hide Price Analysis & Insights section based on button state
if st.session_state.show_price_analysis:
    #START: Price Analysis & Insights
    # Filter options
    st.markdown("**Select Location:**")
    towns = ["All Towns", "Ang Mo Kio", "Bedok", "Bishan", "Bukit Batok", "Bukit Merah", 
             "Bukit Panjang", "Bukit Timah", "Central Area", "Choa Chu Kang", "Clementi",
             "Geylang", "Hougang", "Jurong East", "Jurong West", "Kallang/Whampoa",
             "Marine Parade", "Pasir Ris", "Punggol", "Queenstown", "Sembawang",
             "Sengkang", "Serangoon", "Tampines", "Toa Payoh", "Woodlands", "Yishun"]
    selected_town = st.selectbox("Choose a town", towns, label_visibility="collapsed")

    st.write("")
    st.markdown("**Flat Type:**")
    flat_col1, flat_col2, flat_col3, flat_col4, flat_col5, flat_col6, flat_col7 = st.columns(7)
    with flat_col1:
        room_1 = st.checkbox("1-Room")
    with flat_col2:
        room_2 = st.checkbox("2-Room")
    with flat_col3:
        room_3 = st.checkbox("3-Room")
    with flat_col4:
        room_4 = st.checkbox("4-Room")
    with flat_col5:
        room_5 = st.checkbox("5-Room")
    with flat_col6:
        executive = st.checkbox("Executive")
    with flat_col7:
        multi_gen = st.checkbox("Multi-Generation")

    st.write("")
    st.markdown("**Price Range:**")
    price_range = st.slider("Price range selector", min_value=300000, max_value=1500000, value=(300000, 1500000), 
                            format="$%d", label_visibility="collapsed")
    st.write(f"Selected range: ${price_range[0]:,} - ${price_range[1]:,}")

    #add a button "Analyze" to show the analysis results
    if st.button("Analyze", use_container_width=True):
        st.success("Analysis results will be displayed here!")
        # Here you can add the logic to perform the analysis based on selected filters
        # For now, we will just display a placeholder message
        st.write(f"Analyzing resale prices for {selected_town} with the following criteria:")
        st.write(f"- Flat Types: {', '.join([ft for ft, sel in zip(['1-Room', '2-Room', '3-Room', '4-Room', '5-Room', 'Executive', 'Multi-Generation'], 
                                                            [room_1, room_2, room_3, room_4, room_5, executive, multi_gen]) if sel])}")
        st.write(f"- Price Range: ${price_range[0]:,} - ${price_range[1]:,}")
    #END: Price Analysis & Insights

st.write("")

# form = st.form(key="form")
# form.subheader("Or ask me anything about HDB resale...")

# user_prompt = form.text_area("Enter your query here", height=200)

# if form.form_submit_button("Submit"):
#     print(f"User has submitted {user_prompt}")
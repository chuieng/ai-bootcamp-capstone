import streamlit as st


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

    #END: Price Analysis & Insights

st.write("")

# form = st.form(key="form")
# form.subheader("Or ask me anything about HDB resale...")

# user_prompt = form.text_area("Enter your query here", height=200)

# if form.form_submit_button("Submit"):
#     print(f"User has submitted {user_prompt}")
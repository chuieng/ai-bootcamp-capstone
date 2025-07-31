import streamlit as st
from utility import check_password

# region &lt;--------- Streamlit Page Configuration ---------&gt;

st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

# endregion &lt;--------- Streamlit Page Configuration ---------&gt;

st.title("Streamlit App")
form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    print(f"User has submitted {user_prompt}")
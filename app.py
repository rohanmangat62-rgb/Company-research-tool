import streamlit as st
from analyser import analyse_company

st.title("AI Company Research Tool")
st.write("Enter a company name to generate an AI-powered risk and opportunity analysis based on live news.")

company = st.text_input("Company name", placeholder="e.g. Apple, Tesla, Amazon")

if st.button("Analyse"):
    if company:
        with st.spinner("Fetching news and analysing..."):
            result = analyse_company(company)
        st.markdown(result)
    else:
        st.warning("Please enter a company name.")
import streamlit as st
from analyser import analyse_company

st.title("AI Company Research Tool")
st.write("Enter a company name and stock ticker to generate an AI-powered equity research report based on live news and financial data.")

company = st.text_input("Company name", placeholder="e.g. Apple")
ticker = st.text_input("Stock ticker", placeholder="e.g. AAPL")

if st.button("Analyse"):
    if company and ticker:
        with st.spinner("Fetching news and financial data, analysing..."):
            result = analyse_company(company, ticker.upper())

        # Recommendation badge
        rec = result["recommendation"]
        if rec == "Buy":
            st.success(f"Recommendation: {rec}")
        elif rec == "Hold":
            st.warning(f"Recommendation: {rec}")
        elif rec == "Sell":
            st.error(f"Recommendation: {rec}")

        # Sentiment indicator
        sentiment = result["sentiment"]
        confidence = result["sentiment_confidence"]
        st.metric(label="Market Sentiment", value=sentiment, delta=f"{confidence}% confidence")

        # Recommendation rationale
        st.subheader("Rationale")
        st.write(result["recommendation_rationale"])

        # Full report
        st.subheader("Full Analysis")
        st.markdown(result["report"])

    elif not company:
        st.warning("Please enter a company name.")
    elif not ticker:
        st.warning("Please enter a stock ticker.")
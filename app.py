import streamlit as st
from analyser import analyse_company
from pdf_exporter import generate_pdf

st.title("AI Company Research Tool")
st.write("Enter a company name and stock ticker to generate an AI-powered equity research report based on live news and financial data.")

company = st.text_input("Company name", placeholder="e.g. Apple")
ticker = st.text_input("Stock ticker", placeholder="e.g. AAPL")

if st.button("Analyse"):
    if company and ticker:
        with st.spinner("Fetching news and financial data, analysing..."):
            result = analyse_company(company, ticker.upper())

        st.session_state["result"] = result
        st.session_state["company"] = company
        st.session_state["ticker"] = ticker.upper()

    elif not company:
        st.warning("Please enter a company name.")
    elif not ticker:
        st.warning("Please enter a stock ticker.")

if "result" in st.session_state:
    result = st.session_state["result"]
    company = st.session_state["company"]
    ticker = st.session_state["ticker"]

    # Recommendation badge
    rec = result["recommendation"]
    if rec == "Buy":
        st.success(f"Recommendation: {rec}")
    elif rec == "Hold":
        st.warning(f"Recommendation: {rec}")
    elif rec == "Sell":
        st.error(f"Recommendation: {rec}")

    # Sentiment
    st.metric(label="Market Sentiment", value=result["sentiment"], delta=f"{result['sentiment_confidence']}% confidence")

    # Rationale
    st.subheader("Rationale")
    st.write(result["recommendation_rationale"])

    # Full report
    st.subheader("Full Analysis")
    st.markdown(result["report"])

    # PDF download
    pdf_buffer = generate_pdf(company, ticker, result)
    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name=f"{ticker}_research_report.pdf",
        mime="application/pdf"
    )
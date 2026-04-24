import streamlit as st
from analyser import analyse_company, compare_companies
from pdf_exporter import generate_pdf

st.title("AI Company Research Tool")

# Mode toggle
mode = st.radio("Select mode", ["Single Company", "Compare Two Companies"], horizontal=True)

if mode == "Single Company":
    st.write("Enter a company name and stock ticker to generate an AI-powered equity research report.")

    company = st.text_input("Company name", placeholder="e.g. Apple")
    ticker = st.text_input("Stock ticker", placeholder="e.g. AAPL")

    if st.button("Analyse"):
        if company and ticker:
            with st.spinner("Fetching news and financial data, analysing..."):
                result = analyse_company(company, ticker.upper())
            st.session_state["result"] = result
            st.session_state["company"] = company
            st.session_state["ticker"] = ticker.upper()
            st.session_state["mode"] = "single"
        elif not company:
            st.warning("Please enter a company name.")
        elif not ticker:
            st.warning("Please enter a stock ticker.")

    if "result" in st.session_state and st.session_state.get("mode") == "single":
        result = st.session_state["result"]
        company = st.session_state["company"]
        ticker = st.session_state["ticker"]

        rec = result["recommendation"]
        if rec == "Buy":
            st.success(f"Recommendation: {rec}")
        elif rec == "Hold":
            st.warning(f"Recommendation: {rec}")
        elif rec == "Sell":
            st.error(f"Recommendation: {rec}")

        st.metric(label="Market Sentiment", value=result["sentiment"], delta=f"{result['sentiment_confidence']}% confidence")

        st.subheader("Rationale")
        st.write(result["recommendation_rationale"])

        st.subheader("Full Analysis")
        st.markdown(result["report"])

        pdf_buffer = generate_pdf(company, ticker, result)
        st.download_button(
            label="Download PDF Report",
            data=pdf_buffer,
            file_name=f"{ticker}_research_report.pdf",
            mime="application/pdf"
        )

elif mode == "Compare Two Companies":
    st.write("Enter two companies to generate a side-by-side comparable company analysis.")

    col1, col2 = st.columns(2)

    with col1:
        company1 = st.text_input("Company 1 name", placeholder="e.g. Apple")
        ticker1 = st.text_input("Company 1 ticker", placeholder="e.g. AAPL")

    with col2:
        company2 = st.text_input("Company 2 name", placeholder="e.g. Microsoft")
        ticker2 = st.text_input("Company 2 ticker", placeholder="e.g. MSFT")

    if st.button("Compare"):
        if company1 and ticker1 and company2 and ticker2:
            with st.spinner("Fetching data for both companies and comparing..."):
                comparison = compare_companies(company1, ticker1.upper(), company2, ticker2.upper())
            st.session_state["comparison"] = comparison
            st.session_state["mode"] = "compare"
        else:
            st.warning("Please fill in all four fields.")

    if "comparison" in st.session_state and st.session_state.get("mode") == "compare":
        comparison = st.session_state["comparison"]

        # Side by side recommendation badges
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{comparison['company1']} ({comparison['ticker1']})")
            rec1 = comparison["company1_recommendation"]
            if rec1 == "Buy":
                st.success(f"Recommendation: {rec1}")
            elif rec1 == "Hold":
                st.warning(f"Recommendation: {rec1}")
            elif rec1 == "Sell":
                st.error(f"Recommendation: {rec1}")

            f1 = comparison["financials1"]
            st.metric("Market Cap", f"${f1['market_cap']:,.0f}" if f1['market_cap'] != "N/A" else "N/A")
            st.metric("P/E Ratio", f1['pe_ratio'])
            st.metric("Analyst Rating", f1['analyst_rating'].upper() if f1['analyst_rating'] != "N/A" else "N/A")

        with col2:
            st.subheader(f"{comparison['company2']} ({comparison['ticker2']})")
            rec2 = comparison["company2_recommendation"]
            if rec2 == "Buy":
                st.success(f"Recommendation: {rec2}")
            elif rec2 == "Hold":
                st.warning(f"Recommendation: {rec2}")
            elif rec2 == "Sell":
                st.error(f"Recommendation: {rec2}")

            f2 = comparison["financials2"]
            st.metric("Market Cap", f"${f2['market_cap']:,.0f}" if f2['market_cap'] != "N/A" else "N/A")
            st.metric("P/E Ratio", f2['pe_ratio'])
            st.metric("Analyst Rating", f2['analyst_rating'].upper() if f2['analyst_rating'] != "N/A" else "N/A")

        st.subheader("Comparative Analysis")
        st.markdown(comparison["comparison_report"])
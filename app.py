import streamlit as st
from analyser import analyse_company, compare_companies
from pdf_exporter import generate_pdf

st.set_page_config(
    page_title="AI Equity Research Tool",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #f7f8fc;
    color: #1a1f36;
}

.stApp {
    background-color: #f7f8fc;
}

.main-header {
    padding: 2rem 0 1.2rem 0;
    border-bottom: 2px solid #1a1f36;
    margin-bottom: 2rem;
}

.main-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    color: #1a1f36;
    margin: 0;
    letter-spacing: -0.5px;
}

.main-header p {
    color: #6b7280;
    font-size: 0.9rem;
    margin-top: 0.4rem;
    font-weight: 400;
}

.badge-buy {
    display: inline-block;
    background-color: #dcfce7;
    color: #15803d;
    border: 1px solid #86efac;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.4rem 1.2rem;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

.badge-hold {
    display: inline-block;
    background-color: #fef9c3;
    color: #a16207;
    border: 1px solid #fde047;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.4rem 1.2rem;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

.badge-sell {
    display: inline-block;
    background-color: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fca5a5;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.4rem 1.2rem;
    border-radius: 4px;
    letter-spacing: 1px;
    margin-bottom: 1rem;
}

.sentiment-box {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 1rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.sentiment-box .label {
    font-size: 0.72rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.3rem;
}

.sentiment-box .value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1a1f36;
}

.sentiment-box .confidence {
    font-size: 0.82rem;
    color: #3b82f6;
    margin-top: 0.2rem;
}

.section-card {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.section-card h3 {
    font-size: 0.72rem;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 0.6rem;
    font-weight: 500;
}

.section-card p {
    color: #374151;
    line-height: 1.7;
    font-size: 0.92rem;
}

.divider {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5rem 0;
}

.stTextInput > div > div > input {
    background-color: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #1a1f36 !important;
    border-radius: 4px !important;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15) !important;
}

.stButton > button {
    background-color: #1a1f36 !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-weight: 500 !important;
    padding: 0.5rem 2rem !important;
}

.stButton > button:hover {
    background-color: #2d3561 !important;
}

.stDownloadButton > button {
    background-color: transparent !important;
    color: #3b82f6 !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 4px !important;
    font-weight: 500 !important;
}

.stRadio > div {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.4rem 1rem;
}

[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 0.72rem !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

[data-testid="stMetricValue"] {
    color: #1a1f36 !important;
}

[data-testid="stMetricDelta"] {
    color: #3b82f6 !important;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📈 AI Equity Research</h1>
    <p>Institutional-grade company analysis powered by live news and real financial data</p>
</div>
""", unsafe_allow_html=True)

mode = st.radio("", ["Single Company", "Compare Two Companies"], horizontal=True)
st.markdown("<hr class='divider'>", unsafe_allow_html=True)

def render_recommendation_badge(rec):
    css_class = {"Buy": "badge-buy", "Hold": "badge-hold", "Sell": "badge-sell"}.get(rec, "badge-hold")
    st.markdown(f'<div class="{css_class}">⬤ {rec.upper()}</div>', unsafe_allow_html=True)

if mode == "Single Company":
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        company = st.text_input("Company name", placeholder="e.g. Apple")
    with col_input2:
        ticker = st.text_input("Stock ticker", placeholder="e.g. AAPL")

    if st.button("Run Analysis"):
        if company and ticker:
            with st.spinner("Fetching live data and generating report..."):
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

        st.markdown(f"### {company} ({ticker})")
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])

        with col1:
            render_recommendation_badge(result["recommendation"])
            st.markdown(f"""
            <div class="sentiment-box">
                <div class="label">Market Sentiment</div>
                <div class="value">{result['sentiment']}</div>
                <div class="confidence">{result['sentiment_confidence']}% confidence</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="section-card">
                <h3>Investment Rationale</h3>
                <p>{result['recommendation_rationale']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### Full Analysis")
        st.markdown(result["report"])

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        pdf_buffer = generate_pdf(company, ticker, result)
        st.download_button(
            label="⬇ Download PDF Report",
            data=pdf_buffer,
            file_name=f"{ticker}_research_report.pdf",
            mime="application/pdf"
        )

elif mode == "Compare Two Companies":
    col1, col2 = st.columns(2)
    with col1:
        company1 = st.text_input("Company 1 name", placeholder="e.g. Apple")
        ticker1 = st.text_input("Company 1 ticker", placeholder="e.g. AAPL")
    with col2:
        company2 = st.text_input("Company 2 name", placeholder="e.g. Microsoft")
        ticker2 = st.text_input("Company 2 ticker", placeholder="e.g. MSFT")

    if st.button("Run Comparison"):
        if company1 and ticker1 and company2 and ticker2:
            with st.spinner("Fetching data for both companies and comparing..."):
                comparison = compare_companies(company1, ticker1.upper(), company2, ticker2.upper())
            st.session_state["comparison"] = comparison
            st.session_state["mode"] = "compare"
        else:
            st.warning("Please fill in all four fields.")

    if "comparison" in st.session_state and st.session_state.get("mode") == "compare":
        comparison = st.session_state["comparison"]

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### {comparison['company1']} ({comparison['ticker1']})")
            render_recommendation_badge(comparison["company1_recommendation"])
            f1 = comparison["financials1"]
            st.metric("Market Cap", f"${f1['market_cap']:,.0f}" if f1['market_cap'] != "N/A" else "N/A")
            st.metric("P/E Ratio", f1['pe_ratio'])
            st.metric("Analyst Rating", f1['analyst_rating'].upper() if f1['analyst_rating'] != "N/A" else "N/A")

        with col2:
            st.markdown(f"### {comparison['company2']} ({comparison['ticker2']})")
            render_recommendation_badge(comparison["company2_recommendation"])
            f2 = comparison["financials2"]
            st.metric("Market Cap", f"${f2['market_cap']:,.0f}" if f2['market_cap'] != "N/A" else "N/A")
            st.metric("P/E Ratio", f2['pe_ratio'])
            st.metric("Analyst Rating", f2['analyst_rating'].upper() if f2['analyst_rating'] != "N/A" else "N/A")

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("### Comparative Analysis")
        st.markdown(comparison["comparison_report"])
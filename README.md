# AI Company Research Tool

An AI-powered equity research assistant that replicates core sell-side analyst workflows — pulling live news and real financial data to generate structured investment reports.

## What it does

- Ingests live news articles via NewsAPI
- Fetches real financial data (market cap, revenue, P/E ratio, analyst ratings) via Yahoo Finance
- Sends both to Claude (Anthropic) to generate a structured equity research report
- Outputs a Buy/Hold/Sell recommendation, sentiment score, risk/opportunity analysis
- Exports a formatted PDF report
- Supports side-by-side comparable company analysis

## Tech stack

- **Python** — core language
- **Anthropic Claude API** — LLM powering the analysis (claude-haiku-4-5-20251001)
- **NewsAPI** — live news ingestion
- **yfinance** — real-time financial data from Yahoo Finance
- **Streamlit** — web interface
- **ReportLab** — PDF generation
- **python-dotenv** — secure API key management

## How to run it

1. Clone the repository
2. Create a virtual environment and activate it

    python -m venv venv
    source venv/bin/activate

3. Install dependencies

    pip install anthropic requests python-dotenv streamlit yfinance reportlab

4. Create a .env file in the root folder with your API keys

    ANTHROPIC_API_KEY=your_key_here
    NEWS_API_KEY=your_key_here

5. Run the app

    streamlit run app.py

## Project structure

    company-research-tool/
    ├── app.py                 # Streamlit web interface
    ├── analyser.py            # Claude API integration and prompt engineering
    ├── news_fetcher.py        # NewsAPI ingestion
    ├── financials_fetcher.py  # Yahoo Finance data retrieval
    ├── pdf_exporter.py        # PDF report generation
    ├── .env                   # API keys (not committed)
    └── .gitignore

## Example output

Enter a company name and ticker (e.g. Apple / AAPL) to generate:
- A Buy, Hold, or Sell recommendation with rationale
- Bullish/Neutral/Bearish sentiment with confidence percentage
- Three key risks and three key opportunities grounded in live data
- A downloadable PDF research report

Supports side-by-side comparison of two companies for comparable company analysis.
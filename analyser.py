import anthropic
import os
import json
from dotenv import load_dotenv
from news_fetcher import get_news
from financials_fetcher import get_financials

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def format_large_number(n):
    if n == "N/A":
        return "N/A"
    if n >= 1_000_000_000_000:
        return f"${n / 1_000_000_000_000:.2f}T"
    if n >= 1_000_000_000:
        return f"${n / 1_000_000_000:.2f}B"
    if n >= 1_000_000:
        return f"${n / 1_000_000:.2f}M"
    return str(n)

def analyse_company(company_name, ticker):
    articles = get_news(company_name)
    financials = get_financials(ticker)

    news_text = ""
    for i, article in enumerate(articles[:5]):
        news_text += f"Article {i+1}: {article['title']}\n{article['description']}\n\n"

    financial_text = f"""
Company: {financials['company_name']}
Sector: {financials['sector']}
Market Cap: {format_large_number(financials['market_cap'])}
Revenue: {format_large_number(financials['revenue'])}
P/E Ratio: {financials['pe_ratio']}
52-Week High: ${financials['52_week_high']}
52-Week Low: ${financials['52_week_low']}
Analyst Rating: {financials['analyst_rating'].upper()}
"""

    json_prompt = f"""You are a sell-side equity research analyst. Analyse the following company using both the news and financial data provided.

FINANCIAL DATA:
{financial_text}

RECENT NEWS:
{news_text}

Respond with ONLY a JSON object in this exact format, no other text, no code fences:
{{
    "recommendation": "Buy",
    "sentiment": "Bullish",
    "sentiment_confidence": 72,
    "recommendation_rationale": "one paragraph explaining the recommendation"
}}

Use only Buy, Hold, or Sell for recommendation. Use only Bullish, Neutral, or Bearish for sentiment."""

    json_message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        messages=[{"role": "user", "content": json_prompt}]
    )

    raw = json_message.content[0].text
    print("DEBUG:", repr(raw))
    clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    structured = json.loads(clean)

    report_prompt = f"""You are a sell-side equity research analyst. Analyse the following company using both the news and financial data provided.

FINANCIAL DATA:
{financial_text}

RECENT NEWS:
{news_text}

Provide a structured report with:
1. Three key risks
2. Three key opportunities

Be concise and specific. Ground your analysis in the data provided."""

    report_message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": report_prompt}]
    )

    report_text = report_message.content[0].text

    return {
        "recommendation": structured["recommendation"],
        "sentiment": structured["sentiment"],
        "sentiment_confidence": structured["sentiment_confidence"],
        "recommendation_rationale": structured["recommendation_rationale"],
        "report": report_text
    }

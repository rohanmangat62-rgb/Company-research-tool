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

def build_financial_text(financials):
    return f"""
Company: {financials['company_name']}
Sector: {financials['sector']}
Market Cap: {format_large_number(financials['market_cap'])}
Revenue: {format_large_number(financials['revenue'])}
P/E Ratio: {financials['pe_ratio']}
52-Week High: ${financials['52_week_high']}
52-Week Low: ${financials['52_week_low']}
Analyst Rating: {financials['analyst_rating'].upper()}
"""

def analyse_company(company_name, ticker):
    articles = get_news(company_name)
    financials = get_financials(ticker)

    news_text = ""
    for i, article in enumerate(articles[:5]):
        news_text += f"Article {i+1}: {article['title']}\n{article['description']}\n\n"

    financial_text = build_financial_text(financials)

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


def compare_companies(company1, ticker1, company2, ticker2):
    # Fetch data for both companies
    articles1 = get_news(company1)
    financials1 = get_financials(ticker1)
    articles2 = get_news(company2)
    financials2 = get_financials(ticker2)

    news_text1 = ""
    for i, article in enumerate(articles1[:5]):
        news_text1 += f"Article {i+1}: {article['title']}\n{article['description']}\n\n"

    news_text2 = ""
    for i, article in enumerate(articles2[:5]):
        news_text2 += f"Article {i+1}: {article['title']}\n{article['description']}\n\n"

    financial_text1 = build_financial_text(financials1)
    financial_text2 = build_financial_text(financials2)

    # Single Claude call with both companies
    comparison_prompt = f"""You are a sell-side equity research analyst conducting a comparable company analysis.

COMPANY 1 - FINANCIAL DATA:
{financial_text1}

COMPANY 1 - RECENT NEWS:
{news_text1}

COMPANY 2 - FINANCIAL DATA:
{financial_text2}

COMPANY 2 - RECENT NEWS:
{news_text2}

Provide a structured comparative analysis with:
1. Head-to-head financial comparison (valuation, growth, profitability)
2. Two key strengths for each company
3. Two key risks for each company
4. Which company has stronger near-term momentum and why
5. Overall verdict: which is the better investment and why

Be concise and specific. Reference the actual numbers provided."""

    comparison_message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{"role": "user", "content": comparison_prompt}]
    )

    # Get individual recommendations for each company
    verdict_prompt = f"""You are a sell-side equity research analyst. Based on this data, give a one-word recommendation for each company.

COMPANY 1 ({company1}):
{financial_text1}

COMPANY 2 ({company2}):
{financial_text2}

Respond with ONLY a JSON object, no other text, no code fences:
{{
    "company1_recommendation": "Buy",
    "company2_recommendation": "Hold"
}}

Use only Buy, Hold, or Sell for each."""

    verdict_message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[{"role": "user", "content": verdict_prompt}]
    )

    raw = verdict_message.content[0].text
    print("DEBUG verdict:", repr(raw))
    clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    verdicts = json.loads(clean)

    return {
        "company1": company1,
        "ticker1": ticker1,
        "company2": company2,
        "ticker2": ticker2,
        "financials1": financials1,
        "financials2": financials2,
        "comparison_report": comparison_message.content[0].text,
        "company1_recommendation": verdicts["company1_recommendation"],
        "company2_recommendation": verdicts["company2_recommendation"]
    }
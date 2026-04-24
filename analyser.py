import anthropic
import os
from dotenv import load_dotenv
from news_fetcher import get_news

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def analyse_company(company_name):
    articles = get_news(company_name)
    
    news_text = ""
    for article in articles.get("articles", []):
        news_text += f"Title: {article['title']}\n"
        news_text += f"Description: {article['description']}\n\n"
    
    prompt = f"""You are a senior equity research analyst. 
Based on the following recent news articles about {company_name}, 
provide a structured analysis with:

1. THREE key risks facing the company
2. THREE key opportunities for the company

Be specific and concise. Base your analysis only on the news provided.

NEWS ARTICLES:
{news_text}

Respond in this exact format:
RISKS:
- Risk 1
- Risk 2
- Risk 3

OPPORTUNITIES:
- Opportunity 1
- Opportunity 2
- Opportunity 3"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

if __name__ == "__main__":
    analysis = analyse_company("Apple")
    print(analysis)
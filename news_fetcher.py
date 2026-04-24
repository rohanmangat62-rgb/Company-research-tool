import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news(company_name):
    url = "https://newsapi.org/v2/everything"
    
    params = {
        "q": f"{company_name} business OR earnings OR strategy OR revenue OR competition",
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 10
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    return data.get("articles", [])

if __name__ == "__main__":
    result = get_news("Amazon")
    for article in result:
        print(article["title"])
        print("---")
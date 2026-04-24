import yfinance as yf

def get_financials(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    financials = {
        "company_name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        "analyst_rating": info.get("recommendationKey", "N/A")
    }
    
    return financials

if __name__ == "__main__":
    data = get_financials("AAPL")
    for key, value in data.items():
        print(f"{key}: {value}")
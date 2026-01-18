import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

file_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(file_dir)

data_dir = os.path.join(root_dir, "data")
processed_data_dir = os.path.join(data_dir, "processed_data")
raw_data_dir = os.path.join(data_dir, "raw_data")

os.makedirs(processed_data_dir, exist_ok=True)

html_path = os.path.join(raw_data_dir, "web_data.html")
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

os.makedirs("processed_data", exist_ok=True)

print("Extracting news data...")

news_data = []
latest_news_items = soup.find_all(class_=lambda x: x and "LatestNews" in x)

for news_item in latest_news_items:
    headline = news_item.find("a", class_="LatestNews-headline")
    timestamp = news_item.find("time", class_="LatestNews-timestamp")
    
    if headline and timestamp:
        title = headline.get("title", headline.text.strip())
        link = headline.get("href", "")
        
        if not link.startswith("http"):
            link = "https://www.cnbc.com" + link
        
        news_data.append({
            "timestamp": timestamp.text.strip(),
            "title": title.strip(),
            "link": link
        })

pd.DataFrame(news_data).to_csv("./data/processed_data/news_data.csv", index=False)
print(f"News data saved: {len(news_data)} items\n")

print("Extracting market data...")

market_data = []
market_banner = soup.find("div", class_="MarketsBanner-marketData")

if market_banner:
    market_cards = market_banner.find_all("a", class_="MarketCard-container")
    
    for card in market_cards:
        symbol = card.find("span", class_="MarketCard-symbol")
        stock_position = card.find("span", class_="MarketCard-stockPosition")
        change_pct = card.find("span", class_="MarketCard-changePct")
        
        if symbol and stock_position and change_pct:
            market_data.append({
                "symbol": symbol.text.strip(),
                "stock_position": float(stock_position.text.strip().replace(",", "")),
                "change_pct": float(change_pct.text.strip().replace(",", "").replace("%", ""))
            })

pd.DataFrame(market_data).to_csv("processed_data/market_data.csv", index=False)
print(f"Market data saved: {len(market_data)} items\n")

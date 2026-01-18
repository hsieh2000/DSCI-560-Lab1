import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
res =  requests.get("https://www.cnbc.com/world/?region=world", headers = headers)
soup = BeautifulSoup(res.text, 'html.parser')
market_banner = soup.find(
    "div",
    class_="MarketsBanner-main"
)
print(market_banner.prettify())

latest_news = soup.find("ul", class_="LatestNews-list")

with open("./data/raw_data/web_data.html", "w") as f:
	f.write(f"{market_banner.prettify()}\n")
	f.write(latest_news.prettify())



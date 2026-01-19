import requests
from bs4 import BeautifulSoup
import os

file_path = os.path.dirname(__file__)
root_path =  os.path.dirname(file_path)

raw_data_dir = os.path.join(root_path, "data", "raw_data")

def get_and_parse(url, headers):
    resp = requests.get(url, headers = headers)
    return BeautifulSoup(resp.text, 'html.parser')

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

target_url = "https://www.cnbc.com/world/?region=world"
soup = get_and_parse(target_url, headers)
latest_news = soup.find("ul", class_="LatestNews-list")

market_url = "https://quote.cnbc.com/quote-html-webservice/restQuote/symbolType/symbol?symbols=SMCI%7CMU%7CMRNA%7CCEG%7CTEAM%7CVST%7C.AXJO%7C.N225%7C.NSEI%7C.HSI%7C.SSEC&requestMethod=itv&noform=1&partnerId=2&fund=1&exthrs=1&output=json&events=1"
soup = get_and_parse(market_url, headers)
market_banner = soup

with open(os.path.join(raw_data_dir, "web_data.html"), "w") as f:
	f.write(f"{market_banner.prettify()}\n")
	f.write(latest_news.prettify())



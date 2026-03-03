import requests
from bs4 import BeautifulSoup

url = "https://finance.sina.com.cn/roll/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
print("状态码:", response.status_code)

soup = BeautifulSoup(response.content, "html.parser")

for item in soup.find_all("a"):
    href = item.get("href")
    text = item.get_text().strip()
    # 只输出非空有意义文本
    if text and href and "finance.sina.com.cn" in href:
        print(f"{text} → {href}")
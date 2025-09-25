import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://www.amazon.in/s?rh=n%3A1375424031&fs=true&ref=lp_1375424031_sar"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5"
}

try:
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
except requests.RequestException as e:
    print(f"Error fetching the URL: {e}")
    exit()

soup = BeautifulSoup(resp.content, 'html.parser')
products = soup.find_all('div', {'data-component-type': 's-search-result'})

product_data = []
for product in products:
    title_tag = product.h2
    title = title_tag.text.strip() if title_tag else "Title not available"

    price_tag = product.find('span', class_='a-price-whole')
    price = price_tag.text.strip() if price_tag else "Price not available"

    rating_tag = product.find('span', class_='a-icon-alt')
    rating = rating_tag.text.strip() if rating_tag else "Rating not available"

    product_data.append({
        'title': title,
        'price': price,
        'rating': rating,
    })

for item in product_data:
    print(f"Title: {item['title']}")
    print(f"Price: {item['price']}")
    print(f"Rating: {item['rating']}")
    print("\n")

df = pd.DataFrame(product_data)
csv_filename = 'amazon_products.csv'
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")

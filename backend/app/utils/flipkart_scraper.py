import requests
from bs4 import BeautifulSoup

def get_flipkart_price(product_url: str):
    """Scrape real-time price from a Flipkart product page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
    }

    try:
        response = requests.get(product_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Flipkart uses various price tags — handle all common ones
        price_element = soup.find("div", class_="_30jeq3 _16Jk6d") or soup.find("div", class_="_30jeq3")
        if not price_element:
            return None

        price_text = price_element.text.strip().replace("₹", "").replace(",", "")
        return float(price_text)
    except Exception as e:
        print(f"⚠️ Error fetching price: {e}")
        return None

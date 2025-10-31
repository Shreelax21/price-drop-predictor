import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.product_model import Product

def fetch_latest_price(url):
    # simple example (you’ll refine this later)
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")

    # example for Flipkart (change selector as per site)
    price_tag = soup.select_one("._30jeq3")
    if not price_tag:
        return None
    price = price_tag.text.replace("₹", "").replace(",", "").strip()
    return float(price)

def update_prices():
    db: Session = SessionLocal()
    products = db.query(Product).all()

    for product in products:
        new_price = fetch_latest_price(product.url)
        if not new_price:
            continue

        product.previous_price = product.current_price
        product.current_price = new_price
        product.highest_price = max(product.highest_price or new_price, new_price)
        product.lowest_price = min(product.lowest_price or new_price, new_price)
        db.commit()

        print(f"Updated {product.name} → ₹{new_price}")

    db.close()

if __name__ == "__main__":
    update_prices()

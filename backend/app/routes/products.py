from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.database import get_db
from app.models.product_model import Product

router = APIRouter(prefix="/products", tags=["Products"])

# 🧩 Request body model for creating a product
class ProductCreate(BaseModel):
    name: str
    url: str
    current_price: float

# 🧭 Get all products
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# 🔍 Get a single product by ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 💡 Analyze price trends for a product
@router.get("/{product_id}/analysis")
def analyze_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # You may later replace these with real tracked history data
    if not getattr(product, "lowest_price", None) or not getattr(product, "highest_price", None):
        return {"message": "Not enough data yet for analysis"}

    deal_score = 0
    remarks = []

    # 1️⃣ Price trend logic
    if getattr(product, "previous_price", None) and product.current_price < product.previous_price:
        deal_score += 30
        remarks.append("Price dropped recently 🟢")
    elif getattr(product, "previous_price", None) and product.current_price > product.previous_price:
        remarks.append("Price hiked before sale 🔴")

    # 2️⃣ All-time low logic
    if product.current_price <= product.lowest_price * 1.05:
        deal_score += 40
        remarks.append("Near all-time low 💥")

    # 3️⃣ Discount logic
    if product.current_price < (product.highest_price * 0.8):
        deal_score += 30
        remarks.append("Good discount from highest 🔻")

    result = {
        "name": product.name,
        "current_price": product.current_price,
        "lowest_price": getattr(product, "lowest_price", None),
        "highest_price": getattr(product, "highest_price", None),
        "deal_score": deal_score,
        "remarks": remarks
    }

    # 📨 Optional: trigger alert when deal_score > 80
    if deal_score > 80:
        # We'll add email alert later
        print(f"⚠️ Price Alert for {product.name} — Deal Score: {deal_score}")

    return result


# 🆕 Add a new product (accepts JSON body)
@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        url=product.url,
        current_price=product.current_price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "✅ Product added successfully!", "product": new_product}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.models.database import get_db
from app.models.product_model import Product

router = APIRouter(prefix="/products", tags=["Products"])

# 🧩 Request body model for creating a product
class ProductCreate(BaseModel):
    name: str
    url: str
    current_price: float

# 🧭 Get all products
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# 🔍 Get a single product by ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# 💡 Analyze price trends for a product
@router.get("/{product_id}/analysis")
def analyze_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # You may later replace these with real tracked history data
    if not getattr(product, "lowest_price", None) or not getattr(product, "highest_price", None):
        return {"message": "Not enough data yet for analysis"}

    deal_score = 0
    remarks = []

    # 1️⃣ Price trend logic
    if getattr(product, "previous_price", None) and product.current_price < product.previous_price:
        deal_score += 30
        remarks.append("Price dropped recently 🟢")
    elif getattr(product, "previous_price", None) and product.current_price > product.previous_price:
        remarks.append("Price hiked before sale 🔴")

    # 2️⃣ All-time low logic
    if product.current_price <= product.lowest_price * 1.05:
        deal_score += 40
        remarks.append("Near all-time low 💥")

    # 3️⃣ Discount logic
    if product.current_price < (product.highest_price * 0.8):
        deal_score += 30
        remarks.append("Good discount from highest 🔻")

    result = {
        "name": product.name,
        "current_price": product.current_price,
        "lowest_price": getattr(product, "lowest_price", None),
        "highest_price": getattr(product, "highest_price", None),
        "deal_score": deal_score,
        "remarks": remarks
    }

    # 📨 Optional: trigger alert when deal_score > 80
    if deal_score > 80:
        # We'll add email alert later
        print(f"⚠️ Price Alert for {product.name} — Deal Score: {deal_score}")

    return result


# 🆕 Add a new product (accepts JSON body)
@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        url=product.url,
        current_price=product.current_price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "✅ Product added successfully!", "product": new_product}

import random
from fastapi import Query

@router.get("/predict_drop/")
def predict_price_drop(url: str = Query(...), db: Session = Depends(get_db)):
    """
    Simulated Flipkart price analysis endpoint
    (Later you can replace this with real scraping + model prediction)
    """
    # Simulate a current price
    current_price = random.uniform(30000, 90000)

    # Simulate predicted drop probability (0–100%)
    predicted_drop_probability = random.uniform(10, 70)

    # Simple logic for comment
    if predicted_drop_probability > 50:
        comment = "High chance of price drop soon 💸"
    elif predicted_drop_probability > 25:
        comment = "Moderate chance — consider waiting 🕒"
    else:
        comment = "Low chance — safe to buy now 🛒"

    return {
        "current_price": current_price,
        "predicted_drop_probability": predicted_drop_probability,
        "prediction_comment": comment
    }


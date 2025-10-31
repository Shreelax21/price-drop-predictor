import numpy as np
import pandas as pd
import lightgbm as lgb
import joblib
import os
from app.utils.flipkart_scraper import get_flipkart_price

MODEL_PATH = "app/ml/price_drop_model.pkl"

# =============================
# Generate synthetic history
# =============================
def generate_synthetic_history(current_price: float, days: int = 30):
    """
    Simulates a short-term price history (since real API data isn't available yet).
    Adds realistic variation around the current price.
    """
    np.random.seed(42)
    prices = [current_price]
    for _ in range(days - 1):
        # Random daily fluctuation between -3% and +3%
        change = np.random.uniform(-0.03, 0.03)
        new_price = prices[-1] * (1 + change)
        prices.append(new_price)

    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    df = pd.DataFrame({"date": dates, "price": prices})
    return df


# =============================
# Train the LightGBM model
# =============================
def train_lightgbm_model(df: pd.DataFrame):
    """
    Trains a simple LightGBM model using price change patterns.
    """
    df["pct_change"] = df["price"].pct_change().fillna(0) * 100
    df["prev_price"] = df["price"].shift(1).fillna(df["price"])
    df["label"] = (df["price"].diff() < 0).astype(int)  # 1 if price dropped

    X = df[["prev_price", "price", "pct_change"]]
    y = df["label"]

    model = lgb.LGBMClassifier(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    print("✅ LightGBM model trained and saved successfully!")


# =============================
# Predict price drop
# =============================
def predict_drop_probability(url: str):
    """
    Fetches product price, generates historical trend, predicts drop probability.
    """
    # 1️⃣ Get latest price
    current_price = get_flipkart_price(url)
    if not current_price:
        return {"error": "⚠️ Failed to fetch price from Flipkart."}

    # 2️⃣ Create synthetic history
    df = generate_synthetic_history(current_price)

    # 3️⃣ Train model if missing
    if not os.path.exists(MODEL_PATH):
        print("⚙️ Model not found — training new model...")
        train_lightgbm_model(df)

    # 4️⃣ Load trained model
    model = joblib.load(MODEL_PATH)

    # 5️⃣ Extract last feature row
    df["pct_change"] = df["price"].pct_change().fillna(0) * 100
    last_row = df.iloc[-1]
    features = np.array([[last_row["prev_price"], last_row["price"], last_row["pct_change"]]])

    # 6️⃣ Predict drop probability
    prob = model.predict_proba(features)[0][1] * 100

    # 7️⃣ Interpret results
    if prob > 70:
        comment = "🔥 High chance of price drop soon — hold your purchase!"
    elif prob > 40:
        comment = "📉 Moderate chance of drop in coming weeks."
    else:
        comment = "🛒 Low chance — safe to buy now."

    return {
        "product_url": url,
        "current_price": round(current_price, 2),
        "predicted_drop_probability": round(prob, 2),
        "prediction_comment": comment
    }

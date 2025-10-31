# train_model.py

import numpy as np
import pandas as pd
import lightgbm as lgb
import joblib
import os

MODEL_PATH = "app/ml/price_drop_model.pkl"

def generate_training_data(num_samples=1000):
    """
    Creates synthetic training data that simulates product price trends.
    """
    np.random.seed(42)
    data = []
    for _ in range(num_samples):
        current_price = np.random.uniform(500, 50000)
        prev_price = current_price * np.random.uniform(0.9, 1.1)
        pct_change = ((current_price - prev_price) / prev_price) * 100
        label = int(current_price < prev_price)  # 1 if price dropped
        data.append([prev_price, current_price, pct_change, label])

    df = pd.DataFrame(data, columns=["prev_price", "price", "pct_change", "label"])
    return df


def train_and_save_model():
    df = generate_training_data()

    X = df[["prev_price", "price", "pct_change"]]
    y = df["label"]

    model = lgb.LGBMClassifier(
        n_estimators=150,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    print("🚀 Training LightGBM model on synthetic price data...")
    model.fit(X, y)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model trained and saved successfully at: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()

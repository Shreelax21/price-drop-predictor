from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import products

app = FastAPI(title="Price Drop Predictor API")

# ✅ Enable CORS (allows your frontend to call the backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(products.router)

@app.get("/")
def home():
    return {"message": "Welcome to Price Drop Predictor API"}

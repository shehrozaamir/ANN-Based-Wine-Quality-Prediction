import os
import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# Lazy import / initialization for TensorFlow
import tensorflow as tf

app = FastAPI(
    title="Château AI - Wine Quality Prediction System",
    description="Deep Learning (ANN) Powered Wine Quality Classification & Enological Analysis",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static folder
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

MODEL_PATH = os.path.join(BASE_DIR, "wine_model.keras")
SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

model = None
scaler = None


def get_artifacts():
    global model, scaler
    if model is None and os.path.exists(MODEL_PATH):
        try:
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Keras ANN Wine model loaded successfully.")
        except Exception as e:
            print(f"Error loading Keras model: {e}")

    if scaler is None and os.path.exists(SCALER_PATH):
        try:
            scaler = joblib.load(SCALER_PATH)
            print("StandardScaler loaded successfully.")
        except Exception as e:
            print(f"Error loading scaler: {e}")

    return model, scaler


# Initial load attempt
get_artifacts()


class WineFeatures(BaseModel):
    fixed_acidity: float = Field(..., ge=2.0, le=20.0, description="Tartaric acid (g/dm³)", example=7.4)
    volatile_acidity: float = Field(..., ge=0.05, le=2.5, description="Acetic acid (g/dm³)", example=0.7)
    citric_acid: float = Field(..., ge=0.0, le=2.0, description="Citric acid (g/dm³)", example=0.0)
    residual_sugar: float = Field(..., ge=0.2, le=30.0, description="Residual sugar (g/dm³)", example=1.9)
    chlorides: float = Field(..., ge=0.005, le=1.0, description="Sodium chloride (g/dm³)", example=0.076)
    free_sulfur_dioxide: float = Field(..., ge=1.0, le=120.0, description="Free SO2 (mg/dm³)", example=11.0)
    total_sulfur_dioxide: float = Field(..., ge=5.0, le=400.0, description="Total SO2 (mg/dm³)", example=34.0)
    density: float = Field(..., ge=0.97, le=1.05, description="Density (g/cm³)", example=0.9978)
    pH: float = Field(..., ge=2.5, le=4.5, description="pH level", example=3.51)
    sulphates: float = Field(..., ge=0.1, le=3.0, description="Potassium sulphate (g/dm³)", example=0.56)
    alcohol: float = Field(..., ge=6.0, le=18.0, description="Alcohol percentage (% vol)", example=9.4)


@app.get("/", response_class=FileResponse)
async def serve_home():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h2>Frontend error: static/index.html not found</h2>", status_code=404)


@app.get("/health")
async def health_check():
    ann_model, std_scaler = get_artifacts()
    return {
        "status": "online",
        "service": "Château AI Wine Quality Predictor",
        "model_loaded": ann_model is not None,
        "scaler_loaded": std_scaler is not None,
        "architecture": "Artificial Neural Network (Sequential: 11 -> 16 -> 8 -> 1)"
    }


@app.post("/predict")
async def predict_wine_quality(data: WineFeatures):
    ann_model, std_scaler = get_artifacts()

    if ann_model is None or std_scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model or Scaler not loaded. Ensure wine_model.keras and scaler.pkl are generated."
        )

    try:
        # Prepare feature vector in exact training order
        feature_df = pd.DataFrame([{
            'fixed acidity': data.fixed_acidity,
            'volatile acidity': data.volatile_acidity,
            'citric acid': data.citric_acid,
            'residual sugar': data.residual_sugar,
            'chlorides': data.chlorides,
            'free sulfur dioxide': data.free_sulfur_dioxide,
            'total sulfur dioxide': data.total_sulfur_dioxide,
            'density': data.density,
            'pH': data.pH,
            'sulphates': data.sulphates,
            'alcohol': data.alcohol
        }])

        # Scale features
        feature_scaled = std_scaler.transform(feature_df)

        # Predict probability
        raw_pred = ann_model.predict(feature_scaled, verbose=0)
        prob = float(raw_pred[0][0])
        is_good = prob >= 0.5

        # Detailed confidence score
        confidence_pct = round(prob * 100 if is_good else (1.0 - prob) * 100, 1)

        # Analytical enology insights based on input chemistry
        insights = []
        if data.volatile_acidity > 0.65:
            insights.append("High volatile acidity detected: may cause vinegary/acetic sharpness.")
        elif data.volatile_acidity <= 0.4:
            insights.append("Low volatile acidity: clean, fruit-forward aromatic profile.")

        if data.alcohol >= 11.5:
            insights.append("Generous alcohol concentration provides rich body, warmth and mouthfeel.")
        elif data.alcohol < 9.5:
            insights.append("Lower alcohol level: lighter body, may feel watery or lean.")

        if data.sulphates >= 0.65:
            insights.append("Optimal sulphates support antioxidant protection and fruit preservation.")
        else:
            insights.append("Moderate to low sulphates: gentle finish with reduced astringency.")

        if data.pH < 3.2:
            insights.append("Low pH provides crisp freshness and microbial stability.")
        elif data.pH > 3.6:
            insights.append("High pH softens tartness but requires careful SO2 management.")

        # Quality tiering
        if prob >= 0.80:
            tier = "Grand Cru Reserve (Exceptional Quality)"
        elif prob >= 0.50:
            tier = "Premium Selection (Good Quality)"
        elif prob >= 0.30:
            tier = "Standard Vintage (Mediocre / Sub-standard)"
        else:
            tier = "Deficient Vintage (Poor Quality)"

        return {
            "prediction": "good" if is_good else "bad",
            "is_good": is_good,
            "raw_probability": round(prob, 4),
            "quality_probability_pct": round(prob * 100, 1),
            "confidence_pct": confidence_pct,
            "tier": tier,
            "insights": insights,
            "metrics": {
                "alcohol_level": f"{data.alcohol}% vol",
                "ph_balance": f"{data.pH} pH",
                "volatile_acidity": f"{data.volatile_acidity} g/dm³",
                "sugar_level": f"{data.residual_sugar} g/dm³"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

# 🍷 Château AI — Wine Quality Prediction System (ANN)

An end-to-end Deep Learning web application that predicts **Wine Quality** (Good vs. Deficient) based on physiochemical tests, powered by an **Artificial Neural Network (Sequential ANN)**, **FastAPI**, and a luxury responsive frontend UI.

---

## 🚀 Features

- **Deep Learning Model (ANN)**:
  - Architecture: `11 Input Neurons` ➔ `Dense(16, ReLU)` ➔ `Dense(8, ReLU)` ➔ `Dense(1, Sigmoid)`
  - Optimizer: `Adam` | Loss: `Binary Crossentropy`
  - Scaler: Scikit-Learn `StandardScaler`
- **FastAPI Production Engine**:
  - Validated Pydantic input schemas (`WineFeatures`)
  - Health check endpoint `/health` for Render zero-downtime monitoring
  - `/predict` returning prediction verdict, classification confidence %, quality tier, and enological notes
- **Luxury Responsive Studio UI**:
  - Deep Bordeaux wine aesthetic with gold accents and glassmorphism
  - Instant sample presets: *Grand Cru Reserve*, *Table Vintage*, *Acetic Defect*, and *Dataset Averages*
  - Dual tactile controls: Synced Range Sliders + Number inputs
  - Real-time animated probability gauge and sommelier tasting diagnostics
  - Keyboard shortcuts (`Ctrl` + `Enter` for rapid evaluation)
- **Production Ready Deployment**:
  - Ready for **Render**, **Railway**, or Docker with pre-configured `render.yaml`, `Procfile`, and `requirements.txt`.

---

## 🧪 Chemical Parameters Evaluated

1. **Fixed Acidity** (`g/dm³` - Tartaric acid)
2. **Volatile Acidity** (`g/dm³` - Acetic acid / vinegar defect)
3. **Citric Acid** (`g/dm³` - Freshness & crispness)
4. **Residual Sugar** (`g/dm³` - Sweetness balance)
5. **Chlorides** (`g/dm³` - Salinity)
6. **Free Sulfur Dioxide** (`mg/dm³` - Microbial stability)
7. **Total Sulfur Dioxide** (`mg/dm³` - SO₂ balance)
8. **Density** (`g/cm³` - Specific gravity)
9. **pH Level** (`pH` - Acidity index)
10. **Sulphates** (`g/dm³` - Antimicrobial & antioxidant)
11. **Alcohol** (`% vol` - Body & mouthfeel)

---

## 💻 Local Quickstart

### 1. Clone & Enter Directory
```bash
cd "ANN PROJECT"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run FastAPI Web Server
```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```
Open your browser at **[http://127.0.0.1:8000](http://127.0.0.1:8000)**.

---

## ☁️ How to Deploy on Render

1. Push your project folder to **GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Château AI Wine Predictor"
   git branch -M main
   git remote add origin https://github.com/<your-username>/wine-quality-ann.git
   git push -u origin main
   ```

2. Go to **[Render.com](https://render.com/)** and click **New + > Web Service**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml`, or you can configure manually:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Click **Deploy Web Service** — Your live URL will be ready in 2–3 minutes!

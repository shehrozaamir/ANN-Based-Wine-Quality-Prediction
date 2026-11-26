# 🍷 ANN-Based Wine Quality Prediction

A binary classification project that predicts whether a red wine is **Good** or **Bad** from its physicochemical properties, using an Artificial Neural Network (ANN) built with Keras. The trained model is served through a **FastAPI** backend with an interactive web UI.

## Features

- ANN classifier trained on the Red Wine Quality dataset
- Feature scaling with `StandardScaler` (the same scaler is reused at inference time)
- FastAPI backend that loads the saved model and scaler
- Web UI with sliders, preset wine profiles, and live prediction output

## Dataset

- **Source:** Red Wine Quality dataset (Kaggle)
- **Samples:** 1,599
- **Input features (11):** fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol
- **Target:** `quality` → `good` (1) / `bad` (0)

## Model Architecture

| Layer | Details |
|---|---|
| Input | 11 features |
| Dense | 16 neurons, ReLU |
| Dense | 8 neurons, ReLU |
| Output | 1 neuron, Sigmoid |

- **Loss:** Binary Crossentropy
- **Optimizer:** Adam
- **Epochs:** 100, **Batch size:** 32, **Validation split:** 20%
- **Train/Test split:** 80/20, stratified, `random_state=42`

## Results

| Metric | Score |
|---|---|
| Training accuracy | ~80% |
| Validation accuracy | ~76% |
| **Test accuracy** | **~75.6%** |

Accuracy in the 75–80% range is typical for this dataset, since wine quality is a subjective rating that the 11 chemical features cannot fully explain.

## Project Structure

```
ANN-Based-Wine-Quality-Prediction/
├── Wine_Quality.py      # Data prep, training, evaluation
├── main.py              # FastAPI app
├── wine.csv             # Dataset
├── wine_model.keras     # Trained ANN model
├── scaler.pkl           # Fitted StandardScaler
├── requirements.txt
└── README.md
```

## Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/ANN-Based-Wine-Quality-Prediction.git
cd ANN-Based-Wine-Quality-Prediction

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000` in your browser.

## Tech Stack

Python · TensorFlow/Keras · scikit-learn · pandas · NumPy · FastAPI · Uvicorn

## Future Improvements

- Add EarlyStopping and Dropout to reduce overfitting
- Hyperparameter tuning (layers, neurons, learning rate)
- Deploy on Hugging Face Spaces

## Author

**Shehroz** — BSCS student, aspiring AI Engineer

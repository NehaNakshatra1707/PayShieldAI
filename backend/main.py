from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import joblib
import os

# =========================================================
# PAYSHIELD AI - FASTAPI BACKEND
# =========================================================

app = FastAPI(
    title="PayShield AI",
    description="AI-powered payment fraud detection API",
    version="1.0.0"
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "xgboost_fraud_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "scaler.pkl"
)

# =========================================================
# LOAD MODEL
# =========================================================

try:
    model = joblib.load(MODEL_PATH)
    print("✅ XGBoost fraud model loaded successfully.")
except Exception as e:
    model = None
    print("❌ Failed to load XGBoost model:", e)

# =========================================================
# LOAD SCALER
# =========================================================

try:
    scaler = joblib.load(SCALER_PATH)
    print("✅ Scaler loaded successfully.")
except Exception as e:
    scaler = None
    print("⚠️ Scaler not loaded:", e)

# =========================================================
# ROOT
# =========================================================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "PayShield AI backend is running.",
        "model_loaded": model is not None
    }

# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None
    }

# =========================================================
# PREDICT
# =========================================================

@app.post("/predict")
async def predict(request: Request):

    try:

        # -------------------------------------------------
        # READ JSON
        # -------------------------------------------------

        data = await request.json()

        # -------------------------------------------------
        # GET FEATURES
        # -------------------------------------------------

        features = None

        # FORMAT 1:
        # {
        #     "features": [30 values]
        # }

        if "features" in data:

            features = data["features"]

        # FORMAT 2:
        # {
        #     "Time": ...,
        #     "V1": ...,
        #     ...
        #     "V28": ...,
        #     "Amount": ...
        # }

        elif "Time" in data and "Amount" in data:

            features = []

            features.append(float(data["Time"]))

            for i in range(1, 29):

                key = f"V{i}"

                if key not in data:
                    return {
                        "status": "error",
                        "message": f"Missing feature: {key}"
                    }

                features.append(
                    float(data[key])
                )

            features.append(
                float(data["Amount"])
            )

        else:

            return {
                "status": "error",
                "message": "Invalid transaction format."
            }

        # -------------------------------------------------
        # CHECK FEATURE COUNT
        # -------------------------------------------------

        if len(features) != 30:

            return {
                "status": "error",
                "message": (
                    f"Expected 30 features, "
                    f"but received {len(features)}."
                )
            }

        # -------------------------------------------------
        # CONVERT TO FLOAT
        # -------------------------------------------------

        try:

            features = [
                float(value)
                for value in features
            ]

        except Exception:

            return {
                "status": "error",
                "message": "All transaction features must be numeric."
            }

        # -------------------------------------------------
        # CHECK INVALID VALUES
        # -------------------------------------------------

        if not all(
            np.isfinite(value)
            for value in features
        ):

            return {
                "status": "error",
                "message": "Transaction contains invalid numeric values."
            }

        # -------------------------------------------------
        # NUMPY ARRAY
        # -------------------------------------------------

        input_data = np.array(
            features,
            dtype=float
        ).reshape(1, -1)

        # -------------------------------------------------
        # MODEL CHECK
        # -------------------------------------------------

        if model is None:

            return {
                "status": "error",
                "message": "Fraud detection model is not loaded."
            }

        # -------------------------------------------------
        # SCALING
        # -------------------------------------------------

        # Your trained model evaluation showed that
        # Time and Amount were standardized while
        # V1-V28 remained unchanged.

        if scaler is not None:

            try:

                # Scale only Time and Amount
                scaled_time_amount = scaler.transform(
                    input_data[:, [0, 29]]
                )

                input_data[:, 0] = scaled_time_amount[:, 0]
                input_data[:, 29] = scaled_time_amount[:, 1]

            except Exception:

                # If scaler does not match this format,
                # continue using the raw features.
                pass

        # -------------------------------------------------
        # PREDICTION
        # -------------------------------------------------

        prediction = model.predict(
            input_data
        )[0]

        # -------------------------------------------------
        # PROBABILITY
        # -------------------------------------------------

        if hasattr(model, "predict_proba"):

            probability = model.predict_proba(
                input_data
            )[0][1]

        else:

            probability = float(prediction)

        probability = float(
            np.clip(
                probability,
                0,
                1
            )
        )

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        if int(prediction) == 1:

            result = "Fraud"

        else:

            result = "Legitimate"

        # -------------------------------------------------
        # RISK LEVEL
        # -------------------------------------------------

        if probability >= 0.75:

            risk = "CRITICAL"

        elif probability >= 0.50:

            risk = "HIGH"

        elif probability >= 0.20:

            risk = "MEDIUM"

        else:

            risk = "LOW"

        # -------------------------------------------------
        # RECOMMENDATION
        # -------------------------------------------------

        if result == "Fraud":

            recommendation = (
                "Review or block this transaction "
                "before processing."
            )

        else:

            recommendation = (
                "Transaction appears safe based "
                "on the AI assessment."
            )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {

            "status": "success",

            "result": result,

            "prediction": int(prediction),

            "is_fraud": int(prediction) == 1,

            "fraud_probability": probability,

            "risk_level": risk,

            "recommendation": recommendation

        }

    except Exception as e:

        print("Prediction error:", str(e))

        return {

            "status": "error",

            "message": str(e)

        }
import os, pickle
from pathlib import Path
from flask import Flask, request, render_template, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__, template_folder="templates")

# --- Load model/preprocessor once ---
pipeline = None
model = None
preproc = None

def _load(p):
    with open(p, "rb") as f: return pickle.load(f)

if Path("model_trainer.pkl").exists():
    obj = _load("model_trainer.pkl")
    if hasattr(obj, "predict") and hasattr(obj, "set_params"):
        pipeline = obj
    else:
        model = obj

if pipeline is None and Path("prepocessor_obj.pkl").exists():
    preproc = _load("prepocessor_obj.pkl")

FEATURES = [
    "gender",
    "race_ethnicity",
    "parental_level_of_education",
    "lunch",
    "test_preparation_course",
    "reading_score",
    "writing_score",
]

def _predict(rows):
    df = pd.DataFrame(rows, columns=FEATURES)
    if pipeline is not None:
        y = pipeline.predict(df)
    else:
        X = preproc.transform(df) if preproc is not None else df
        y = model.predict(X)
    return [float(v) for v in y]

# --- Routes ---
@app.route("/")
def index():
    return redirect(url_for("predict_datapoint"))

@app.route("/predict", methods=["GET", "POST"])
@app.route("/predict_datapoint", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("home.html", results=None)

    # JSON API
    if request.is_json:
        body = request.get_json(silent=True) or {}
        inst = body.get("instances", [])
        rows = []
        for it in inst:
            if isinstance(it, dict):
                rows.append([
                    it.get("gender"),
                    it.get("race_ethnicity") or it.get("ethnicity"),
                    it.get("parental_level_of_education"),
                    it.get("lunch"),
                    it.get("test_preparation_course"),
                    it.get("reading_score"),
                    it.get("writing_score"),
                ])
            elif isinstance(it, (list, tuple)) and len(it) == 7:
                rows.append(list(it))
            else:
                return jsonify(error="Each instance must be a dict or a 7-item list"), 400
        return jsonify(predictions=_predict(rows))

    # Form POST -> re-render home.html with result
    f = request.form
    # If your home.html labels were swapped, you can swap here:
    reading = f.get("reading_score")
    writing = f.get("writing_score")
    row = [[
        f.get("gender"),
        f.get("ethnicity"),
        f.get("parental_level_of_education"),
        f.get("lunch"),
        f.get("test_preparation_course"),
        int(reading),
        int(writing),
    ]]
    try:
        pred = _predict(row)[0]
        return render_template("home.html", results=f"{pred:.2f}")
    except Exception as e:
        return render_template("home.html", results=f"Error: {e}")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    if not request.is_json:
        return jsonify(error="Send JSON with 'instances'."), 400
    body = request.get_json(silent=True) or {}
    inst = body.get("instances", [])
    rows = []
    for it in inst:
        if isinstance(it, dict):
            rows.append([
                it.get("gender"),
                it.get("race_ethnicity") or it.get("ethnicity"),
                it.get("parental_level_of_education"),
                it.get("lunch"),
                it.get("test_preparation_course"),
                it.get("reading_score"),
                it.get("writing_score"),
            ])
        elif isinstance(it, (list, tuple)) and len(it) == 7:
            rows.append(list(it))
        else:
            return jsonify(error="Each instance must be a dict or a 7-item list"), 400
    return jsonify(predictions=_predict(rows))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

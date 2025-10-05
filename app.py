import os
import pickle
from pathlib import Path
from flask import Flask, request, render_template, jsonify, redirect, url_for
import pandas as pd

app = Flask(__name__, template_folder="templates")

# ============================================================
#               🔹 MODEL / PREPROCESSOR LOADER
# ============================================================

# Tell Flask where to find model & preprocessor files
MODEL_DIR = Path(os.getenv("MODEL_DIR", "artifacts")).resolve()

MODEL_CANDIDATES = [
    MODEL_DIR / "model_trainer.pkl",
]

PREPROC_CANDIDATES = [
    MODEL_DIR / "prepocessor_obj.pkl",  # (your uploaded spelling)
    MODEL_DIR / "preprocessor_obj.pkl",
]

pipeline = None
model = None
preproc = None
load_messages = []


def _load_pickle(p: Path):
    with p.open("rb") as f:
        return pickle.load(f)


def try_load():
    global pipeline, model, preproc

    # --- Try to load model/pipeline ---
    for p in MODEL_CANDIDATES:
        if p.exists():
            try:
                obj = _load_pickle(p)
                if hasattr(obj, "predict"):
                    if hasattr(obj, "transform"):
                        pipeline = obj
                        load_messages.append(f"Loaded pipeline: {p}")
                    else:
                        model = obj
                        load_messages.append(f"Loaded model: {p}")
                    break
                else:
                    load_messages.append(f"Found pickle without predict(): {p}")
            except Exception as e:
                load_messages.append(f"Failed to load model from {p}: {e}")

    # --- Try to load preprocessor if not a full pipeline ---
    if pipeline is None:
        for p in PREPROC_CANDIDATES:
            if p.exists():
                try:
                    obj = _load_pickle(p)
                    if hasattr(obj, "transform"):
                        preproc = obj
                        load_messages.append(f"Loaded preprocessor: {p}")
                        break
                    else:
                        load_messages.append(f"Found pickle without transform(): {p}")
                except Exception as e:
                    load_messages.append(f"Failed to load preprocessor from {p}: {e}")


try_load()

FEATURES = [
    "gender",
    "race_ethnicity",
    "parental_level_of_education",
    "lunch",
    "test_preparation_course",
    "reading_score",
    "writing_score",
]


def predict_rows(rows):
    """Run model prediction."""
    if pipeline is None and model is None:
        raise RuntimeError(
            "Model not loaded. "
            + " | ".join(load_messages or ["No model/preprocessor files found."])
        )

    df = pd.DataFrame(rows, columns=FEATURES)

    if pipeline is not None:
        y = pipeline.predict(df)
    else:
        X = preproc.transform(df) if preproc is not None else df
        y = model.predict(X)

    return [float(v) for v in y]


# ============================================================
#                       🔹 ROUTES
# ============================================================

@app.route("/")
def index():
    """Redirect root to /predict."""
    return redirect(url_for("predict_datapoint"))


@app.route("/predict", methods=["GET", "POST"])
@app.route("/predict_datapoint", methods=["GET", "POST"])
def predict_datapoint():
    """Handles both UI form and JSON POST."""
    if request.method == "GET":
        debug = "<br>".join(load_messages) if load_messages else "No load messages."
        return render_template("home.html", results=None, debug=debug)

    # --- JSON API POST ---
    if request.is_json:
        body = request.get_json(silent=True) or {}
        instances = body.get("instances", [])
        rows = []

        for it in instances:
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

        try:
            return jsonify(predictions=predict_rows(rows))
        except Exception as e:
            return jsonify(error=str(e), details=load_messages), 500

    # --- FORM POST (from home.html) ---
    f = request.form
    try:
        reading = int(f.get("reading_score"))
        writing = int(f.get("writing_score"))
    except (TypeError, ValueError):
        return render_template("home.html", results="Please enter numeric Reading/Writing scores.")

    row = [[
        f.get("gender"),
        f.get("ethnicity"),
        f.get("parental_level_of_education"),
        f.get("lunch"),
        f.get("test_preparation_course"),
        reading,
        writing,
    ]]

    try:
        pred = predict_rows(row)[0]
        pretty = f"{pred:.2f}"
        debug = "<br>".join(load_messages) if load_messages else ""
        return render_template("home.html", results=pretty, debug=debug)
    except Exception as e:
        debug = "<br>".join(load_messages) if load_messages else ""
        return render_template("home.html", results=f"Error: {e}", debug=debug)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Dedicated API endpoint for JSON prediction."""
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

    try:
        return jsonify(predictions=predict_rows(rows))
    except Exception as e:
        return jsonify(error=str(e), details=load_messages), 500


# ============================================================
#                      🔹 ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

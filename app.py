# app.py
from flask import Flask, request, render_template, render_template_string, jsonify
import pandas as pd
import os
import traceback
import json

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize Flask app
application = Flask(__name__)
app = application

# --------------------------------------------------------------------------------
# Define the expected column names in the same order used during model training
# --------------------------------------------------------------------------------
EXPECTED_COLUMNS = [
    "gender",
    "race_ethnicity",
    "parental_level_of_education",
    "lunch",
    "test_preparation_course",
    "reading_score",
    "writing_score"
]

# --------------------------------------------------------------------------------
# Root / Home Route
# --------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


# --------------------------------------------------------------------------------
# HTML Form Route (for local web UI)
# --------------------------------------------------------------------------------
@app.route('/predicted_data', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')

    try:
        # Collect data from the HTML form
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        # Convert form inputs to DataFrame
        pred_df = data.get_data_as_data_frame()

        # Make prediction
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # Return the result rendered in the web page
        return render_template('home.html', results=results[0])

    except Exception as e:
        app.logger.error(f"Error in /predicted_data: {e}", exc_info=True)
        return render_template('home.html', results=None, error=str(e)), 500


# --------------------------------------------------------------------------------
# JSON API Route (for curl / Postman / Cloud Run)
# Also supports GET: shows a small help page + a textarea form for manual testing.
# --------------------------------------------------------------------------------
@app.route('/predict', methods=['GET', 'POST'])
def predict_api():
    # If user visits /predict in browser (GET), show simple help + form
    if request.method == 'GET':
        html = """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8" />
            <title>Predict API</title>
            <style>
              body { font-family: Arial, sans-serif; margin: 2rem; }
              textarea { width: 100%; max-width: 900px; }
              pre { background:#f7f7f7; padding:10px; border-radius:6px; }
              .note { color:#555; }
            </style>
          </head>
          <body>
            <h2>Predict API</h2>
            <p class="note">This endpoint accepts <strong>POST</strong> requests with JSON bodies of the form:</p>
            <pre>{
  "instances": [
    ["female","group B","some college","free/reduced","completed",53,66]
  ]
}</pre>
            <p class="note">You can also paste JSON below and submit to test.</p>
            <form method="post" action="/predict">
              <textarea name="json_input" rows="8">{"instances": [["female", "group B", "some college", "free/reduced", "completed", 53, 66]]}</textarea><br><br>
              <button type="submit">Submit JSON</button>
            </form>
          </body>
        </html>
        """
        return render_template_string(html), 200

    # For POST (either JSON API clients or the form above)
    try:
        # If the request is a form post from the HTML above, it will be application/x-www-form-urlencoded
        if request.content_type and 'application/x-www-form-urlencoded' in request.content_type:
            js = request.form.get('json_input', '').strip()
            if not js:
                return jsonify({"error": "Form submitted but no JSON found in 'json_input'"}), 400
            try:
                payload = json.loads(js)
            except Exception as e:
                return jsonify({"error": f"Invalid JSON in form input: {str(e)}"}), 400
        else:
            # Expect JSON content-type for API clients
            if not request.is_json:
                return jsonify({"error": "Request must be JSON (Content-Type: application/json)"}), 415
            payload = request.get_json()

        instances = payload.get("instances")
        if instances is None:
            return jsonify({
                "error": "Missing 'instances' key in JSON payload. Example: {'instances': [[...], ...]}"
            }), 400

        # Detect whether input is list of dicts or list of lists
        first = instances[0] if isinstance(instances, list) and len(instances) > 0 else None

        if isinstance(first, dict):
            # Case 1: list of dictionaries → directly create DataFrame
            input_df = pd.DataFrame(instances)
            # Reorder and ensure all expected columns exist
            input_df = input_df.reindex(columns=EXPECTED_COLUMNS)
        elif isinstance(first, list) or first is None:
            # Case 2: list of lists → map to expected column order
            input_df = pd.DataFrame(instances, columns=EXPECTED_COLUMNS)
        else:
            return jsonify({"error": "Each instance must be a list or an object/dict."}), 400

        # Convert numeric columns to float safely
        for col in ["reading_score", "writing_score"]:
            if col in input_df.columns:
                input_df[col] = pd.to_numeric(input_df[col], errors="coerce")

        # Basic validation
        if input_df.shape[0] == 0:
            return jsonify({"error": "No instances provided."}), 400

        # Predict using your existing pipeline
        predict_pipeline = PredictPipeline()
        preds = predict_pipeline.predict(input_df)

        # Convert predictions to JSON-serializable format
        preds_list = [float(x) for x in preds]

        return jsonify({"predictions": preds_list}), 200

    except Exception as e:
        app.logger.error(f"Error in /predict: {e}", exc_info=True)
        # If your PredictPipeline is structured to return structured errors, optionally include those
        return jsonify({"error": str(e)}), 500


# --------------------------------------------------------------------------------
# App Runner
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    # Cloud Run uses PORT env var, default to 8080 locally
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)

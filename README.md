Student Performance Prediction — End-to-End ML Deployment on Google Cloud

 Overview

This project predicts a student’s math score based on demographic and educational attributes such as gender, parental education, and test preparation.

The goal was to design a production-ready ML system — from raw data preprocessing to live deployment — demonstrating complete MLOps capability.

Workflow

1️⃣ Data Exploration & Model Building

Performed Exploratory Data Analysis (EDA) using Jupyter Notebook.

Cleaned, visualized, and analyzed relationships between student features and performance.

Encoded categorical variables, scaled numerical ones, and handled missing values.

Trained multiple ML algorithms (Linear Regression, Random Forest, etc.).

Selected the best-performing model based on R² score and cross-validation.

Serialized the final model using pickle for production use.

Main notebooks:

notebook/EDA.ipynb

notebook/model_training.ipynb

2️⃣ Modular Pipeline Development

Converted Jupyter workflow into modular Python code under src/:

data_ingestion.py – reads and preprocesses data.

data_transformation.py – handles feature engineering.

model_trainer.py – trains and saves the model.

predict_pipeline.py – loads the model and predicts on new data.

Implemented exception handling and logging across all modules.

Created a fully reproducible structure following ML pipeline best practices.

 Core modules:

src/
 ├── components/
 │   ├── data_ingestion.py
 │   ├── data_transformation.py
 │   └── model_trainer.py
 ├── pipeline/
 │   ├── predict_pipeline.py
 │   └── training_pipeline.py
 └── utils.py


3️⃣ Flask Web Application

Developed an interactive Flask app (app.py) for predictions.

Added two endpoints:

/predicted_data → renders HTML form (for manual input)

/predict → REST API endpoint for JSON input (used in Docker & Cloud Run)

Implemented validation, structured error handling, and logging.

4️⃣ Containerization with Docker

Created a production-ready Dockerfile for environment reproducibility.

Included all dependencies in requirements.txt.

Built local image and verified API via cURL.

Commands used:

docker build -t my-ml-api:dev .
docker run -p 8080:8080 my-ml-api:dev


5️⃣ Deployment on Google Cloud Run

Deployed the containerized app on Google Cloud Run (fully serverless):

Created and configured:

Artifact Registry (ml-repo)

Cloud Run service (my-ml-api)

Pushed image to GCP and Deployed.

6️⃣ CI/CD Automation with Cloud Build

Created a cloudbuild.yaml for automated Docker build & deployment.

Connected GitHub repo via Google Cloud Build Triggers using a user-managed service account.

Configured build to:

Build Docker image

Push to Artifact Registry

Deploy to Cloud Run

Each Git push → triggers a full rebuild and redeploy automatically.


7️⃣ Tech Stack & Tools
Layer	Technologies Used
Data Processing	Python, Pandas, NumPy
Modeling	scikit-learn
Web Framework	Flask
Containerization	Docker
Cloud Deployment	Google Cloud Run, Artifact Registry
Automation	Google Cloud Build (CI/CD)
Version Control	Git, GitHub
Monitoring & Logging	Cloud Logging, Docker logs

🏁 End-to-End Flow Summary

Data Exploration & Preprocessing

Model Training & Evaluation

Modular Code Conversion

Flask REST API Creation

Dockerization

GCP Deployment (Artifact Registry + Cloud Run)

CI/CD Automation via Cloud Build

🧰 Future Improvements

Integrate Vertex AI for automated model retraining

Add monitoring dashboards using Prometheus or Cloud Monitoring

Implement automated unit tests in CI/CD

💬 Author

Rakshith A H
📧 Email: ahrakshith122@gmail.com


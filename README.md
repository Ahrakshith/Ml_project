🎓 Student Performance Prediction — End-to-End ML Deployment on Google Cloud
🚀 Overview

This project predicts a student’s math score based on demographic and educational attributes such as gender, parental education, and test preparation.

The goal was to design a production-ready ML system — from raw data preprocessing to live deployment — demonstrating full MLOps capability.

🧩 Workflow
1️⃣ Data Exploration & Model Building

Performed Exploratory Data Analysis (EDA) using Jupyter Notebook.

Cleaned, visualized, and analyzed relationships between student features and performance.

Encoded categorical variables, scaled numerical features, and handled missing values.

Trained multiple ML algorithms (Linear Regression, Random Forest, etc.).

Selected the best-performing model using R² score and cross-validation.

Serialized the final model using pickle for production deployment.

Main Notebooks:
notebook/EDA.ipynb
notebook/model_training.ipynb

2️⃣ Modular Pipeline Development

Converted Jupyter workflow into modular, reusable Python components under the src/ directory.

Core Modules:

src/
 ├── components/
 │   ├── data_ingestion.py        # Reads and preprocesses data
 │   ├── data_transformation.py   # Handles feature engineering
 │   └── model_trainer.py         # Trains and saves the model
 ├── pipeline/
 │   ├── predict_pipeline.py      # Loads model & predicts new data
 │   └── training_pipeline.py     # Orchestrates the full training
 └── utils.py                     # Utility functions


✅ Implemented exception handling and logging across all modules.
✅ Ensured full reproducibility following ML pipeline best practices.

3️⃣ Flask Web Application

Developed an interactive Flask web app for real-time predictions.

Endpoints:

/predicted_data → Renders HTML form (for manual user input)

/predict → REST API endpoint for JSON input (used by Docker & Cloud Run)

Features:

Input validation

Structured error handling

Logging support for production

4️⃣ Containerization with Docker

Built a production-ready Docker image to ensure environment reproducibility.

Included:

All dependencies in requirements.txt

Optimized Dockerfile for smaller image size

Commands Used:

docker build -t my-ml-api:dev .
docker run -p 8080:8080 my-ml-api:dev

5️⃣ Deployment on Google Cloud Run

Deployed the containerized app on Google Cloud Run (fully serverless).

Steps:

Created an Artifact Registry (ml-repo)

Built and pushed Docker image to GCP

Deployed service to Cloud Run (my-ml-api)

✅ Result → Fully managed, scalable REST API endpoint.

6️⃣ CI/CD Automation with Cloud Build

Set up Google Cloud Build for automated CI/CD.

Created: cloudbuild.yaml
Configured GitHub Trigger:

Builds Docker image

Pushes to Artifact Registry

Deploys to Cloud Run automatically

Every Git push → triggers full rebuild & redeploy 🚀

🧠 Tech Stack & Tools
Layer	Technologies Used
Data Processing	Python, Pandas, NumPy
Modeling	scikit-learn
Web Framework	Flask
Containerization	Docker
Cloud Deployment	Google Cloud Run, Artifact Registry
Automation (CI/CD)	Google Cloud Build
Version Control	Git, GitHub
Monitoring & Logging	Cloud Logging, Docker logs
🏁 End-to-End Flow Summary

1️⃣ Data Exploration & Preprocessing
2️⃣ Model Training & Evaluation
3️⃣ Modular Code Conversion
4️⃣ Flask REST API Creation
5️⃣ Dockerization
6️⃣ GCP Deployment (Artifact Registry + Cloud Run)
7️⃣ CI/CD Automation via Cloud Build

🔮 Future Improvements

🔁 Integrate Vertex AI for automated model retraining

📊 Add monitoring dashboards using Prometheus or Cloud Monitoring

✅ Implement automated unit tests in CI/CD pipeline

💬 Author

👨‍💻 Rakshith A H
📧 ahrakshith122@gmail.com

⭐ If you found this project helpful, consider giving it a star!

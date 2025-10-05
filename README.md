
# 🚀 Student Performance Predictor: End-to-End MLOps on Google Cloud ☁️

**Predicting student math scores with a production-ready, fully serverless ML system.**

## ✨ Project Overview

This project delivers a complete MLOps pipeline, starting from raw data analysis to a live, scalable API endpoint on Google Cloud. The goal is to **predict a student's math score** based on key attributes like gender, parental education, and test preparation.

It serves as a full-stack demonstration of MLOps best practices, CI/CD automation, and cloud-native deployment.

---

## 🛠️ Tech Stack & Tools

| Layer | Technologies Used |
| :--- | :--- |
| **Data Processing** | Python, Pandas, NumPy |
| **Modeling** | scikit-learn (Linear Regression, Random Forest) |
| **Web Framework** | Flask (REST API) |
| **Containerization** | Docker |
| **Cloud Deployment** | Google Cloud Run, Artifact Registry |
| **Automation (CI/CD)** | Google Cloud Build |
| **Version Control** | Git, GitHub |
| **Monitoring & Logging**| Cloud Logging, Docker logs |

---

## 🎯 End-to-End Workflow

The entire ML system is structured into a seven-stage, production-ready pipeline:

### 1️⃣ Data Exploration & Model Building (Offline)

* Performed **Exploratory Data Analysis (EDA)** and deep-dive visualization in Jupyter.
* Conducted feature engineering: cleaned, analyzed relationships, handled missing values, and applied **encoding/scaling**.
* Trained and evaluated multiple **ML algorithms** (Linear Regression, Random Forest, etc.).
* Selected the best model based on the **R² score** and cross-validation, then serialized it using `pickle`.
    * **Main Notebooks:** `notebook/EDA.ipynb`, `notebook/model_training.ipynb`

### 2️⃣ Modular Pipeline Development (Code Refactoring)

The entire Jupyter workflow was refactored into a **modular, reusable Python package** to ensure reproducibility and maintainability.


src/
├── components/
│   ├── data\_ingestion.py        \# Reads and preprocesses data source
│   ├── data\_transformation.py   \# Handles categorical encoding, scaling, and feature engineering
│   └── model\_trainer.py         \# Trains, evaluates, and saves the final model
├── pipeline/
│   ├── predict\_pipeline.py      \# Loads the production model and generates predictions
│   └── training\_pipeline.py     \# Orchestrates the full end-to-end training flow
└── utils.py                     \# Helper functions (e.g., saving objects, loading models)



* ✅ Implemented robust **exception handling and logging** across all modules.

### 3️⃣ Flask Web Application (API Layer)

Developed a lightweight **Flask web application** to serve the model for real-time predictions.

* **HTML Form Endpoint:** `/predicted_data` (Renders a form for manual user input).
* **REST API Endpoint:** `/predict` (Accepts JSON input, perfect for microservice communication).
* Includes input validation and structured error handling for a production environment.

### 4️⃣ Containerization with Docker 🐳

The entire application (model, dependencies, and Flask API) was containerized into a single, production-ready Docker image to guarantee environment consistency.

* Optimized `Dockerfile` for a smaller image footprint.
* **Commands Used:**
    ```bash
    docker build -t my-ml-api:dev .
    docker run -p 8080:8080 my-ml-api:dev
    ```

### 5️⃣ Deployment on Google Cloud Run ☁️

Deployed the containerized application to **Google Cloud Run**, a fully serverless platform, providing a managed, scalable REST API endpoint.

* Used **Artifact Registry** (`ml-repo`) to store and manage the Docker images.
* Deployed the service (`my-ml-api`) for autoscaling and zero infrastructure overhead.

### 6️⃣ CI/CD Automation with Cloud Build ⚙️

Implemented a complete Continuous Integration/Continuous Deployment (CI/CD) pipeline using **Google Cloud Build** and a GitHub trigger.

* Defined the CI/CD steps in `cloudbuild.yaml`.
* Every `git push` automatically triggers:
    1.  Building the new Docker image.
    2.  Pushing the image to Artifact Registry.
    3.  Deploying the updated service to Cloud Run.

---

## 💡 Future Improvements (Roadmap)

* **Vertex AI Integration:** 🔁 Integrate Vertex AI Pipelines for automated, scheduled model retraining and advanced MLOps features.
* **Observability:** 📊 Add monitoring dashboards using **Prometheus/Grafana** or **Cloud Monitoring** to track model drift and API health.
* **Testing:** ✅ Implement automated **unit tests** for all modular components within the CI/CD pipeline.

---

## 👨‍💻 Author

| **Rakshith A H** | ahrakshith122@gmail.com |
| :--- | :--- |

⭐ If you found this project helpful, please give it a star!

# 🎓 Student Performance Prediction — End-to-End ML Deployment on Google Cloud

## 📖 Overview
This project predicts a student's **math score** using demographic and educational attributes such as gender, parental education, and test-preparation status.  
It demonstrates a **production-grade MLOps pipeline**: data exploration → model training → modular pipeline → REST API → Docker → GCP Cloud Run → CI/CD with Cloud Build.

---

## 🚀 Workflow Summary
1️⃣ Data Exploration & Model Building

Performed Exploratory Data Analysis (EDA) using Jupyter Notebook.

Cleaned, visualized, and analyzed relationships between student features and performance.

Encoded categorical variables, scaled numerical ones, and handled missing values.

Trained multiple ML algorithms (Linear Regression, Random Forest, etc.).

Selected the best-performing model based on R² score and cross-validation.

Serialized the final model using pickle for production use.

📁 Main notebooks:

notebook/EDA.ipynb

notebook/model_training.ipynb

2. **Pipeline Modularization**
   - Converted notebooks into reproducible modules under `src/`.
   - Implemented `data_ingestion.py`, `data_transformation.py`, `model_trainer.py`, and `predict_pipeline.py`.
   - Added exception handling & logging for production use.

3. **Flask REST API**
   - Built `app.py` with two routes:
     - `/predicted_data` → HTML form for manual input  
     - `/predict` → JSON API endpoint for programmatic prediction
   - Example:
     ```bash
     curl -X POST https://<CLOUD-RUN-URL>/predict \
       -H "Content-Type: application/json" \
       -d '{"instances":[["female","group B","some college","free/reduced","completed",53,66]]}'
     ```
     → `{"predictions":[51.03]}`

4. **Docker Containerization**
   - Created a `Dockerfile` for consistent runtime.
   - Built and ran locally:
     ```bash
     docker build -t my-ml-api:dev .
     docker run -p 8080:8080 my-ml-api:dev
     ```

5. **Deployment on Google Cloud Run**
   - Created **Artifact Registry** (`ml-repo`) and pushed container image.
   - Deployed via:
     ```bash
     gcloud run deploy my-ml-api \
       --image us-central1-docker.pkg.dev/my-ml-project-474215/ml-repo/my-ml-api:latest \
       --region us-central1 --allow-unauthenticated
     ```
   - ✅ Live endpoint:  
     `https://my-ml-api-1071805107569.us-central1.run.app/predict`

6. **CI/CD Automation with Cloud Build**
   - Added `cloudbuild.yaml`:
     ```yaml
     options:
       logging: CLOUD_LOGGING_ONLY
     steps:
       - name: 'gcr.io/cloud-builders/docker'
         args: ['build','-t','${_IMAGE}','.']
       - name: 'gcr.io/cloud-builders/docker'
         args: ['push','${_IMAGE}']
       - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
         entrypoint: gcloud
         args: [
           'run','deploy','${_SERVICE}',
           '--image','${_IMAGE}',
           '--region','${_REGION}',
           '--allow-unauthenticated',
           '--service-account=${_SERVICE_ACCOUNT}'
         ]
     substitutions:
       _REGION: 'us-central1'
       _SERVICE: 'my-ml-api'
       _PROJECT_ID: 'my-ml-project-474215'
       _REPO: 'ml-repo'
       _IMAGE: 'us-central1-docker.pkg.dev/my-ml-project-474215/ml-repo/my-ml-api:${SHORT_SHA}'
       _SERVICE_ACCOUNT: 'ml-run-sa@my-ml-project-474215.iam.gserviceaccount.com'
     images:
       - '${_IMAGE}'
     timeout: '1200s'
     ```
   - Connected GitHub → Cloud Build Trigger → automatic rebuild + redeploy on each push.

---

## 🧰 Tech Stack
| Layer | Technologies |
|-------|---------------|
| Data Processing | Python, Pandas, NumPy |
| Modeling | scikit-learn |
| API | Flask |
| Containerization | Docker |
| Cloud | Google Cloud Run, Artifact Registry |
| CI/CD | Cloud Build Triggers |
| Version Control | Git + GitHub |



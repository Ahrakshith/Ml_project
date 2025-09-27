# 📦 MLProject

End-to-End Machine Learning Project — demonstrating the complete lifecycle of an ML application: **data processing, model training, evaluation, packaging, and deployment**.


## 🚀 Overview

This repository implements a **complete machine learning project pipeline**. It includes:

* Data ingestion and preprocessing
* Feature engineering
* Model training & evaluation (with `scikit-learn` / `catboost`)
* Model serialization (saving artifacts)
* REST API (`Flask` or `FastAPI`) for predictions
* Packaging with `setup.py` for easy distribution
* Deployment support (e.g., AWS Elastic Beanstalk / Docker)

The project is structured in a modular way so you can **plug in your own dataset and models**.

---

## ✨ Features

✅ Clean, modular project structure
✅ Works with any tabular dataset
✅ Preprocessing & feature engineering pipeline
✅ Model training, evaluation, and saving
✅ REST API for inference
✅ Deployment-ready (AWS EB / Docker)
✅ Packaged with `setup.py` for reusability

## 🔧 Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/krishnaik06/mlproject.git
cd mlproject
```

### 2. Create a virtual environment

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (cmd)**

```bat
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Install as a package

```bash
pip install .
```

---

## 🧰 Usage

### Run the API locally

```bash
python app.py
```

By default, it runs on `http://127.0.0.1:5000`.

### Import package in your code

```python
from src import preprocessing, model, predict
```

### Generate predictions (example CLI)

```bash
mlproject-predict data/input.csv
```

---

## 🔄 Workflow

1. **Data ingestion** → Collect raw dataset
2. **Preprocessing & feature engineering** → Clean & transform data
3. **Model training & evaluation** → Train ML model(s)
4. **Save artifacts** → Store trained model in `artifacts/`
5. **API service** → Serve model via Flask/FastAPI (`app.py`)
6. **Deployment** → Package with `setup.py`, deploy to AWS EB/Docker

---

## 📋 Requirements

* Python 3.7+
* Libraries in `requirements.txt` (e.g., `numpy`, `pandas`, `scikit-learn`, `catboost`, `flask`)
* (Optional) Docker & AWS CLI for deployment

Install all dependencies:

```bash
pip install -r requirements.txt
```

---

## ☁️ Deployment

* **Local**: Run with `python app.py`
* **AWS Elastic Beanstalk**: Use `.ebextensions/` config + `requirements.txt`
* **Docker**: Add a `Dockerfile` and build an image for containerized deployment


## 🙌 Acknowledgements

* [Krish Naik](https://github.com/krishnaik06) for tutorials and project inspiration
* Open-source ML & data science community

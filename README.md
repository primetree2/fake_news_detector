📘 README.md
# 📰 Fake News Detector

A Flask-based web app that classifies whether a news article is **real or fake** using a pre-trained NLP model (TF-IDF + Naive Bayes).

---

## ⚙️ Project Structure


fake_news_detector/
│
├── app.py # Flask backend with fallback model logic
├── modules/
│ └── preprocessing.py # Text cleaning utilities
├── models/
│ └── best_pipeline.joblib # Optional full pipeline
├── scripts/
│ └── train_full.py # Re-training script
├── templates/
│ ├── index.html # Input page
│ └── result.html # Prediction results
├── static/
│ └── styles.css # Optional CSS
├── requirements.txt
└── README.md


---

## 🚀 Quick Setup

### 1️⃣ Clone and enter directory
```bash
git clone <your-repo-url>
cd fake_news_detector

2️⃣ Create virtual environment
python -m venv venv
source venv/bin/activate       # (Linux/Mac)
venv\Scripts\activate          # (Windows)

3️⃣ Install dependencies (exact versions)
pip install -r requirements.txt

🧠 Train / Retrain Model

If you want to retrain the model:

python scripts/train_full.py --dataset data/news.csv


Produces:

models/best_pipeline.joblib 

🧩 Run the App
python app.py


Then open your browser at:

http://127.0.0.1:5000

🧪 Test Health

To verify models load properly:

curl http://127.0.0.1:5000/health


Expected:

{"status": "ok", "model_loaded": true}

☁️ Deployment (Production)

For lightweight production hosting:

gunicorn app:app --bind 0.0.0.0:5000 --workers 3

❌ Common Pitfalls Avoided

✅ No “incompatible pickle” errors (fixed sklearn/joblib versions)
✅ Works both with .joblib and .pkl models
✅ Flask 3.x compatible templates and routing
✅ Tested with Python 3.10 – 3.12


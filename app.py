from flask import Flask, render_template, request, flash, redirect, url_for
import joblib
import os
import traceback
from newspaper import Article

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load your model pipeline
def try_load_joblib():
    try:
        return joblib.load(os.path.join("models", "best_pipeline.joblib"))
    except Exception as e:
        print("⚠️ Failed to load joblib pipeline:", e)
        return None

model_pipeline = try_load_joblib()

# Predict using text
def predict_text(text):
    try:
        prediction = model_pipeline.predict([text])[0]
        # If your pipeline supports predict_proba, get confidence
        if hasattr(model_pipeline, "predict_proba"):
            prob = model_pipeline.predict_proba([text]).max()
        else:
            prob = 0.9  # fallback confidence
        return prediction, prob
    except Exception as e:
        print("Prediction error:", e)
        traceback.print_exc()
        return "error", 0

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "").strip()
    url = request.form.get("url", "").strip()

    if not text and not url:
        flash("Please enter text or URL", "warning")
        return redirect(url_for("index"))

    # If URL is provided, fetch article
    if url:
        try:
            article = Article(url)
            article.download()
            article.parse()
            text = article.text
            if not text:
                flash("Could not extract text from URL", "danger")
                return redirect(url_for("index"))
        except Exception as e:
            print("URL error:", e)
            flash("Error fetching article from URL", "danger")
            return redirect(url_for("index"))

    # Predict
    label, prob = predict_text(text)
    if label == "error":
        flash("Prediction failed", "danger")
        return redirect(url_for("index"))

    # Render result page
    return render_template("result.html", text=text, label=label, prob=prob)

if __name__ == "__main__":
    app.run(debug=True)

# fake_news_detector/scripts/train_full.py
import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.preprocessing import simple_clean

def build_and_train(csv_path, out_dir, test_size=0.2, random_state=42):
    df = pd.read_csv(csv_path)
    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("CSV must contain 'text' and 'label' columns.")
    df = df.dropna(subset=['text','label'])
    X = df['text'].astype(str).apply(simple_clean).tolist()
    y = df['label'].astype(str).tolist()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=10000, ngram_range=(1,2))),
        ('clf', MultinomialNB())
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "best_pipeline.joblib")
    joblib.dump(pipeline, out_path)
    print(f"Saved pipeline to {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train fake news model")
    parser.add_argument("--csv", required=True, help="Path to CSV with 'text' and 'label' columns")
    parser.add_argument("--out", default=os.path.join(os.path.dirname(__file__), "..", "models"), help="Output directory for model")
    args = parser.parse_args()
    build_and_train(args.csv, args.out)

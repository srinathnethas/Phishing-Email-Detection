"""Phishing Email Detection Model (Scikit-learn)

Usage:
    python generate_dataset.py                      # make sample emails.csv (optional)
    python phishing_detector.py train               # train, show accuracy + confusion matrix
    python phishing_detector.py predict "email text here"
"""
import re, sys
import numpy as np, pandas as pd, joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.sparse import hstack, csr_matrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay

DATA, MODEL = "emails.csv", "phishing_model.joblib"
URL_RE = re.compile(r"(?:https?://|www\.)\S+|\b(?:bit\.ly|tinyurl\.com)/\S+", re.I)
KEYWORDS = ["urgent", "verify", "password", "suspended", "confirm", "click", "login", "update",
            "bank", "otp", "pin", "prize", "winner", "refund", "limited", "immediately", "blocked"]
SHORTENERS = ("bit.ly", "tinyurl.com", "goo.gl", "t.co")
BAD_TLDS = (".xyz", ".top", ".click", ".tk", ".ru")

def extract_features(text):
    """Hand-crafted features: URL and keyword signals."""
    t = str(text)
    urls = URL_RE.findall(t)
    low = t.lower()
    letters = [ch for ch in t if ch.isalpha()]
    return [
        len(urls),
        int(any(re.search(r"https?://\d{1,3}(\.\d{1,3}){3}", u) or re.match(r"\d{1,3}(\.\d{1,3}){3}", u) for u in urls)),
        int(any(s in u.lower() for u in urls for s in SHORTENERS)),
        int(any(u.lower().rstrip("/.,").endswith(BAD_TLDS) or any(x in u.lower() for x in BAD_TLDS) for u in urls)),
        int(any("@" in u for u in urls)),
        int(any(re.search(r"[a-z]\d[a-z]", u.lower()) for u in urls)),   # e.g. paypa1, amaz0n
        max([len(u) for u in urls], default=0),
        sum(low.count(k) for k in KEYWORDS),
        t.count("!"),
        sum(ch.isupper() for ch in letters) / max(len(letters), 1),
        len(t),
    ]

def build(texts, tfidf=None, scaler=None, fit=False):
    feats = np.array([extract_features(x) for x in texts], dtype=float)
    if fit:
        tfidf = TfidfVectorizer(lowercase=True, stop_words="english", ngram_range=(1, 2), min_df=2)
        scaler = StandardScaler()
        X_text = tfidf.fit_transform(texts)
        X_num = scaler.fit_transform(feats)
    else:
        X_text, X_num = tfidf.transform(texts), scaler.transform(feats)
    return hstack([X_text, csr_matrix(X_num)]).tocsr(), tfidf, scaler

def train():
    df = pd.read_csv(DATA).dropna(subset=["text", "label"])
    print(f"Dataset: {len(df)} emails  |  Phishing: {int(df.label.sum())}  Safe: {int((df.label == 0).sum())}")
    X_tr, X_te, y_tr, y_te = train_test_split(df.text, df.label, test_size=0.2, random_state=42, stratify=df.label)
    Xtr, tfidf, scaler = build(X_tr.tolist(), fit=True)
    Xte, _, _ = build(X_te.tolist(), tfidf, scaler)
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(Xtr, y_tr)
    pred = model.predict(Xte)
    print(f"\nAccuracy: {accuracy_score(y_te, pred) * 100:.2f}%")
    cm = confusion_matrix(y_te, pred)
    print("\nConfusion Matrix (rows = actual, cols = predicted)\n         Safe  Phishing")
    print(f"Safe     {cm[0][0]:<5} {cm[0][1]}\nPhishing {cm[1][0]:<5} {cm[1][1]}")
    print("\n" + classification_report(y_te, pred, target_names=["Safe", "Phishing"]))
    ConfusionMatrixDisplay(cm, display_labels=["Safe", "Phishing"]).plot(cmap="Blues")
    plt.title("Phishing Email Detection - Confusion Matrix")
    plt.savefig("confusion_matrix.png", dpi=150, bbox_inches="tight")
    joblib.dump({"model": model, "tfidf": tfidf, "scaler": scaler}, MODEL)
    print(f"Saved {MODEL} and confusion_matrix.png")

def predict(text):
    b = joblib.load(MODEL)
    X, _, _ = build([text], b["tfidf"], b["scaler"])
    p = b["model"].predict_proba(X)[0][1]
    print(f"Result: {'PHISHING' if p >= 0.5 else 'SAFE'}  (phishing probability {p * 100:.1f}%)")

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "train":
        train()
    elif len(sys.argv) >= 3 and sys.argv[1] == "predict":
        predict(" ".join(sys.argv[2:]))
    else:
        print(__doc__)

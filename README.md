# Phishing Email Detection Model

A machine learning model built with **Scikit-learn** that classifies emails as **Phishing** or **Safe**
using textual content and URL features.

## Features
- Trains on a dataset of phishing and legitimate emails
- Extracts features: URLs, IP-address links, URL shorteners, suspicious domains, look-alike characters (paypa1), urgent keywords, exclamation marks, capital-letter ratio
- TF-IDF text features combined with the hand-crafted URL/keyword features
- Logistic Regression classifier
- Displays **accuracy**, **confusion matrix** and a classification report; saves `confusion_matrix.png`
- Command-line prediction for any email text

## Project structure
| File | Purpose |
|---|---|
| `generate_dataset.py` | Creates a sample `emails.csv` (1200 synthetic emails) |
| `phishing_detector.py` | Feature extraction, training, evaluation, prediction |
| `emails.csv` | Sample dataset (columns: `text`, `label`; 1 = Phishing, 0 = Safe) |
| `confusion_matrix.png` | Output plot from training |
| `requirements.txt` | Python dependencies |

## Setup
```bash
pip install -r requirements.txt
python generate_dataset.py        # optional, emails.csv is already included
python phishing_detector.py train
```

## Predict an email
```bash
python phishing_detector.py predict "URGENT: verify your password at http://paypa1-support.xyz/login"
# Result: PHISHING  (phishing probability 100.0%)

python phishing_detector.py predict "Hi team, meeting notes are at https://docs.google.com/notes"
# Result: SAFE  (phishing probability 1.8%)
```

## Important note on accuracy
The bundled `emails.csv` is **synthetic** (generated from templates), so the model scores close to
100%. That is not realistic performance. For real results, replace `emails.csv` with a public dataset
(for example the Kaggle "Phishing Email Dataset", SpamAssassin or Enron-based sets) formatted with
`text` and `label` columns, then run `python phishing_detector.py train` again.

## Possible improvements
- Train on a large real-world dataset and compare Naive Bayes, Random Forest, SVM
- Add email header analysis (SPF, DKIM, sender mismatch)
- Build a small web interface with Flask or Streamlit

## Tech stack
Python, Scikit-learn, Pandas, NumPy, SciPy, Matplotlib

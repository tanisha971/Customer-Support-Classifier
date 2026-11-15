
import pandas as pd
import joblib
import json

import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed_tickets.csv"

MODEL_FILE = BASE_DIR / "model" / "ticket_classifier.pkl"

REPORT_DIR = BASE_DIR / "reports"

SCREENSHOT_DIR = BASE_DIR / "screenshots"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. LOAD DATASET AND TRAINED MODEL
# ==========================================

print("=" * 60)
print("CUSTOMER SUPPORT TICKET - MODEL EVALUATION")
print("=" * 60)

df = pd.read_csv(DATA_FILE)

model = joblib.load(MODEL_FILE)

print("\nDataset loaded successfully!")

print("Trained model loaded successfully!")


# ==========================================
# 3. SELECT FEATURES AND TARGET
# ==========================================

X = df["cleaned_description"]

y = df["category"]

print("\nTotal records:", len(df))

print("Total categories:", y.nunique())


# ==========================================
# 4. RECREATE THE SAME TRAIN-TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTEST DATA INFORMATION")

print("Training records:", len(X_train))

print("Testing records:", len(X_test))


# ==========================================
# 5. PREDICT TEST DATA
# ==========================================

print("\nGENERATING PREDICTIONS...")

y_pred = model.predict(X_test)

print("Predictions generated successfully!")


# ==========================================
# 6. CALCULATE EVALUATION METRICS
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

macro_f1 = f1_score(
    y_test,
    y_pred,
    average="macro",
    zero_division=0
)


# ==========================================
# 7. DISPLAY PERFORMANCE METRICS
# ==========================================

print("\n" + "=" * 60)

print("MODEL PERFORMANCE RESULTS")

print("=" * 60)

print(f"\nAccuracy:  {accuracy * 100:.2f}%")

print(f"Precision: {precision * 100:.2f}%")

print(f"Recall:    {recall * 100:.2f}%")

print(f"F1-Score:  {f1 * 100:.2f}%")

print(f"Macro F1:  {macro_f1 * 100:.2f}%")


# ==========================================
# 8. CLASSIFICATION REPORT
# ==========================================

print("\nCLASSIFICATION REPORT")

report = classification_report(
    y_test,
    y_pred,
    zero_division=0
)

print(report)

# Save classification report
report_path = REPORT_DIR / "classification_report.txt"

with open(report_path, "w", encoding="utf-8") as file:
    file.write("CUSTOMER SUPPORT TICKET CLASSIFICATION REPORT\n\n")
    file.write(report)


# ==========================================
# 9. CONFUSION MATRIX
# ==========================================

print("\nGENERATING CONFUSION MATRIX...")

labels = model.named_steps["classifier"].classes_

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

plt.figure(figsize=(14, 10))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=labels,
    yticklabels=labels,
    linewidths=0.5
)

plt.title(
    "Customer Support Ticket - Confusion Matrix",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Predicted Category")

plt.ylabel("Actual Category")

plt.xticks(rotation=45, ha="right")

plt.yticks(rotation=0)

plt.tight_layout()

cm_path = SCREENSHOT_DIR / "confusion_matrix.png"

plt.savefig(
    cm_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Confusion matrix saved:", cm_path)


# ==========================================
# 10. ACTUAL VS PREDICTED COMPARISON
# ==========================================

comparison = pd.DataFrame({
    "Ticket Description": X_test.values,
    "Actual Category": y_test.values,
    "Predicted Category": y_pred
})

comparison["Correct Prediction"] = (
    comparison["Actual Category"]
    == comparison["Predicted Category"]
)

comparison_path = REPORT_DIR / "test_predictions.csv"

comparison.to_csv(
    comparison_path,
    index=False
)

print("\nACTUAL VS PREDICTED SAMPLE")

print(comparison.head(10).to_string(index=False))


# ==========================================
# 11. CORRECT AND INCORRECT PREDICTIONS
# ==========================================

correct = (y_test == y_pred).sum()

incorrect = (y_test != y_pred).sum()

print("\nPREDICTION SUMMARY")

print("Correct predictions:", correct)

print("Incorrect predictions:", incorrect)

print("Total test predictions:", len(y_test))


# ==========================================
# 12. SAVE METRICS
# ==========================================

metrics = {
    "total_records": len(df),
    "training_records": len(X_train),
    "testing_records": len(X_test),
    "accuracy": round(float(accuracy), 4),
    "precision_weighted": round(float(precision), 4),
    "recall_weighted": round(float(recall), 4),
    "f1_weighted": round(float(f1), 4),
    "f1_macro": round(float(macro_f1), 4),
    "correct_predictions": int(correct),
    "incorrect_predictions": int(incorrect)
}

metrics_path = REPORT_DIR / "evaluation_metrics.json"

with open(metrics_path, "w", encoding="utf-8") as file:
    json.dump(metrics, file, indent=4)


# ==========================================
# 13. FINAL RESULT
# ==========================================

print("\n" + "=" * 60)

print("MODEL EVALUATION COMPLETED SUCCESSFULLY!")

print("=" * 60)

print("\nReports saved inside:", REPORT_DIR)

print("Confusion matrix saved inside:", SCREENSHOT_DIR)

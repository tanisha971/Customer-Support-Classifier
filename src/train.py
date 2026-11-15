
import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed_tickets.csv"

MODEL_DIR = BASE_DIR / "model"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_FILE = MODEL_DIR / "ticket_classifier.pkl"


# ==========================================
# 2. LOAD PROCESSED DATASET
# ==========================================

print("=" * 60)
print("CUSTOMER SUPPORT TICKET CLASSIFICATION")
print("MACHINE LEARNING MODEL TRAINING")
print("=" * 60)

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")

print("Dataset shape:", df.shape)


# ==========================================
# 3. SELECT FEATURES AND TARGET
# ==========================================

X = df["cleaned_description"]

y = df["category"]

print("\nFeatures (X): cleaned_description")
print("Target (y): category")

print("\nNumber of input records:", len(X))

print("Number of categories:", y.nunique())

print("\nAvailable categories:")
print(sorted(y.unique()))


# ==========================================
# 4. SPLIT DATASET
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nDATASET SPLIT COMPLETED")

print("Total records:", len(df))

print("Training records:", len(X_train))

print("Testing records:", len(X_test))

print("\nTraining category distribution:")
print(y_train.value_counts().sort_index())

print("\nTesting category distribution:")
print(y_test.value_counts().sort_index())


# ==========================================
# 5. CREATE ML PIPELINE
# ==========================================

model = Pipeline([

    # Convert text into numerical features
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=2,
            max_features=10000,
            sublinear_tf=True
        )
    ),

    # Classification algorithm
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            random_state=42
        )
    )

])


print("\nML PIPELINE CREATED")

print(model)


# ==========================================
# 6. TRAIN THE MODEL
# ==========================================

print("\nMODEL TRAINING STARTED...")

model.fit(X_train, y_train)

print("MODEL TRAINING COMPLETED!")


# ==========================================
# 7. CHECK TRAINING INFORMATION
# ==========================================

print("\nMODEL INFORMATION")

print("Algorithm: Logistic Regression")

print("Text Vectorizer: TF-IDF")

print(
    "Number of TF-IDF features:",
    len(model.named_steps["tfidf"].get_feature_names_out())
)

print(
    "Number of learned categories:",
    len(model.named_steps["classifier"].classes_)
)


# ==========================================
# 8. SAVE TRAINED MODEL
# ==========================================

joblib.dump(model, MODEL_FILE)

print("\nTRAINED MODEL SAVED SUCCESSFULLY!")

print("Model location:", MODEL_FILE)


# ==========================================
# 9. QUICK TRAINING PREDICTION CHECK
# ==========================================

sample_tickets = [
    "I need help with my refund",
    "My payment was charged twice",
    "I cannot login to my account"
]

predictions = model.predict(sample_tickets)

print("\nSAMPLE PREDICTIONS")

for ticket, prediction in zip(sample_tickets, predictions):

    print("\nTicket:", ticket)

    print("Predicted Category:", prediction)


# ==========================================
# 10. TRAINING COMPLETION
# ==========================================

print("\n" + "=" * 60)

print("MACHINE LEARNING MODEL TRAINING COMPLETED!")

print("=" * 60)

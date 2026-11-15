
import re
import joblib

from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "model" / "ticket_classifier.pkl"


# ==========================================
# 2. LOAD TRAINED MODEL
# ==========================================

print("=" * 60)
print("CUSTOMER SUPPORT TICKET CLASSIFICATION SYSTEM")
print("=" * 60)

print("\nLoading trained machine learning model...")

if not MODEL_FILE.exists():
    raise FileNotFoundError(
        "Trained model not found. Please run src/train.py first."
    )

model = joblib.load(MODEL_FILE)

print("Model loaded successfully!")


# ==========================================
# 3. TEXT CLEANING FUNCTION
# ==========================================

def clean_text(text):

    # Convert to lowercase
    text = str(text).lower()

    # Remove special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ==========================================
# 4. PREDICT TICKET CATEGORY
# ==========================================

def predict_ticket(description):

    # Clean input description
    cleaned_description = clean_text(description)

    if not cleaned_description:
        print("\nPlease enter a valid ticket description.")
        return

    # Predict category
    prediction = model.predict([cleaned_description])[0]

    # Get probabilities for all categories
    probabilities = model.predict_proba(
        [cleaned_description]
    )[0]

    # Get category names
    categories = model.named_steps[
        "classifier"
    ].classes_

    # Find highest probability
    confidence = max(probabilities) * 100

    # Sort categories by probability
    top_indices = probabilities.argsort()[::-1][:3]

    print("\n" + "=" * 60)

    print("TICKET CLASSIFICATION RESULT")

    print("=" * 60)

    print("\nOriginal Ticket:")
    print(description)

    print("\nPredicted Category:")
    print(prediction)

    print(f"\nModel Confidence Score: {confidence:.2f}%")

    print("\nTop 3 Predicted Categories:")

    for rank, index in enumerate(top_indices, start=1):

        category = categories[index]

        probability = probabilities[index] * 100

        print(
            f"{rank}. {category}: {probability:.2f}%"
        )

    print("\n" + "=" * 60)


# ==========================================
# 5. INTERACTIVE PREDICTION SYSTEM
# ==========================================

def main():

    print("\nWelcome to the Customer Support Classifier!")

    print("\nEnter a customer support ticket below.")

    print("Type 'exit' to close the application.")

    while True:

        print("\n" + "-" * 60)

        description = input(
            "\nEnter Ticket Description: "
        ).strip()

        if description.lower() in ["exit", "quit"]:
            print("\nThank you for using the classifier!")
            break

        if not description:
            print("Please enter a ticket description.")
            continue

        predict_ticket(description)


# ==========================================
# 6. RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    main()

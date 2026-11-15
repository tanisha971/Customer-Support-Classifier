
import pandas as pd
import re
from pathlib import Path

# ------------------------------------------
# 1. Define project paths
# ------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "tickets.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed_tickets.csv"


# ------------------------------------------
# 2. Load the dataset
# ------------------------------------------

print("=" * 55)
print("CUSTOMER SUPPORT TICKET - DATA PREPROCESSING")
print("=" * 55)

df = pd.read_csv(INPUT_FILE)

print("\n1. DATASET LOADED SUCCESSFULLY")

print("Dataset shape:", df.shape)

print("\nFirst five records:")
print(df.head())


# ------------------------------------------
# 3. Understand the dataset
# ------------------------------------------

print("\n2. DATASET INFORMATION")

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()


# ------------------------------------------
# 4. Check missing values
# ------------------------------------------

print("\n3. MISSING VALUE ANALYSIS")

missing_values = df.isnull().sum()

print(missing_values)

print("\nTotal missing values:", missing_values.sum())


# ------------------------------------------
# 5. Check duplicate records
# ------------------------------------------

print("\n4. DUPLICATE ANALYSIS")

full_duplicates = df.duplicated().sum()

duplicate_ids = df["ticket_id"].duplicated().sum()

print("Duplicate rows:", full_duplicates)
print("Duplicate ticket IDs:", duplicate_ids)


# ------------------------------------------
# 6. Handle duplicates
# ------------------------------------------

before_duplicates = len(df)

df = df.drop_duplicates()

df = df.drop_duplicates(
    subset=["ticket_id"],
    keep="first"
)

removed_duplicates = before_duplicates - len(df)

print("\nDuplicates removed:", removed_duplicates)


# ------------------------------------------
# 7. Handle missing values
# ------------------------------------------

print("\n5. HANDLING MISSING VALUES")

# Description, category and ticket ID
# are essential for our classification task.

df = df.dropna(
    subset=[
        "ticket_id",
        "ticket_description",
        "category"
    ]
)

# Priority and status are additional fields.
# Fill missing values instead of discarding
# otherwise usable ticket descriptions.

df["priority"] = df["priority"].fillna("Unknown")
df["status"] = df["status"].fillna("Unknown")

print("Remaining missing values:")
print(df.isnull().sum())


# ------------------------------------------
# 8. Clean categorical columns
# ------------------------------------------

print("\n6. CLEANING CATEGORICAL DATA")

for column in ["category", "priority", "status"]:
    df[column] = (
        df[column]
        .astype(str)
        .str.strip()
    )

print("Categorical columns cleaned.")


# ------------------------------------------
# 9. Text preprocessing
# ------------------------------------------

print("\n7. TEXT PREPROCESSING")


def clean_text(text):

    # Convert text to lowercase
    text = str(text).lower()

    # Remove unnecessary special characters
    # Keep letters, numbers and spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Preserve the original descriptions
# and create a separate cleaned column.

df["cleaned_description"] = (
    df["ticket_description"].apply(clean_text)
)

# Remove descriptions that become empty
# after cleaning.

df = df[
    df["cleaned_description"].str.len() > 0
].copy()

print("Text cleaning completed.")


# ------------------------------------------
# 10. Final dataset validation
# ------------------------------------------

print("\n8. FINAL DATASET VALIDATION")

print("Total records:", len(df))

print(
    "Number of categories:",
    df["category"].nunique()
)

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nFinal missing values:")
print(df.isnull().sum())

print("\nFinal duplicate rows:", df.duplicated().sum())


# ------------------------------------------
# 11. Save processed dataset
# ------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 55)
print("DATA PREPROCESSING COMPLETED SUCCESSFULLY!")
print("=" * 55)

print("\nProcessed dataset saved at:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:", df.shape)

print("\nSample of cleaned descriptions:")

print(
    df[
        [
            "ticket_description",
            "cleaned_description"
        ]
    ].head()
)

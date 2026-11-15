
import pandas as pd
from datasets import load_dataset
from pathlib import Path

# Create the data folder if it doesn't exist
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("Downloading customer support dataset...")

# Load the humans_only configuration
dataset = load_dataset(
    "s2pidape/support-ticket-dataset",
    "humans_only",
    split="train",
    streaming=True
)

# Shuffle and select 2000 records
sample = dataset.shuffle(
    seed=42,
    buffer_size=50000
).take(2000)

# Convert records into a Pandas DataFrame
df = pd.DataFrame(list(sample))

print("\nOriginal dataset shape:", df.shape)

# Select the required columns
required_columns = [
    "ticket_id",
    "issue_description",
    "category",
    "priority",
    "status"
]

df = df[required_columns]

# Rename issue_description to ticket_description
df = df.rename(columns={
    "issue_description": "ticket_description"
})

# Handle missing values
df = df.dropna(subset=[
    "ticket_id",
    "ticket_description",
    "category",
    "priority",
    "status"
])

# Remove extra spaces
for column in [
    "ticket_description",
    "category",
    "priority",
    "status"
]:
    df[column] = df[column].astype(str).str.strip()

# Remove empty ticket descriptions
df = df[df["ticket_description"] != ""]

# Remove duplicate ticket IDs
df = df.drop_duplicates(subset=["ticket_id"])

# Check minimum dataset requirements
if len(df) < 200:
    raise ValueError("Dataset contains fewer than 200 usable records.")

if df["category"].nunique() < 4:
    raise ValueError("Dataset contains fewer than 4 categories.")

# Save the cleaned dataset
output_path = DATA_DIR / "tickets.csv"
df.to_csv(output_path, index=False)

# Display results
print("\nDataset successfully prepared!")
print("Total records:", len(df))
print("Total categories:", df["category"].nunique())

print("\nCategory distribution:")
print(df["category"].value_counts())

print("\nFinal dataset:")
print(df.head())

print("\nSaved to:", output_path)

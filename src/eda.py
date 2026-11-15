
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path


# ==========================================
# 1. PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = BASE_DIR / "data" / "processed_tickets.csv"

OUTPUT_DIR = BASE_DIR / "screenshots"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. LOAD DATASET
# ==========================================

print("=" * 60)
print("CUSTOMER SUPPORT TICKET - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")

print("\nDataset shape:", df.shape)


# ==========================================
# 3. BASIC DATASET ANALYSIS
# ==========================================

print("\n1. BASIC DATASET INFORMATION")

print("\nFirst five records:")
print(df.head())

print("\nDataset columns:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe(include="all"))


# ==========================================
# 4. TOTAL NUMBER OF TICKETS
# ==========================================

total_tickets = len(df)

print("\n2. TOTAL TICKETS")
print("Total number of tickets:", total_tickets)


# ==========================================
# 5. CATEGORY DISTRIBUTION
# ==========================================

print("\n3. TICKETS BY CATEGORY")

category_counts = df["category"].value_counts()

print(category_counts)

print("\nCategory percentages:")

category_percentages = (
    df["category"].value_counts(normalize=True) * 100
)

print(category_percentages.round(2))


# ==========================================
# 6. PRIORITY DISTRIBUTION
# ==========================================

print("\n4. TICKETS BY PRIORITY")

priority_counts = df["priority"].value_counts()

print(priority_counts)


# ==========================================
# 7. STATUS DISTRIBUTION
# ==========================================

print("\n5. TICKETS BY STATUS")

status_counts = df["status"].value_counts()

print(status_counts)


# ==========================================
# 8. CHART 1 - CATEGORY DISTRIBUTION
# ==========================================

sns.set_theme(style="whitegrid")

plt.figure(figsize=(12, 7))

sns.countplot(
    data=df,
    y="category",
    order=category_counts.index,
    hue="category",
    palette="viridis",
    legend=False
)

plt.title(
    "Customer Support Tickets by Category",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Number of Tickets")
plt.ylabel("Ticket Category")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "category_distribution.png",
    dpi=300
)

plt.show()


# ==========================================
# 9. CHART 2 - PRIORITY DISTRIBUTION
# ==========================================

priority_order = [
    "Urgent",
    "Critical",
    "High",
    "Medium",
    "Low",
    "Unknown"
]

priority_order = [
    p for p in priority_order
    if p in df["priority"].unique()
]

# Include any other priority labels found in the data.
priority_order += [
    p for p in priority_counts.index
    if p not in priority_order
]

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="priority",
    order=priority_order,
    hue="priority",
    palette="magma",
    legend=False
)

plt.title(
    "Distribution of Ticket Priorities",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Priority")
plt.ylabel("Number of Tickets")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "priority_distribution.png",
    dpi=300
)

plt.show()


# ==========================================
# 10. CHART 3 - STATUS DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 6))

sns.countplot(
    data=df,
    x="status",
    order=status_counts.index,
    hue="status",
    palette="Set2",
    legend=False
)

plt.title(
    "Distribution of Ticket Status",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Ticket Status")
plt.ylabel("Number of Tickets")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "status_distribution.png",
    dpi=300
)

plt.show()


# ==========================================
# 11. CHART 4 - CATEGORY VS PRIORITY
# ==========================================

category_priority = pd.crosstab(
    df["category"],
    df["priority"]
)

plt.figure(figsize=(12, 8))

sns.heatmap(
    category_priority,
    annot=True,
    fmt="d",
    cmap="YlGnBu",
    linewidths=0.5
)

plt.title(
    "Ticket Category vs Priority",
    fontsize=16,
    fontweight="bold"
)

plt.xlabel("Priority")
plt.ylabel("Category")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "category_priority_heatmap.png",
    dpi=300
)

plt.show()


# ==========================================
# 12. AUTOMATIC DATA OBSERVATIONS
# ==========================================

print("\n6. IMPORTANT DATA OBSERVATIONS")

most_common_category = category_counts.idxmax()
least_common_category = category_counts.idxmin()

most_common_priority = priority_counts.idxmax()
most_common_status = status_counts.idxmax()

print(
    "Most common category:",
    most_common_category,
    "-",
    category_counts.max(),
    "tickets"
)

print(
    "Least common category:",
    least_common_category,
    "-",
    category_counts.min(),
    "tickets"
)

print(
    "Most common priority:",
    most_common_priority,
    "-",
    priority_counts.max(),
    "tickets"
)

print(
    "Most common status:",
    most_common_status,
    "-",
    status_counts.max(),
    "tickets"
)

print(
    "Number of unique categories:",
    df["category"].nunique()
)


# ==========================================
# 13. SAVE ANALYSIS SUMMARY
# ==========================================

summary = pd.DataFrame({
    "Category": category_counts.index,
    "Ticket_Count": category_counts.values,
    "Percentage": category_percentages.reindex(
        category_counts.index
    ).values
})

summary.to_csv(
    OUTPUT_DIR / "category_summary.csv",
    index=False
)

print("\nAll charts and analysis summaries saved in:")
print(OUTPUT_DIR)

print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS COMPLETED!")
print("=" * 60)

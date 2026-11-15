# SupportAI – Customer Support Ticket Classification System

SupportAI is an NLP-based machine learning application that predicts the category of a customer support ticket from its text description. It uses TF-IDF feature extraction and Logistic Regression, with a Streamlit interface for interactive classification.

## 1. Project Overview

The application helps organize incoming support requests by predicting one of 11 predefined categories. Users can enter a ticket, view the predicted category and estimated class probabilities, try sample tickets, clear the current ticket, and review prediction history.

> This is an educational prototype. Predictions should be reviewed by a human, especially for vague or low-confidence inputs.

## 2. Problem Statement

Customer support teams receive requests about account management, authentication, billing, refunds, technical issues and other topics. Manually categorizing every request can be time-consuming. SupportAI explores how supervised machine learning can classify ticket descriptions and help route them to the appropriate support category.

## 3. Technologies Used

- Python
- Pandas
- Hugging Face `datasets`
- Scikit-learn
- TF-IDF vectorization
- Logistic Regression
- Joblib
- Matplotlib / Seaborn (EDA visualizations)
- Streamlit

## 4. Dataset Information

- **Source:** [Support Ticket Dataset on Hugging Face](https://huggingface.co/datasets/s2pidape/support-ticket-dataset)
- **Repository:** `s2pidape/support-ticket-dataset`
- **Configuration:** `humans_only`
- **Split:** `train`
- **Sample size:** 2,000 records
- **Sampling seed:** 42
- **Number of categories:** 11

The prepared dataset fields are:

| Field | Description |
|---|---|
| `ticket_id` | Unique ticket identifier |
| `ticket_description` | Original customer issue description |
| `category` | Target category to predict |
| `priority` | Ticket priority |
| `status` | Ticket status |
| `cleaned_description` | Normalized text used by the model |

The download script saves `data/tickets.csv`. The preprocessing script creates `data/processed_tickets.csv`.

### Supported Categories

1. Account Management
2. Authentication & Access
3. Billing
4. Bugs & Errors
5. Data Sync
6. Integrations & API
7. Onboarding & How-To
8. Performance
9. Refunds
10. Security
11. Subscription

## 5. Project Structure

```text
Customer-Support-Classifier/
├── data/
│   ├── tickets.csv
│   ├── processed_tickets.csv
│   └── README.md
├── model/
│   └── ticket_classifier.pkl
├── reports/
│   ├── classification_report.txt
│   ├── evaluation_metrics.json
│   └── test_predictions.csv
├── screenshots/
│   ├── category_distribution.png
│   ├── category_priority_heatmap.png
│   ├── category_summary.csv
│   ├── confusion_matrix.png
│   ├── priority_distribution.png
│   └── status_distribution.png
├── src/
│   ├── app.py
│   ├── download_dataset.py
│   ├── eda.py
│   ├── evaluate.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── styles.py
│   ├── theme.py
│   └── train.py
├── .gitignore
└── requirements.txt
```

## 6. Installation

### Prerequisites

- Python 3.10 or a compatible Python version for the installed dependencies
- Git
- Internet access for downloading the dataset and installing packages

Clone the repository:

```bash
git clone https://github.com/tanisha971/Customer-Support-Classifier.git
cd Customer-Support-Classifier
```

Create and activate a virtual environment on Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If setting up dependencies manually, the project uses packages including:

```bash
pip install pandas datasets scikit-learn joblib streamlit matplotlib seaborn
```

## 7. Prepare the Dataset

Run the dataset download script:

```bash
python src/download_dataset.py
```

This downloads and samples the selected Hugging Face dataset configuration and saves the prepared records to `data/tickets.csv`.

## 8. Data Preprocessing

Run:

```bash
python src/preprocessing.py
```

The preprocessing stage handles missing values, duplicate ticket IDs, empty descriptions, whitespace and text normalization. It saves:

```text
data/processed_tickets.csv
```

## 9. Exploratory Data Analysis

Run:

```bash
python src/eda.py
```

The script generates visualizations and category summaries in the `screenshots/` directory.

## 10. Train the Model

Run:

```bash
python src/train.py
```

The model uses TF-IDF text features and Logistic Regression. The training workflow uses a stratified 80:20 train-test split with `random_state=42`. The trained pipeline is saved to:

```text
model/ticket_classifier.pkl
```

## 11. Evaluate the Model

Run:

```bash
python src/evaluate.py
```

The evaluation script generates evaluation metrics, a classification report, test predictions and a confusion matrix. Outputs are saved in `reports/` and `screenshots/`.

### Recorded Evaluation Result

In the supplied evaluation run, the confusion matrix showed 400 correct predictions out of 400 test records (100% observed accuracy). The corresponding precision, recall and F1-score were also 100% for that test split.

This unusually high result should be interpreted cautiously. Similar or template-based text examples may occur in both training and testing data. Further validation using grouped duplicate removal and a separate real-world test dataset is necessary before making production claims.

## 12. Predict a New Ticket (Command Line)

Run:

```bash
python src/predict.py
```

Enter a ticket description when prompted. Type `exit` to close the interactive program.

Example input:

```text
I was charged twice for my monthly invoice.
```

Example output (from a recorded run):

```text
Predicted Category: Billing
Model Confidence Score: 63.63%

Top Predicted Categories:
1. Billing: 63.63%
2. Subscription: 11.39%
3. Refunds: 5.35%
```

The displayed score is the model's highest estimated class probability; it is not necessarily a calibrated probability of correctness.

## 13. Run the Streamlit Web Application

From the project root, run:

```bash
streamlit run src/app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that address in your browser.

### Application Features

- Dashboard with dataset and prediction statistics
- Ticket classification form
- Predicted category and estimated probabilities
- Top-five predicted categories
- Complete probability distribution
- Sample ticket button
- Clear ticket button
- Prediction history
- CSV export of prediction history
- Model information page
- Dark and light appearance themes
- Glassmorphism styling and gradient buttons

## 14. AI Tools and Development Assistance

ChatGPT was used selectively as a supporting tool during development to clarify machine-learning concepts, explore preprocessing and model implementation approaches, explain debugging errors, suggest Streamlit UI improvements and organize documentation.

Suggestions were reviewed, adapted and tested before being incorporated. AI tools supported the development process; they did not remove the need to understand, verify and explain the implementation.

Representative prompts included:

- "Explain how to preprocess a customer support ticket dataset using Pandas, including missing values, duplicate IDs and text normalization."
- "Explain why TF-IDF and Logistic Regression can be used for multiclass text classification and describe their limitations."
- "Guide me through a stratified train-test split and evaluation using accuracy, precision, recall, F1-score and a confusion matrix."
- "Analyze this Python error, explain its cause and suggest a minimal correction that I can understand."
- "Help me build a Streamlit interface with ticket classification, prediction history, sample and clear actions, and a dark/light theme."
- "Suggest a glassmorphism design with electric-blue gradients while preserving the existing application functionality."

## 15. Limitations

- The dataset contains only 2,000 records.
- Classification is restricted to the 11 categories in the dataset.
- Similar or template-based ticket descriptions may inflate random-split evaluation results.
- Vague or very short input may lead to unreliable predictions.
- Predicted probabilities may not be calibrated.
- The text-cleaning approach is primarily designed for English text.
- The prototype is not connected to a production ticketing system.
- There is no automatic feedback loop or continuous model retraining.

## 16. Future Improvements

- Train and validate on a larger, more diverse real-world dataset.
- Add categories and an out-of-scope/needs-review class.
- Use duplicate-aware or time-based validation.
- Compare Logistic Regression with Linear SVM and transformer-based models.
- Calibrate prediction probabilities and validate review thresholds.
- Add multilingual support.
- Build a production REST API.
- Integrate a database and a ticket management platform.
- Introduce human feedback, model monitoring and controlled retraining.

## 17. License and Data Attribution

The dataset is sourced from the Hugging Face dataset repository linked above. Review and comply with the dataset's published license and terms before redistribution or commercial use. Third-party packages remain subject to their respective licenses.

---

**SupportAI** · AI-Powered Customer Support Ticket Classification System  
Built with Python, Scikit-learn and Streamlit.

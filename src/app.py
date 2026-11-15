import re
import html
import joblib
import pandas as pd
import streamlit as st

from pathlib import Path
from theme import initialize_state, get_theme
from styles import inject_styles


# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "model" / "ticket_classifier.pkl"
DATA_FILE = BASE_DIR / "data" / "processed_tickets.csv"

st.set_page_config(
    page_title="SupportAI | Smart Ticket Classification",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

initialize_state()

# Safety initialization: prevent missing session-state keys

DEFAULT_STATE = {
    "dark_mode": True,
    "history": [],
    "last_result": None,
    "last_ticket": "",
    "sample_index": 0,
    "ticket_description": ""
}

for key, default_value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = default_value


# =====================================================
# LOAD THEME
# =====================================================

theme = get_theme()
inject_styles(theme)


# =====================================================
# 2. LOAD MODEL AND DATA
# =====================================================

@st.cache_resource
def load_model():
    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            "Model not found. Run src/train.py first."
        )
    return joblib.load(MODEL_FILE)


@st.cache_data
def load_dataset():
    if not DATA_FILE.exists():
        return None
    return pd.read_csv(DATA_FILE)


try:
    model = load_model()
except Exception as error:
    st.error(f"Unable to load model: {error}")
    st.stop()

df = load_dataset()


# =====================================================
# 3. TEXT PREPROCESSING AND PREDICTION
# =====================================================

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def predict_ticket(description):
    cleaned = clean_text(description)
    if not cleaned:
        return None

    prediction = model.predict([cleaned])[0]
    probabilities = model.predict_proba([cleaned])[0]
    categories = model.named_steps["classifier"].classes_

    results = pd.DataFrame({
        "Category": categories,
        "Probability": probabilities * 100
    }).sort_values(
        "Probability", ascending=False
    ).reset_index(drop=True)

    return {
        "prediction": prediction,
        "confidence": float(results.iloc[0]["Probability"]),
        "probabilities": results
    }


# =====================================================
# 4. SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("""
        <div class="brand-lockup">
            <div class="brand-mark">⚡</div>
            <div>
                <div class="brand-name">SupportAI</div>
                <div class="brand-caption">INTELLIGENT SUPPORT</div>
            </div>
        </div>
        <span class="online-pill">● SYSTEM ONLINE</span>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**WORKSPACE**")

    page = st.radio(
        "Navigation",
        ["Dashboard", "Classify Ticket", "Prediction History", "About Model"],
        label_visibility="collapsed"
    )

    st.divider()
    st.markdown("**APPEARANCE**")

    theme_choice = st.toggle(
        "Light theme",
        value=not st.session_state.dark_mode,
        key="light_theme_toggle"
    )

    new_dark_mode = not theme_choice
    if new_dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = new_dark_mode
        st.rerun()

    st.caption("Glass · Electric blue · Gradient")

    st.divider()
    st.markdown("**MODEL STATUS**")
    st.success("Model loaded successfully")
    st.caption("TF-IDF + Logistic Regression")

    if st.button("Clear prediction history", use_container_width=True):
        st.session_state.history = []
        st.rerun()

    st.markdown(
        '<div class="footer">SUPPORTAI v1.0<br>POWERED BY MACHINE LEARNING</div>',
        unsafe_allow_html=True
    )


# =====================================================
# 5. SHARED PAGE HEADER
# =====================================================

def page_header(kicker, title, subtitle):
    st.markdown(
        f'<div class="eyebrow">{html.escape(kicker)}</div>'
        f'<div class="page-title">{html.escape(title)}</div>'
        f'<div class="page-subtitle">{html.escape(subtitle)}</div>',
        unsafe_allow_html=True
    )

# =====================================================
# TICKET ACTIONS
# =====================================================

SAMPLE_TICKETS = [
    "I cannot log in to my account even after resetting my password.",
    "I was charged twice for my monthly invoice.",
    "The application crashes whenever I try to open the dashboard.",
    "My records are not syncing between my devices.",
    "I want to request a refund for my recent purchase.",
    "The application takes too long to load and responds very slowly.",
    "I want to update my registered email address.",
    "I am having trouble connecting our application to the API.",
    "I noticed suspicious activity on my account.",
    "Can someone guide me through setting up my new account?"
]


def clear_ticket():
    """Clear the current ticket and its displayed result."""

    st.session_state.ticket_description = ""
    st.session_state.last_result = None
    st.session_state.last_ticket = ""


def load_sample_ticket():
    """Load the next sample ticket."""

    index = st.session_state.sample_index % len(SAMPLE_TICKETS)

    st.session_state.ticket_description = SAMPLE_TICKETS[index]

    st.session_state.sample_index += 1

    # Remove the previous result when loading a new sample.
    st.session_state.last_result = None
    st.session_state.last_ticket = ""

# =====================================================
# 6. DASHBOARD
# =====================================================

if page == "Dashboard":
    page_header(
        "WORKSPACE / OVERVIEW",
        "Customer Support Dashboard",
        "A clear view of your AI-powered ticket classification workspace."
    )

    total_tickets = len(df) if df is not None else 0
    total_categories = df["category"].nunique() if df is not None else 0
    total_predictions = len(st.session_state.history)

    c1, c2, c3 = st.columns(3)
    c1.metric("Dataset tickets", f"{total_tickets:,}", "Available records")
    c2.metric("Ticket categories", total_categories, "Classification classes")
    c3.metric("Predictions made", total_predictions, "This session")

    st.write("")
    st.markdown('<div class="section-title">System overview</div>', unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:
        with st.container(border=True):
            st.markdown("### ⚡ AI classification")
            st.write(
                "Automatically classify customer support tickets "
                "using Natural Language Processing."
            )
            st.caption("TF-IDF vectorization · Logistic Regression")
            st.markdown('<span class="online-pill">READY TO CLASSIFY</span>', unsafe_allow_html=True)

    with right:
        with st.container(border=True):
            st.markdown("### ◈ Model status")
            st.markdown('<span class="online-pill">● ACTIVE AND READY</span>', unsafe_allow_html=True)
            st.write("Your trained machine learning pipeline is loaded.")

    if df is not None:
        st.write("")
        st.markdown('<div class="section-title">Ticket category distribution</div>', unsafe_allow_html=True)
        category_counts = (
            df["category"].value_counts()
            .rename_axis("Category")
            .reset_index(name="Tickets")
        )
        st.bar_chart(
            category_counts.set_index("Category"),
            color=theme["chart"]
        )
    else:
        st.warning("Dataset file is unavailable.")


# =====================================================
# CLASSIFY TICKET
# =====================================================

elif page == "Classify Ticket":

    page_header(
        "AI WORKSPACE / CLASSIFIER",
        "Classify a support ticket",
        "Describe the customer's issue and let SupportAI predict its category."
    )

    # -----------------------------------------------
    # TICKET INPUT CARD
    # -----------------------------------------------

    with st.container(border=True):

        st.markdown("### ✨ New support ticket")

        st.caption(
            "Use a clear description of the customer's problem."
        )

        with st.form(
            "ticket_form",
            clear_on_submit=False
        ):

            description = st.text_area(

                "Ticket description",

                placeholder=(
                    "Example: I cannot access my account "
                    "even after resetting my password..."
                ),

                height=165,

                key="ticket_description"

            )

            submitted = st.form_submit_button(

                "⚡  Classify Ticket",

                use_container_width=True

            )

        # -------------------------------------------
        # SECONDARY ACTION BUTTONS
        # -------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.button(

                "＋  Try Sample Ticket",

                key="sample_button",

                use_container_width=True,

                on_click=load_sample_ticket

            )

        with col2:

            st.button(

                "✕  Clear Ticket",

                key="clear_button",

                use_container_width=True,

                on_click=clear_ticket

            )

    # -----------------------------------------------
    # PROCESS CLASSIFICATION
    # -----------------------------------------------

    if submitted:

        if not description.strip():

            st.warning(
                "Please enter a ticket description."
            )

        else:

            result = predict_ticket(description)

            if result is not None:

                # Save prediction history

                st.session_state.history.append({

                    "Ticket": description,

                    "Category": result["prediction"],

                    "Confidence": result["confidence"]

                })

                # Save current result

                st.session_state.last_result = result

                st.session_state.last_ticket = description

    # -----------------------------------------------
    # DISPLAY CLASSIFICATION RESULT
    # -----------------------------------------------

    result = st.session_state.last_result

    if result is not None:

        st.write("")

        st.markdown(
            '<div class="section-title">'
            'Classification result'
            '</div>',
            unsafe_allow_html=True
        )

        result_html = f"""
        <div class="result-panel">
            <div class="result-kicker">PREDICTED CATEGORY</div>
            <div class="result-category">{html.escape(str(result["prediction"]))}</div>
        </div>
        """
        st.markdown(
            result_html,
            unsafe_allow_html=True
        )

        

        st.write("")

        # -------------------------------------------
        # CONFIDENCE METRICS
        # -------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Prediction Confidence",
                f'{result["confidence"]:.2f}%'
            )

        with col2:

            st.metric(
                "Categories Analyzed",
                len(result["probabilities"])
            )

        st.progress(

            min(
                max(result["confidence"] / 100, 0),
                1
            )

        )

        # -------------------------------------------
        # LOW CONFIDENCE WARNING
        # -------------------------------------------

        if result["confidence"] < 30:

            st.warning(

                "Low-confidence prediction. "
                "Please review this ticket manually. "
                "The 30% threshold is provisional "
                "and is not a validated confidence boundary."

            )

        st.write("")

        # -------------------------------------------
        # TOP 5 PREDICTIONS
        # -------------------------------------------

        st.markdown(

            '<div class="section-title">'
            'Top 5 predicted categories'
            '</div>',

            unsafe_allow_html=True

        )

        top_five = result["probabilities"].head(5)

        for _, row in top_five.iterrows():

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(
                    f"**{row['Category']}**"
                )

            with col2:

                st.markdown(
                    f"**{row['Probability']:.2f}%**"
                )

            st.progress(

                min(
                    max(float(row["Probability"]) / 100, 0),
                    1
                )

            )

        st.write("")

        # -------------------------------------------
        # COMPLETE PROBABILITY DISTRIBUTION
        # -------------------------------------------

        with st.expander(
            "View Complete Probability Distribution"
        ):

            st.bar_chart(

                result["probabilities"].set_index(
                    "Category"
                ),

                color=theme["chart"]

            )


# =====================================================
# 8. PREDICTION HISTORY
# =====================================================

elif page == "Prediction History":
    page_header(
        "WORKSPACE / ACTIVITY",
        "Prediction history",
        "Review and export the tickets classified in this session."
    )

    if not st.session_state.history:
        with st.container(border=True):
            st.info("No predictions yet. Classify a ticket to start building your history.")
    else:
        history_df = pd.DataFrame(st.session_state.history)

        c1, c2 = st.columns(2)
        c1.metric("Total predictions", len(history_df))
        c2.metric("Unique categories", history_df["Category"].nunique())

        st.write("")
        st.markdown('<div class="section-title">Classification records</div>', unsafe_allow_html=True)
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Download prediction history",
            data=csv,
            file_name="prediction_history.csv",
            mime="text/csv",
            use_container_width=True
        )


# =====================================================
# 9. ABOUT MODEL
# =====================================================

elif page == "About Model":
    page_header(
        "SUPPORTAI / TECHNOLOGY",
        "About the model",
        "The machine learning pipeline behind customer support classification."
    )

    with st.container(border=True):
        st.markdown("### 🧠 Model architecture")
        st.write(
            "SupportAI is a supervised machine learning application "
            "that classifies customer support ticket descriptions."
        )
        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Algorithm**")
            st.write("Logistic Regression")
            st.markdown("**Text vectorization**")
            st.write("TF-IDF")
            st.markdown("**Learning type**")
            st.write("Supervised learning")
        with c2:
            st.markdown("**Problem type**")
            st.write("Multiclass text classification")
            st.markdown("**Framework**")
            st.write("Scikit-learn")
            st.markdown("**Model serialization**")
            st.write("Joblib")

    st.write("")
    st.markdown('<div class="section-title">Supported ticket categories</div>', unsafe_allow_html=True)

    categories = model.named_steps["classifier"].classes_
    category_cols = st.columns(2)

    for index, category in enumerate(categories):
        with category_cols[index % 2]:
            with st.container(border=True):
                st.markdown(f"🔹 **{category}**")

    st.write("")
    with st.container(border=True):
        st.markdown("### ⚙️ How SupportAI works")
        steps = [
            ("01", "Customer input", "The user enters a support ticket."),
            ("02", "Text preprocessing", "The text is cleaned and normalized."),
            ("03", "TF-IDF vectorization", "Text is converted into numerical features."),
            ("04", "Logistic Regression", "The model predicts the most likely category."),
            ("05", "Prediction output", "The app displays the category and estimated probabilities.")
        ]
        for number, title, detail in steps:
            st.markdown(f"**{number} — {title}**")
            st.caption(detail)


# =====================================================
# 10. FOOTER
# =====================================================

st.divider()
st.markdown(
    '<div class="footer"><b>⚡ SupportAI</b> · AI-Powered Customer Support Ticket Classification'
    '<br>Built with Python · Scikit-learn · Streamlit</div>',
    unsafe_allow_html=True
)

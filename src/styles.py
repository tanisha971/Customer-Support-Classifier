import streamlit as st

def inject_styles(theme):
    st.markdown(f"""
    <style>
    :root {{
        --bg: {theme["bg"]};
        --sidebar: {theme["sidebar"]};
        --surface: {theme["surface"]};
        --surface-strong: {theme["surface_strong"]};
        --input: {theme["input"]};
        --text: {theme["text"]};
        --muted: {theme["muted"]};
        --border: {theme["border"]};
        --blue: {theme["blue"]};
        --blue2: {theme["blue2"]};
        --cyan: {theme["cyan"]};
        --shadow: {theme["shadow"]};
        --result: {theme["result"]};
    }}

    html, body, [data-testid="stAppViewContainer"], .stApp {{
        background: var(--bg) !important;
        color: var(--text) !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background:
            radial-gradient(ellipse at 82% 12%, rgba(33, 105, 255, .19), transparent 32%),
            radial-gradient(ellipse at 93% 62%, rgba(255, 104, 62, .10), transparent 27%),
            radial-gradient(ellipse at 18% 88%, rgba(105, 77, 255, .13), transparent 30%),
            var(--bg) !important;
        background-attachment: fixed !important;
    }}

    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .block-container {{
        max-width: 1480px;
        padding-top: 2.1rem;
        padding-bottom: 3rem;
    }}

    [data-testid="stSidebar"] {{
        background: var(--sidebar) !important;
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-right: 1px solid var(--border);
    }}
    [data-testid="stSidebar"] > div:first-child {{
        background: transparent !important;
    }}

    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {{
        color: var(--text);
    }}
    [data-testid="stCaptionContainer"], .stCaption {{
        color: var(--muted) !important;
    }}

    /* Glass cards: Streamlit bordered containers and metrics */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMetric"],
    [data-testid="stExpander"] {{
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        border-radius: 20px !important;
        box-shadow: var(--shadow);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
    }}
    [data-testid="stVerticalBlockBorderWrapper"] {{
        padding: 1rem 1.1rem;
    }}
    [data-testid="stMetric"] {{
        padding: 18px 20px;
    }}
    [data-testid="stMetricLabel"] p {{
        color: var(--muted) !important;
        font-size: .78rem;
        letter-spacing: .07em;
        text-transform: uppercase;
        font-weight: 700;
    }}
    [data-testid="stMetricValue"] {{
        color: var(--text) !important;
        font-weight: 800;
    }}
    [data-testid="stMetricDelta"] {{
        color: var(--cyan) !important;
    }}

    /* Gradient action buttons */
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {{
        color: #fff !important;
        background: linear-gradient(110deg, var(--blue), var(--blue2)) !important;
        border: 1px solid rgba(255,255,255,.18) !important;
        border-radius: 13px !important;
        font-weight: 750 !important;
        min-height: 2.75rem;
        box-shadow: 0 8px 24px rgba(43, 105, 255, .25);
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
    }}
    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover {{
        color: #fff !important;
        filter: brightness(1.12);
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(43, 105, 255, .38);
        border-color: rgba(255,255,255,.35) !important;
    }}
    div.stButton > button:focus,
    div.stFormSubmitButton > button:focus,
    div.stDownloadButton > button:focus {{
        color: #fff !important;
        box-shadow: 0 0 0 3px rgba(57, 139, 255, .25);
    }}

    /* Secondary glass buttons */

div[data-testid="stButton"] button[kind="secondary"] {{
    background: rgba(70, 125, 220, 0.08) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}}

div[data-testid="stButton"] button[kind="secondary"]:hover {{
    background: rgba(57, 139, 255, 0.16) !important;
    border-color: var(--blue) !important;
    color: var(--text) !important;
    transform: translateY(-2px);
    box-shadow: 0 7px 20px rgba(43, 105, 255, 0.15) !important;
}}

    /* Inputs */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {{
        color: var(--text) !important;
        background: var(--input) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(12px);
    }}
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stTextInput"] input:focus {{
        border-color: var(--blue) !important;
        box-shadow: 0 0 0 3px rgba(57, 139, 255, .13) !important;
    }}
    [data-testid="stTextArea"] textarea::placeholder {{
        color: var(--muted) !important;
    }}

    /* Radio navigation */
    [data-testid="stRadio"] > div {{
        gap: .35rem;
    }}
    [data-testid="stRadio"] label {{
        color: var(--text) !important;
        padding: .35rem .45rem;
        border-radius: 10px;
    }}

    /* Toggle and progress */
    [data-testid="stToggle"] label {{
        color: var(--text) !important;
    }}
    [data-testid="stProgressBar"] > div {{
        background: rgba(120, 150, 200, .18) !important;
        border-radius: 20px;
    }}
    [data-testid="stProgressBar"] > div > div {{
        background: linear-gradient(90deg, var(--blue), var(--cyan), var(--blue2)) !important;
        border-radius: 20px;
    }}

    [data-testid="stDataFrame"], [data-testid="stTable"] {{
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
    }}
    [data-testid="stAlert"] {{
        border-radius: 14px;
        backdrop-filter: blur(14px);
    }}
    hr {{
        border-color: var(--border) !important;
    }}

    .brand-lockup {{
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 0 16px;
    }}
    .brand-mark {{
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        color: white;
        font-size: 23px;
        background: linear-gradient(135deg, var(--blue), var(--blue2));
        box-shadow: 0 8px 24px rgba(49, 115, 255, .38);
    }}
    .brand-name {{
        color: var(--text);
        font-size: 22px;
        font-weight: 850;
        letter-spacing: -.7px;
        line-height: 1.1;
    }}
    .brand-caption {{
        color: var(--muted);
        font-size: 9px;
        font-weight: 750;
        letter-spacing: 1.45px;
        margin-top: 4px;
    }}
    .eyebrow {{
        color: var(--cyan);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: .14em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}
    .page-title {{
        color: var(--text);
        font-size: clamp(27px, 3vw, 36px);
        font-weight: 850;
        letter-spacing: -1.2px;
        line-height: 1.15;
        margin: 0;
    }}
    .page-subtitle {{
        color: var(--muted);
        font-size: 14px;
        margin-top: 9px;
        margin-bottom: 25px;
    }}
    .section-title {{
        color: var(--text);
        font-size: 19px;
        font-weight: 780;
        letter-spacing: -.3px;
        margin: 8px 0 13px;
    }}
    .glass-panel {{
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 22px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
    }}
    .result-panel {{
        background: var(--result);
        border: 1px solid rgba(75, 148, 255, .48);
        border-radius: 18px;
        padding: 23px;
        box-shadow: 0 10px 35px rgba(34, 108, 255, .10);
        backdrop-filter: blur(18px);
    }}
    .result-kicker {{
        color: var(--muted);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .15em;
    }}
    .result-category {{
        color: var(--cyan);
        font-size: clamp(24px, 3vw, 32px);
        font-weight: 850;
        margin-top: 7px;
        overflow-wrap: anywhere;
    }}
    .online-pill {{
        display: inline-block;
        color: #55E0B0;
        background: rgba(42, 190, 139, .10);
        border: 1px solid rgba(42, 190, 139, .25);
        border-radius: 30px;
        padding: 6px 10px;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: .08em;
    }}
    .footer {{
        color: var(--muted);
        text-align: center;
        font-size: 11px;
        line-height: 1.8;
        padding: 10px 0 0;
    }}

    @media (max-width: 700px) {{
        .block-container {{ padding-top: 1rem; }}
        [data-testid="stMetric"] {{ padding: 13px; }}
    }}
    </style>
    """, unsafe_allow_html=True)

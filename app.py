import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Superstore Sales Insights DashBoard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PROFESSIONAL THEME + NAVIGATION ANIMATION
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --ivory: #F7F4EC;
        --ivory-card: #FFFEFA;
        --forest: #244A38;
        --forest-dark: #183629;
        --sage: #DCE7DB;
        --text: #26352C;
        --muted: #647267;
        --border: #D7DED3;
        --gold: #B78A45;
    }
    .stApp {
        background: linear-gradient(135deg, #F7F4EC 0%, #F1F0E7 58%, #E8EEE4 100%);
        color: var(--text);
    }
    .main .block-container { padding-top: 1.2rem; animation: pageFade .35s ease-out; }
    @keyframes pageFade {
        from { opacity: .45; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stSidebar"] {
        background: #E9EEE5;
        border-right: 1px solid #CDD8CA;
    }
    h1, h2, h3, h4, p, li, label, .stMarkdown, .stCaption {
        color: #26352C;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #FFFEFA, #EEF3E9);
        border: 1px solid #D4DED0;
        padding: 15px 17px;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(36,74,56,.07);
    }
    [data-testid="stMetricLabel"] { color: #526455 !important; }
    [data-testid="stMetricValue"] { color: #244A38 !important; }
    [data-testid="stMetricDelta"] { color: #557A5D !important; }
    .hero {
        background: linear-gradient(110deg, #183629, #244A38 65%, #496B50);
        border: 1px solid #496B50;
        border-radius: 17px;
        padding: 21px 25px;
        margin: 0 0 15px 0;
        box-shadow: 0 8px 22px rgba(36,74,56,.12);
    }
    .hero h1 { margin: 0; color: #FFFEFA !important; font-size: 1.9rem; letter-spacing: .2px; }
    .hero p { margin: 5px 0 0 0; color: #E5EDE1 !important; }
    .nav-caption { color: #526455; font-size: .82rem; font-weight: 700; letter-spacing: .08em; margin: 0 0 6px 2px; }
    .takeaway {
        background: #E7EFE3;
        color: #26352C !important;
        border-left: 4px solid #557A5D;
        border-radius: 8px;
        padding: 11px 14px;
        margin: 6px 0 19px 0;
        line-height: 1.5;
    }
    .takeaway strong, .takeaway p { color: #26352C !important; }
    .section-note {
        background: #EEF2E9;
        border: 1px solid #D4DED0;
        padding: 12px 15px;
        border-radius: 10px;
        color: #34463A;
        margin-bottom: 12px;
    }
    div.stButton > button {
        background: #FFFEFA;
        color: #244A38;
        border: 1px solid #C8D5C5;
        border-radius: 10px;
        min-height: 42px;
        font-weight: 650;
        transition: all .18s ease-in-out;
        white-space: nowrap;
    }
    div.stButton > button:hover {
        background: #E7EFE3;
        border-color: #557A5D;
        color: #183629;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(36,74,56,.12);
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #244A38, #496B50);
        color: #FFFEFA;
        border-color: #244A38;
        box-shadow: 0 3px 10px rgba(36,74,56,.18);
    }
    [data-testid="stDataFrame"] { border: 1px solid #D4DED0; border-radius: 9px; }

    /* =====================================================
       FORCE IVORY + FOREST GREEN ON FILTERS AND BUTTONS
       High-specificity BaseWeb selectors prevent default pink/red chips.
       ===================================================== */

    /* Multiselect/select field surfaces */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: #FFFEFA !important;
        background-color: #FFFEFA !important;
        border: 1.5px solid #B9CDB8 !important;
        border-radius: 10px !important;
        color: #183629 !important;
        box-shadow: none !important;
    }

    /* Selected Region / Category / Segment chips: override BaseWeb defaults */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"],
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] > span,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] > div,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] > div > span,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] > div > div {
        background: #244A38 !important;
        background-color: #244A38 !important;
        color: #FFFEFA !important;
        border-color: #244A38 !important;
        border-radius: 7px !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] *,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] path {
        color: #FFFEFA !important;
        fill: #FFFEFA !important;
        stroke: #FFFEFA !important;
        opacity: 1 !important;
    }

    /* Dropdown options and selected option */
    [data-baseweb="popover"] [role="option"] {
        color: #183629 !important;
        background-color: #FFFEFA !important;
    }
    [data-baseweb="popover"] [role="option"]:hover,
    [data-baseweb="popover"] [aria-selected="true"] {
        color: #183629 !important;
        background-color: #DCE7DB !important;
    }

    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="select"]:focus-within > div {
        border-color: #244A38 !important;
        box-shadow: 0 0 0 1px #244A38 !important;
    }
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] [data-baseweb="input"] {
        color: #183629 !important;
    }

    /* Green year-range slider */
    [data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {
        background-color: #244A38 !important;
        border: 2px solid #FFFEFA !important;
        box-shadow: 0 0 0 1px #244A38 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] div {
        accent-color: #244A38 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
        background-color: #244A38 !important;
    }

    /* Reset button: soft sage background + dark readable text */
    [data-testid="stSidebar"] div.stButton > button,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] button[kind="primary"] {
        background: #DCE7DB !important;
        background-color: #DCE7DB !important;
        color: #183629 !important;
        border: 1.5px solid #8FAE91 !important;
        border-radius: 10px !important;
        font-weight: 750 !important;
        box-shadow: 0 3px 10px rgba(24,54,41,.10) !important;
    }
    [data-testid="stSidebar"] div.stButton > button *,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] *,
    [data-testid="stSidebar"] button[kind="primary"] * {
        color: #183629 !important;
        fill: #183629 !important;
    }
    [data-testid="stSidebar"] div.stButton > button:hover,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover,
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background: #C8DCC8 !important;
        background-color: #C8DCC8 !important;
        color: #183629 !important;
        border-color: #244A38 !important;
    }

    /* Main navigation: inactive ivory buttons, active forest-green button */
    [data-testid="stMain"] div.stButton > button,
    section.main div.stButton > button {
        background: #FFFEFA !important;
        background-color: #FFFEFA !important;
        color: #183629 !important;
        border: 1.5px solid #B9CDB8 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 42px;
        white-space: nowrap;
    }
    [data-testid="stMain"] div.stButton > button *,
    section.main div.stButton > button * {
        color: #183629 !important;
        fill: #183629 !important;
    }
    [data-testid="stMain"] div.stButton > button[kind="primary"],
    section.main div.stButton > button[kind="primary"] {
        background: linear-gradient(110deg, #183629, #244A38 70%, #496B50) !important;
        background-color: #183629 !important;
        color: #FFFEFA !important;
        border-color: #244A38 !important;
    }
    [data-testid="stMain"] div.stButton > button[kind="primary"] *,
    section.main div.stButton > button[kind="primary"] * {
        color: #FFFEFA !important;
        fill: #FFFEFA !important;
    }
    [data-testid="stMain"] div.stButton > button:hover,
    section.main div.stButton > button:hover {
        border-color: #244A38 !important;
        box-shadow: 0 3px 10px rgba(24,54,41,.12) !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #244A38 !important;
        font-weight: 650 !important;
    }

    /* FINAL OVERRIDES: selected filter chips (Region, Category, Segment).
       Target BaseWeb tags globally because Streamlit DOM nesting varies by version. */
    [data-baseweb="tag"],
    [data-baseweb="tag"] > span,
    [data-baseweb="tag"] > div,
    [data-baseweb="tag"] > div > span,
    [data-baseweb="tag"] > div > div {
        background: #244A38 !important;
        background-color: #244A38 !important;
        color: #FFFEFA !important;
        border-color: #244A38 !important;
        border-radius: 7px !important;
        box-shadow: none !important;
    }
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] svg,
    [data-baseweb="tag"] path {
        color: #FFFEFA !important;
        fill: #FFFEFA !important;
        stroke: #FFFEFA !important;
        opacity: 1 !important;
    }

    /* Smooth transitions + readable labels on every Streamlit button. */
    div.stButton > button,
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {
        transition: background-color .30s ease, color .30s ease,
                    border-color .30s ease, box-shadow .30s ease,
                    transform .30s ease !important;
        font-weight: 700 !important;
    }
    div.stButton > button span,
    div.stButton > button p,
    [data-testid="stBaseButton-secondary"] span,
    [data-testid="stBaseButton-secondary"] p {
        color: #183629 !important;
        opacity: 1 !important;
    }
    /* Reset button: light sage so the label stays visible. */
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: #DCE7DB !important;
        background-color: #DCE7DB !important;
        color: #183629 !important;
        border: 1.5px solid #8FAE91 !important;
        box-shadow: 0 3px 10px rgba(24,54,41,.10) !important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] span,
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"] p,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] span,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] p {
        color: #183629 !important;
    }
    [data-testid="stSidebar"] [data-testid="stBaseButton-primary"]:hover,
    [data-testid="stSidebar"] div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 13px rgba(24,54,41,.16) !important;
    }
    /* Navigation buttons: clear text, dark-green active state, smooth hover. */
    [data-testid="stMain"] div.stButton > button,
    section.main div.stButton > button {
        transition: all .30s ease-in-out !important;
    }
    [data-testid="stMain"] div.stButton > button[kind="primary"] span,
    [data-testid="stMain"] div.stButton > button[kind="primary"] p,
    section.main div.stButton > button[kind="primary"] span,
    section.main div.stButton > button[kind="primary"] p {
        color: #FFFEFA !important;
        opacity: 1 !important;
    }
    [data-testid="stMain"] div.stButton > button:not([kind="primary"]):hover,
    section.main div.stButton > button:not([kind="primary"]):hover {
        background: #DCE7DB !important;
        color: #183629 !important;
        border-color: #244A38 !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 13px rgba(24,54,41,.14) !important;
    }
    [data-testid="stMain"] div.stButton > button[kind="primary"]:hover,
    section.main div.stButton > button[kind="primary"]:hover {
        background: linear-gradient(110deg, #244A38, #496B50) !important;
        color: #FFFEFA !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 13px rgba(24,54,41,.2) !important;
    }
    /* HARD OVERRIDE for selected multiselect chips (Regions, Categories, Segments).
       Keep the Reset button unchanged; only recolor selected values. */
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"],
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] > div,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] > span,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] button,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] [data-baseweb="tag"] [role="button"] {
        background: #244A38 !important;
        background-color: #244A38 !important;
        color: #FFFFFF !important;
        border-color: #244A38 !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] *,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] svg,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"] path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"]:hover,
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="tag"]:hover > div {
        background: #183629 !important;
        background-color: #183629 !important;
        color: #FFFFFF !important;
    }

    /* LAST-RESORT THEME TOKEN OVERRIDES: Streamlit uses its primary color for
       selected multiselect tags and the slider's active track/handles. */
    :root,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] {
        --primary-color: #244A38 !important;
        --st-primary-color: #244A38 !important;
        --primary: #244A38 !important;
        --colors-primary: #244A38 !important;
    }

    /* Actual BaseWeb chip root (and descendants) used by Streamlit versions. */
    [data-testid="stMultiSelect"] [data-baseweb="tag"],
    [data-testid="stMultiSelect"] [data-baseweb="tag"] > span,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] > div > span,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] [role="button"],
    [data-testid="stMultiSelect"] [data-baseweb="tag"] button {
        background: #244A38 !important;
        background-color: #244A38 !important;
        color: #FFFFFF !important;
        border-color: #244A38 !important;
        box-shadow: none !important;
        opacity: 1 !important;
    }
    [data-testid="stMultiSelect"] [data-baseweb="tag"] *,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] svg,
    [data-testid="stMultiSelect"] [data-baseweb="tag"] path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
    }

    /* Streamlit slider: only the active rail and handles, not the whole widget. */
    [data-testid="stSlider"] [role="slider"] {
        background: #244A38 !important;
        background-color: #244A38 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 0 0 0 1px #244A38 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"] {
        background: #244A38 !important;
        background-color: #244A38 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
        background: #244A38 !important;
        background-color: #244A38 !important;
    }

    /* FINAL FORCE: selected filter chips + year range must be forest green. */
    [data-baseweb="tag"],
    [data-baseweb="tag"]:not(:hover),
    [data-baseweb="tag"] > div,
    [data-baseweb="tag"] > span,
    [data-baseweb="tag"] [role="button"],
    [data-baseweb="tag"] button {
        background: #244A38 !important;
        background-color: #244A38 !important;
        color: #FFFFFF !important;
        border-color: #244A38 !important;
        --tag-background: #244A38 !important;
        --tag-color: #FFFFFF !important;
    }
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] svg,
    [data-baseweb="tag"] path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }
    /* Green active rail and handles for the year range slider. */
    [data-testid="stSlider"] [role="slider"] {
        background-color: #244A38 !important;
        border-color: #FFFFFF !important;
        box-shadow: 0 0 0 2px #244A38 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] > div > div,
    [data-testid="stSlider"] [data-baseweb="slider"] [role="presentation"],
    [data-testid="stSlider"] [data-baseweb="slider"] div[style*="background"] {
        background: #244A38 !important;
        background-color: #244A38 !important;
    }
    [data-testid="stSlider"] [data-baseweb="slider"] [aria-valuenow] {
        background: #244A38 !important;
    }

    hr { border-color: #D4DED0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_header():
    st.markdown(
        """
        <div class="hero">
            <h1>📊 Superstore Sales Insights</h1>
            <p>Retail Performance&nbsp; • &nbsp;Sales Trends&nbsp; • &nbsp;Profitability Analytics</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def takeaway(message):
    st.markdown(
        f'<div class="takeaway"><strong>Key takeaway:</strong> {message}</div>',
        unsafe_allow_html=True,
    )


def money(value):
    return f"${value:,.2f}"


@st.cache_data

def load_data(path):
    """Read the source CSV using the latin-1 encoding specified in the brief."""
    return pd.read_csv(path, encoding="latin-1")


def clean_data(raw):
    """Clean the required fields and return both the cleaned frame and audit counts."""
    data = raw.copy()
    required = [
        "Order Date", "Region", "Category", "Sub-Category",
        "Sales", "Quantity", "Discount", "Profit",
    ]
    missing_columns = [column for column in required if column not in data.columns]
    if missing_columns:
        raise ValueError("CSV is missing required column(s): " + ", ".join(missing_columns))

    starting_rows = len(data)
    source_missing_sales = int(data["Sales"].isna().sum())
    source_missing_profit = int(data["Profit"].isna().sum())

    # Convert dates and numeric fields. Invalid strings become NaN so they can
    # be counted and handled transparently instead of silently breaking charts.
    data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")
    invalid_dates = int(data["Order Date"].isna().sum())
    invalid_numeric_by_column = {}
    for column in ["Sales", "Profit", "Quantity", "Discount"]:
        was_present = data[column].notna()
        data[column] = pd.to_numeric(data[column], errors="coerce")
        invalid_numeric_by_column[column] = int((was_present & data[column].isna()).sum())

    critical = [
        "Order Date", "Region", "Category", "Sub-Category",
        "Sales", "Profit", "Quantity", "Discount",
    ]
    missing_mask = data[critical].isna().any(axis=1)
    missing_removed = int(missing_mask.sum())
    data = data.loc[~missing_mask].copy()

    # Remove impossible values only after missing/invalid rows have been removed,
    # so the two audit counts do not count the same row twice.
    impossible_mask = (data["Sales"] <= 0) | (data["Quantity"] <= 0)
    impossible_removed = int(impossible_mask.sum())
    data = data.loc[~impossible_mask].copy()

    # Required feature engineering. Profit Margin is stored as a ratio (Profit / Sales).
    data["Year"] = data["Order Date"].dt.year.astype(int)
    data["Month"] = data["Order Date"].dt.month.astype(int)
    data["Month Name"] = data["Order Date"].dt.strftime("%b")
    data["Day of Week"] = data["Order Date"].dt.day_name()
    data["Year-Month"] = data["Order Date"].dt.to_period("M").astype(str)
    data["Profit Margin"] = data["Profit"] / data["Sales"]
    data["Log Sales"] = np.log1p(data["Sales"])

    audit = {
        "starting_rows": starting_rows,
        "source_missing_sales": source_missing_sales,
        "source_missing_profit": source_missing_profit,
        "invalid_dates": invalid_dates,
        "invalid_numeric_by_column": invalid_numeric_by_column,
        "missing_removed": missing_removed,
        "impossible_removed": impossible_removed,
        "total_removed": starting_rows - len(data),
        "remaining_rows": len(data),
        "duplicate_rows_source": int(raw.duplicated().sum()),
        "remaining_missing_values": int(data[critical].isna().sum().sum()),
    }
    return data, audit


# =========================================================
# LOAD DATA + VALIDATION
# =========================================================
FILE_PATH = "Superstore_Sales-Insights.csv"
try:
    raw_df = load_data(FILE_PATH)
    source_missing_total = int(raw_df.isna().sum().sum())
    source_dtypes = raw_df.dtypes.astype(str).rename("Data Type").to_frame()
    source_missing = raw_df.isna().sum().rename("Missing Values").to_frame()
    df, cleaning_audit = clean_data(raw_df)
except FileNotFoundError:
    st.error("CSV file not found. Keep 'Superstore_Sales-Insights.csv' in the same folder as app.py.")
    st.stop()
except pd.errors.EmptyDataError:
    st.error("The CSV file is empty. Please provide a valid dataset.")
    st.stop()
except UnicodeDecodeError:
    st.error("Could not read the CSV encoding. The assignment specifies encoding='latin-1'.")
    st.stop()
except ValueError as err:
    st.error(str(err))
    st.stop()
except Exception as err:
    st.error(f"Unable to load the dataset: {err}")
    st.stop()

if df.empty:
    st.error("No valid records remain after cleaning. Check the dataset and cleaning rules.")
    st.stop()

# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.markdown("## 🎛️ Dashboard Filters")
st.sidebar.caption("Choose the data you want to explore.")
regions = sorted(df["Region"].dropna().unique().tolist())
categories = sorted(df["Category"].dropna().unique().tolist())
years = sorted(df["Year"].dropna().unique().tolist())
segments = sorted(df["Segment"].dropna().unique().tolist()) if "Segment" in df.columns else []

# Reset filter state before the widgets are created, so Streamlit can safely
# restore each control to its full-dataset selection.
def reset_dashboard_filters():
    st.session_state["filter_regions"] = regions.copy()
    st.session_state["filter_categories"] = categories.copy()
    if "Segment" in df.columns:
        st.session_state["filter_segments"] = segments.copy()
    if len(years) > 1:
        st.session_state["filter_years"] = (int(min(years)), int(max(years)))

st.sidebar.button(
    "↺  Reset All Filters",
    key="reset_all_filters_button",
    on_click=reset_dashboard_filters,
    use_container_width=True,
    type="primary",
    help="Restore all regions, categories, customer segments and order years.",
)

selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=regions,
    default=regions,
    key="filter_regions",
    placeholder="Choose one or more regions",
   
)
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=categories,
    default=categories,
    key="filter_categories",
    placeholder="Choose one or more categories",
    
)

# Customer segment is available in the standard Superstore dataset.
# If a different CSV has no Segment column, keep the dashboard usable and explain why.
if "Segment" in df.columns:
    selected_segments = st.sidebar.multiselect(
        "Select Customer Segment",
        options=segments,
        default=segments,
        key="filter_segments",
        placeholder="Choose customer segments",
        
    )
else:
    selected_segments = None
    st.sidebar.info("Customer Segment filter needs a 'Segment' column in the CSV.")

if len(years) > 1:
    year_range = st.sidebar.slider(
        "Select Order Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years))),
        step=1,
        key="filter_years",
    )
else:
    year_range = (int(years[0]), int(years[0]))
    st.sidebar.caption(f"Available order year: {years[0]}")

filter_mask = (
    df["Region"].isin(selected_regions)
    & df["Category"].isin(selected_categories)
    & df["Year"].between(year_range[0], year_range[1])
)
if selected_segments is not None:
    filter_mask &= df["Segment"].isin(selected_segments)
filtered_df = df.loc[filter_mask].copy()

st.sidebar.divider()
st.sidebar.caption(f"Showing {len(filtered_df):,} of {len(df):,} cleaned records")
st.sidebar.caption("Data source: Sample Superstore CSV")

# =========================================================
# TOP NAVIGATION BAR WITH ACTIVE STATE + PAGE TRANSITION
# =========================================================
page_names = [
    "Dashboard", "Data Overview", "Feature Engineering",
    "Summary Tables", "Charts & Analysis", "Management Insights",
]
page_icons = ["📈", "🧹", "⚙️", "📋", "📊", "💡"]
if "app_page" not in st.session_state or st.session_state.app_page not in page_names:
    st.session_state.app_page = "Dashboard"

show_header()
st.markdown('<div class="nav-caption">NAVIGATE YOUR ANALYSIS</div>', unsafe_allow_html=True)
nav_cols = st.columns(6, gap="small")
for i, page_name in enumerate(page_names):
    with nav_cols[i]:
        if st.button(
            f"{page_icons[i]} {page_name}",
            key=f"top_nav_{i}",
            use_container_width=True,
            type="primary" if st.session_state.app_page == page_name else "secondary",
        ):
            st.session_state.app_page = page_name
            st.rerun()
st.divider()

if filtered_df.empty:
    st.warning("No records match these filters. Select at least one region, category and customer segment, then adjust the order year range.")
    st.stop()

# =========================================================
# PAGE 1 — DASHBOARD
# =========================================================
if st.session_state.app_page == "Dashboard":
    st.subheader("Executive Overview")
    st.markdown('<div class="section-note">A quick view of revenue, profit, margin and regional performance for the selected filters.</div>', unsafe_allow_html=True)
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    margin_pct = (total_profit / total_sales * 100) if total_sales else 0
    order_count = filtered_df["Order ID"].nunique() if "Order ID" in filtered_df.columns else len(filtered_df)
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Sales", money(total_sales))
    k2.metric("Total Profit", money(total_profit))
    k3.metric("Profit Margin", f"{margin_pct:.2f}%")
    k4.metric("Orders / Records", f"{order_count:,}")

    left, right = st.columns([1.45, 1])
    with left:
        st.subheader("Monthly Sales & Profit")
        monthly = filtered_df.groupby("Year-Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        monthly = monthly.sort_values("Year-Month")
        fig, ax1 = plt.subplots(figsize=(9, 4.1))
        ax2 = ax1.twinx()
        l1 = ax1.plot(monthly["Year-Month"], monthly["Sales"], marker="o", linewidth=2, label="Sales")
        l2 = ax2.plot(monthly["Year-Month"], monthly["Profit"], marker="s", linewidth=2, linestyle="--", label="Profit")
        ax1.set_title("Monthly Sales vs Profit")
        ax1.set_xlabel("Year-Month")
        ax1.set_ylabel("Sales ($)")
        ax2.set_ylabel("Profit ($)")
        ax1.tick_params(axis="x", rotation=55, labelsize=8)
        lines = l1 + l2
        ax1.legend(lines, [line.get_label() for line in lines], loc="upper left")
        fig.tight_layout()
        fig.patch.set_facecolor("#FFFEFA")
        ax1.set_facecolor("#FFFEFA")
        ax2.set_facecolor("#FFFEFA")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        if not monthly.empty:
            peak = monthly.loc[monthly["Sales"].idxmax(), "Year-Month"]
            takeaway(f"Sales peak in {peak}. Comparing the profit line with sales to check whether higher revenue is also contributing in generating stronger profit.")
    with right:
        st.subheader("Profit by Region")
        region_profit = filtered_df.groupby("Region", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
        fig, ax = plt.subplots(figsize=(6, 4.1))
        sns.barplot(data=region_profit, x="Region", y="Profit", ax=ax, color="#557A5D")
        ax.axhline(0, color="#B85C50", linewidth=1, linestyle="--")
        ax.set_title("Total Profit by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel("Total Profit ($)")
        ax.tick_params(axis="x", rotation=15)
        fig.tight_layout()
        fig.patch.set_facecolor("#FFFEFA")
        ax.set_facecolor("#FFFEFA")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        if not region_profit.empty:
            takeaway(f"{region_profit.iloc[0]['Region']} has the highest total profit in the selected data; {region_profit.iloc[-1]['Region']} has the lowest.")

# =========================================================
# PAGE 2 — DATA OVERVIEW, INSPECTION + CLEANING
# =========================================================
elif st.session_state.app_page == "Data Overview":
    st.subheader("Data Preview & Inspection")
    st.markdown(
        '<div class="section-note">This inspection is performed before cleaning so the data structure and cleaning decisions are transparent.</div>',
        unsafe_allow_html=True,
    )
    a, b, c, d = st.columns(4)
    a.metric("Original Rows", f"{len(raw_df):,}")
    b.metric("Original Columns", f"{len(raw_df.columns):,}")
    c.metric("Missing Cells", f"{source_missing_total:,}")
    d.metric("Duplicate Rows", f"{int(raw_df.duplicated().sum()):,}")

    st.markdown("#### Column Names")
    st.write(raw_df.columns.tolist())
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Column Data Types")
        st.dataframe(source_dtypes, use_container_width=True)
    with col2:
        st.markdown("#### Missing Values by Column")
        st.dataframe(source_missing, use_container_width=True)
    st.markdown("#### Descriptive Statistics ")
    st.dataframe(raw_df.describe(include="all").T, use_container_width=True)
    st.markdown("#### Original Dataset Preview (first 10 rows)")
    st.dataframe(raw_df.head(10), use_container_width=True)
    st.caption("Inspection Takeaway: These checks the dataset structure, variable types, missingness and initial statistical ranges before rows are removed.")

    st.divider()
    st.subheader("Data Cleaning & Validation")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows Before Cleaning", f"{cleaning_audit['starting_rows']:,}")
    c2.metric("Rows Removed: Missing / Invalid", f"{cleaning_audit['missing_removed']:,}")
    c3.metric("Rows Removed: Impossible Values", f"{cleaning_audit['impossible_removed']:,}")
    c4.metric("Rows After Cleaning", f"{cleaning_audit['remaining_rows']:,}")

    st.markdown("#### Missing Values and Conversion Checks")
    missing_detail = pd.DataFrame({
        "Check": [
            "Sales values missing in source",
            "Profit values missing in source",
            "Order Date values invalid after conversion",
            "Sales values that could not be converted to numbers",
            "Profit values that could not be converted to numbers",
            "Quantity values that could not be converted to numbers",
            "Discount values that could not be converted to numbers",
        ],
        "Count": [
            cleaning_audit["source_missing_sales"],
            cleaning_audit["source_missing_profit"],
            cleaning_audit["invalid_dates"],
            cleaning_audit["invalid_numeric_by_column"]["Sales"],
            cleaning_audit["invalid_numeric_by_column"]["Profit"],
            cleaning_audit["invalid_numeric_by_column"]["Quantity"],
            cleaning_audit["invalid_numeric_by_column"]["Discount"],
        ],
    })
    st.dataframe(missing_detail, use_container_width=True, hide_index=True)

    cleaning_steps = pd.DataFrame({
        "Cleaning stage": [
            "Original dataset",
            "Rows removed for missing / invalid critical fields",
            "Rows removed for Sales ≤ 0 or Quantity ≤ 0",
            "Final cleaned dataset",
        ],
        "Rows": [
            cleaning_audit["starting_rows"],
            cleaning_audit["missing_removed"],
            cleaning_audit["impossible_removed"],
            cleaning_audit["remaining_rows"],
        ],
        "Explanation": [
            "Number of records read from the CSV before cleaning.",
            "Rows with missing required values or failed date/numeric conversion were excluded so calculations are not based on incomplete critical fields.",
            "The assignment asks to remove non-positive Sales or Quantity values for this analysis.",
            "Records remaining for feature engineering, summary tables and charts.",
        ],
    })
    st.dataframe(cleaning_steps, use_container_width=True, hide_index=True)

    st.markdown("#### Cleaning Decisions Explained")
    st.write("1. **Order Date:** Converted to a real datetime value. Unreadable dates become invalid and their rows are excluded from the analysis.")
    st.write("2. **Missing Sales and Profit:** Rows with missing Sales or Profit are removed rather than filling them with invented values. This avoids fabricating revenue or profit; the original missing counts and overall removed-row counts are displayed above.")
    st.write("3. **Impossible values:** Records with Sales ≤ 0 or Quantity ≤ 0 are removed after incomplete records, as specified in the assignment.")
    st.write("4. **Negative Profit:** Retained because a negative profit is a meaningful loss and is essential to identifying unprofitable products or regions.")
    
    st.markdown("#### Cleaned Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.success(f"Cleaning complete: {cleaning_audit['total_removed']:,} rows removed in total; {cleaning_audit['remaining_rows']:,} rows remain for analysis.")

# =========================================================
# PAGE 3 — FEATURE ENGINEERING + SKEWNESS CHARTS
# =========================================================
elif st.session_state.app_page == "Feature Engineering":
    st.subheader("Feature Engineering & Skewness Analysis")
    st.markdown('<div class="section-note">This section creates date and financial features, then compares the distribution of Sales before and after log transformation.</div>', unsafe_allow_html=True)

    feature_cols = ["Order Date", "Year", "Month", "Month Name", "Day of Week", "Sales", "Profit", "Profit Margin", "Log Sales"]
    st.markdown("#### Engineered Feature Preview")
    st.dataframe(filtered_df[feature_cols].head(12), use_container_width=True)

    sales_skew_before = filtered_df["Sales"].skew()
    sales_skew_after = filtered_df["Log Sales"].skew()
    s1, s2, s3 = st.columns(3)
    s1.metric("Log Sales Skewness — Before", f"{sales_skew_before:.3f}" if pd.notna(sales_skew_before) else "N/A")
    s2.metric("Log Sales Skewness — After", f"{sales_skew_after:.3f}" if pd.notna(sales_skew_after) else "N/A")
    if pd.notna(sales_skew_before) and pd.notna(sales_skew_after):
        skew_change = abs(sales_skew_before) - abs(sales_skew_after)
        s3.metric("Reduction in |Skewness|", f"{skew_change:.3f}", delta="Improved symmetry" if skew_change > 0 else "No reduction")
    else:
        s3.metric("Reduction in |Skewness|", "N/A")

    st.markdown("#### Distribution Charts — Before vs After Transformation")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        sns.histplot(filtered_df["Sales"], bins=35, kde=True, stat="density", color="#557A5D", ax=ax)
        ax.set_title("Original Sales Distribution")
        ax.set_xlabel("Sales ($)")
        ax.set_ylabel("Density")
        fig.tight_layout()
        fig.patch.set_facecolor("#FFFEFA")
        ax.set_facecolor("#FFFEFA")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    with chart_right:
        fig, ax = plt.subplots(figsize=(7, 4.2))
        sns.histplot(filtered_df["Log Sales"], bins=35, kde=True, stat="density", color="#B78A45", ax=ax)
        ax.set_title("Log-Transformed Sales Distribution")
        ax.set_xlabel("Log Sales (Sales)")
        ax.set_ylabel("Density")
        fig.tight_layout()
        fig.patch.set_facecolor("#FFFEFA")
        ax.set_facecolor("#FFFEFA")
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    skew_compare = pd.DataFrame({
        "Distribution": ["Original Sales", "Log Sales"],
        "Skewness": [sales_skew_before, sales_skew_after],
    })
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(skew_compare["Distribution"], skew_compare["Skewness"], color=["#557A5D", "#B78A45"])
    ax.axhline(0, color="#647267", linewidth=0.9)
    ax.set_title("Skewness Before and After")
    ax.set_xlabel("")
    ax.set_ylabel("Skewness")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.markdown("#### What Transformation Means")
    st.write("- **Year, Month, Month Name and Day of Week** are extracted from Order Date to support seasonal and calendar analysis.")
    st.write("- **Profit Margin : Profit / Sales** is stored as a ratio. It can be expressed as a percentage by multiplying by 100 when displayed.")
    st.write("- **Log Sales :** Compressing very large sales values while retaining zero-safe mathematical behaviour.")
    if pd.notna(sales_skew_before) and pd.notna(sales_skew_after):
        if abs(sales_skew_after) < abs(sales_skew_before):
            st.success(f"In this filtered dataset, absolute skewness decreased from {abs(sales_skew_before):.3f} to {abs(sales_skew_after):.3f}. The log transformation made the distribution less skewed, Although it may not make it perfectly normal.")
        elif abs(sales_skew_after) > abs(sales_skew_before):
            st.info(f"In this filtered dataset, absolute skewness increased from {abs(sales_skew_before):.3f} to {abs(sales_skew_after):.3f}. The log transformation did not reduce skewness for this selection; the displayed charts show the actual result.")
        else:
            st.info("Absolute skewness is approximately unchanged for this selection. Compare the two histograms to inspect the shape of the distributions.")

# =========================================================
# PAGE 4 — REQUIRED SUMMARY TABLES
# =========================================================
elif st.session_state.app_page == "Summary Tables":
    st.subheader("Summary Tables & Interpretation")
    st.markdown("#### 1. Category Performance")
    group_columns = {
        "Total Sales": ("Sales", "sum"),
        "Total Profit": ("Profit", "sum"),
        "Average Discount": ("Discount", "mean"),
    }
    category_summary = filtered_df.groupby("Category").agg(**group_columns).reset_index()
    st.dataframe(
        category_summary.style.format({"Total Sales": "${:,.2f}", "Total Profit": "${:,.2f}", "Average Discount": "{:.1%}"}),
        use_container_width=True,
    )
    st.write("**Interpretation:** This table combines all filtered orders within each product category. Total Sales and Total Profit show the scale of revenue and profitability, while Average Discount shows the typical discount level. A category with high sales but comparatively low profit deserves a closer review of discounting and costs.")

    st.divider()
    st.markdown("#### 2. Profit by Region and Category")
    profit_pivot = pd.pivot_table(
        filtered_df, index="Region", columns="Category", values="Profit", aggfunc="sum", fill_value=0
    )
    st.dataframe(profit_pivot.style.format("${:,.2f}"), use_container_width=True)
    st.write("**Interpretation:** Rows represent regions and columns represent product categories; each cell is the total profit for that combination. Negative values identify region-category combinations that lose money, while positive values identify profitable combinations. Management can use this view to target further investigation without assuming that one result applies to every region.")

# =========================================================
# PAGE 5 — FIVE REQUIRED CHARTS
# =========================================================
elif st.session_state.app_page == "Charts & Analysis":
    st.subheader("Charts & Analysis")
    st.caption("All charts respond to the Region, Category, Customer Segment and Order Year filters in the sidebar.")

    # Chart 1: Seaborn box plot
    st.markdown("#### Chart 1 — Box Plot of Profit by Category")
    fig, ax = plt.subplots(figsize=(9, 4.2))
    sns.boxplot(data=filtered_df, x="Category", y="Profit", ax=ax)
    ax.set_title("Profit Distribution by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Profit ($)")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    medians = filtered_df.groupby("Category")["Profit"].median()
    if not medians.empty:
        takeaway(f"{medians.idxmax()} has the highest median transaction profit in this selection. The boxes show the middle spread and the points beyond whiskers indicate outliers.")

    st.divider()
    # Chart 2: Matplotlib dual-axis line chart
    st.markdown("#### Chart 2 — Dual-Axis Monthly Sales and Profit")
    monthly = filtered_df.groupby("Year-Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).sort_values("Year-Month")
    fig, ax1 = plt.subplots(figsize=(10, 4.4))
    ax2 = ax1.twinx()
    l1 = ax1.plot(monthly["Year-Month"], monthly["Sales"], marker="o", linewidth=2, label="Sales")
    l2 = ax2.plot(monthly["Year-Month"], monthly["Profit"], marker="s", linewidth=2, linestyle="--", label="Profit")
    ax1.set_title("Monthly Sales and Profit Trends")
    ax1.set_xlabel("Year-Month")
    ax1.set_ylabel("Sales ($)")
    ax2.set_ylabel("Profit ($)")
    ax1.tick_params(axis="x", rotation=55, labelsize=8)
    lines = l1 + l2
    ax1.legend(lines, [line.get_label() for line in lines], loc="upper left")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    if not monthly.empty:
        peak = monthly.loc[monthly["Sales"].idxmax(), "Year-Month"]
        takeaway(f"Sales are highest in {peak}. Check whether the profit line rises at the same time. A gap between the trends can indicate that revenue growth is not translating into profit.")

    st.divider()
    # Chart 3: Seaborn correlation heatmap
    st.markdown("#### Chart 3 — Correlation Heatmap")
    corr = filtered_df[["Sales", "Quantity", "Discount", "Profit"]].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, center=0, fmt=".2f", linewidths=.5, ax=ax)
    ax.set_title("Correlation: Sales, Quantity, Discount and Profit")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    discount_profit_corr = corr.loc["Discount", "Profit"]
    takeaway(f"The Discount–Profit correlation is {discount_profit_corr:.2f}. A negative value indicates that higher discounts are associated with lower profit in this selection; correlation alone does not prove causation.")

    st.divider()
    # Chart 4: Seaborn bar chart of total profit by Sub-Category
    st.markdown("#### Chart 4 — Total Profit / Loss by Sub-Category")
    subcat_profit = filtered_df.groupby("Sub-Category", as_index=False)["Profit"].sum().sort_values("Profit", ascending=True)
    fig, ax = plt.subplots(figsize=(9, 6))
    bar_colors = ["#B85C50" if value < 0 else "#557A5D" for value in subcat_profit["Profit"]]
    ax.barh(subcat_profit["Sub-Category"], subcat_profit["Profit"], color=bar_colors)
    ax.axvline(0, color="#647267", linewidth=1, linestyle="--")
    ax.set_title("Total Profit by Sub-Category")
    ax.set_xlabel("Total Profit ($)")
    ax.set_ylabel("Sub-Category")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    if not subcat_profit.empty:
        worst = subcat_profit.iloc[0]
        best = subcat_profit.iloc[-1]
        takeaway(f"{worst['Sub-Category']} has the lowest total profit ({money(worst['Profit'])}), while {best['Sub-Category']} has the highest ({money(best['Profit'])}) in the selected data.")

    st.divider()
    # Chart 5: interactive Plotly chart
    st.markdown("#### Chart 5 — Interactive Sales vs Profit Explorer")
    subcat = filtered_df.groupby(["Sub-Category", "Category"], as_index=False).agg(
        Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum")
    )
    fig = px.scatter(
        subcat, x="Sales", y="Profit", size="Quantity", color="Category",
        hover_name="Sub-Category", hover_data={"Sales": ":,.2f", "Profit": ":,.2f", "Quantity": True},
        title="Interactive Sub-Category Sales vs Profit", labels={"Sales": "Total Sales ($)", "Profit": "Total Profit ($)"},
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#B78A45", annotation_text="Break-even")
    fig.update_layout(
        paper_bgcolor="#FFFEFA", plot_bgcolor="#F7F4EC", font_color="#26352C",
        title_font_color="#244A38", xaxis=dict(gridcolor="#D7DED3"), yaxis=dict(gridcolor="#D7DED3"),
        legend_title_text="Category", margin=dict(l=20, r=20, t=60, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)
    negative_count = int((subcat["Profit"] < 0).sum())
    takeaway(f"{negative_count} sub-categories have negative total profit in the current selection. Hover over each point to compare sales, profit and quantity; points below break-even indicate losses.")

# =========================================================
# PAGE 6 — MANAGEMENT INSIGHTS (150–250 WORDS)
# =========================================================
elif st.session_state.app_page == "Management Insights":
    st.subheader("Management Recommendations")
    category_profit = filtered_df.groupby("Category")["Profit"].sum().sort_values()
    region_profit = filtered_df.groupby("Region")["Profit"].sum().sort_values()
    subcategory_profit = filtered_df.groupby("Sub-Category")["Profit"].sum().sort_values()
    monthly_sales = filtered_df.groupby("Year-Month")["Sales"].sum().sort_values(ascending=False)
    lowest_category, highest_category = category_profit.index[0], category_profit.index[-1]
    lowest_region = region_profit.index[0]
    worst_subcat, best_subcat = subcategory_profit.index[0], subcategory_profit.index[-1]
    peak_month = monthly_sales.index[0]
    discount_corr = filtered_df[["Discount", "Profit"]].corr().iloc[0, 1]

    recommendation = (
        f"The filtered results show that {lowest_category} is the lowest-profit category, while {highest_category} generates the highest total category profit. At sub-category level, {worst_subcat} has the lowest total profit and {best_subcat} has the highest. Management should review the transaction mix, selling prices, product costs and discount levels in the weaker areas before making broad changes.\n\n"
        f"The observed correlation between Discount and Profit is {discount_corr:.2f}. This describes an association in the selected records, not proof that discounting alone caused the profit outcome. The monthly summary identifies {peak_month} as the highest-sales month, which can help with demand planning. Compare this with the monthly profit chart to check whether the revenue peak also improves profit.\n\n"
        f"Two practical actions are recommended. First, audit low-profit products and region-category combinations, then test targeted discount limits or pricing changes and compare profit before and after the test. Second, use the monthly sales and profit pattern to plan inventory and staffing around stronger demand periods while monitoring slow months. Review the results regularly using sales, profit and profit margin together. The goal should be sustainable profitability, rather than sales growth alone."
    )
    st.markdown(recommendation)
    st.divider()
    st.subheader("Recommended Management Action Plan")
    st.markdown(
        """
        <div class="section-note">
            <strong>Priority 1 — Protect Profitability</strong><br>
            Review loss-making sub-categories and region-category combinations. Test pricing or discount adjustments on a small scale and compare the resulting profit before wider implementation.
        </div>
        <div class="section-note">
            <strong>Priority 2 — Plan Around Demand</strong><br>
            Use monthly sales and profit trends together to plan inventory and staffing. A sales peak should not automatically be treated as a profit peak.
        </div>
        <div class="section-note">
            <strong>Priority 3 — Monitor Measurable Outcomes</strong><br>
            Revisit Total Sales, Total Profit and Profit Margin after each change. Keep decisions evidence-based and avoid judging performance using revenue alone.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Analysis Note: All findings on this page reflect the current Region, Category, Customer Segment and Order Year filters. Change the filters to compare results across different selections.")

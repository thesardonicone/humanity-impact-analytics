
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="🌍 Global Human Impact Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# DARK MODE THEME (BLACK AESTHETIC)
# =====================================================
dark_mode_css = """
<style>
/* GLOBAL BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-color: #0e1117;
    color: #f0f0f0;
}

/* SIDEBAR STYLE */
[data-testid="stSidebar"] {
    background-color: #111418;
    border-right: 1px solid #222;
}

/* HEADINGS */
h1, h2, h3, h4, h5, h6 {
    color: #00b4d8 !important;
    font-weight: 700;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    background-color: #1b1e24 !important;
    color: #f0f0f0 !important;
}

/* TEXT INPUT & SELECTBOX */
.stSelectbox, .stTextInput, .stSlider {
    background-color: #1b1e24 !important;
    color: #f0f0f0 !important;
}

/* METRIC CARDS */
.metric-card {
    background-color: #1b1e24;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    border: 1px solid #333;
}
.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #00b4d8;
}
.metric-label {
    font-size: 14px;
    color: #bbb;
}
</style>
"""
st.markdown(dark_mode_css, unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:
    st.markdown("<h2 style='color:#00b4d8;text-align:center;'>🌐 Global Calamities</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray;'>Human Impact Intelligence Dashboard</p>", unsafe_allow_html=True)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Globe_icon.svg/2048px-Globe_icon.svg.png", width=90)
    st.markdown("---")

    dataset_option = st.selectbox(
        "📦 Select Dataset:",
        [
            "🦠 COVID-19 Pandemic Data",
            "🐖 H1N1 (Swine Flu) Data",
            "🌫️ Air Pollution (PM2.5)",
            "🚗 Road Accident Fatalities",
            "⚔️ Conflict & War Fatalities"
        ]
    )

    st.markdown("### 🔍 Filter Data")
    country_filter = st.text_input("🌍 Country or Region (optional)")

    st.markdown("---")
    st.caption("👤 Built by Vishwajeet | Dark Mode Edition 🖤")

# =====================================================
# LOAD CLEANED DATASETS
# =====================================================
datasets = {
    "🦠 COVID-19 Pandemic Data": "clean_covid-19 (1).csv",
    "🐖 H1N1 (Swine Flu) Data": "clean_h1n1_data.csv",
    "🌫️ Air Pollution (PM2.5)": "clean_pm25_air_pollution (1).csv",
    "🚗 Road Accident Fatalities": "clean_who_road_deaths (3).csv",
    "⚔️ Conflict & War Fatalities": "clean_conflict_fatalities (1).csv",
}

st.title(f"{dataset_option} 🌍 Analytics")

try:
    file_path = datasets[dataset_option]
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("⚠️ File not found. Please ensure all cleaned CSVs are in the app folder.")
    st.stop()

df.columns = [col.strip().title() for col in df.columns]

# Determine the country column name based on the dataset
country_col = None
if "Country/Region" in df.columns:
    country_col = "Country/Region"
elif "Country" in df.columns:
    country_col = "Country"

# =====================================================
# YEAR FILTER FIX (SAFE FOR SINGLE-YEAR DATASETS)
# =====================================================
# Check if 'Year' column exists before attempting to filter
if "Year" in df.columns:
    min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
    if min_year == max_year:
        st.sidebar.info(f"📅 Only {min_year} available.")
        year_filter = (min_year, max_year)
    else:
        year_filter = st.sidebar.slider("📆 Select Year Range", min_year, max_year, (min_year, max_year))
    df = df[(df["Year"] >= year_filter[0]) & (df["Year"] <= year_filter[1])]
else:
    st.sidebar.warning("No 'Year' column found in this dataset.")

# Apply country filter
if country_filter and country_col:
    df = df[df[country_col].str.contains(country_filter, case=False, na=False)]
elif country_filter and not country_col:
     st.sidebar.warning("No country/region column found in this dataset for filtering.")


# =====================================================
# MAIN CONTENT
# =====================================================
st.subheader(f"📊 Data Preview — {country_filter or 'All Countries'}")
st.dataframe(df.head(15))

# =====================================================
# METRICS SECTION
# =====================================================
numeric_cols = df.select_dtypes(include='number').columns.tolist()

if numeric_cols:
    st.markdown("### 💥 Key Global Metrics")
    metric_cols = st.columns(min(4, len(numeric_cols)))
    for i, col in enumerate(numeric_cols[:4]):
        val = df[col].sum()
        with metric_cols[i]:
            st.markdown(f"<div class='metric-card'><div class='metric-value'>{val:,.0f}</div><div class='metric-label'>{col}</div></div>", unsafe_allow_html=True)
else:
    st.warning("No numeric columns available to display metrics.")

# =====================================================
# VISUALIZATIONS
# =====================================================
if len(numeric_cols) > 0:
    st.markdown("### 📈 Trend Over Time")
    # Check if 'Year' column exists before attempting to plot
    if "Year" in df.columns:
        selected_metric = st.selectbox("Select Metric for Trend:", numeric_cols)
        fig_line = px.line(
            df,
            x="Year",
            y=selected_metric,
            color=country_col if country_col and country_col in df.columns else None,
            markers=True,
            template="plotly_dark",
            title=f"{selected_metric} Over Time",
        )
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Trend over time visualization requires a 'Year' column.")

    st.markdown("### 🏆 Top 10 Countries by Impact")
    top_metric = st.selectbox("Select Metric for Ranking:", numeric_cols, key="rank")
    if country_col and country_col in df.columns:
        top_data = df.groupby(country_col)[top_metric].sum().nlargest(10).reset_index()
        fig_bar = px.bar(
            top_data,
            x=country_col,
            y=top_metric,
            text_auto=True,
            color=country_col,
            template="plotly_dark",
            title=f"Top 10 Countries by {top_metric}",
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info(f"Top 10 countries visualization requires a country/region column like '{country_col}'.")


    st.markdown("### 🌍 Global Heatmap")
    map_metric = st.selectbox("Select Metric for Map:", numeric_cols, key="map")
    if country_col and country_col in df.columns:
        fig_map = px.choropleth(
            df,
            locations=country_col,
            locationmode="country names",
            color=map_metric,
            color_continuous_scale="Teal",
            template="plotly_dark",
            title=f"Global Distribution of {map_metric}",
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
         st.info(f"Global heatmap visualization requires a country/region column like '{country_col}'.")

# =====================================================
# FOOTER
# =====================================================
st.markdown("""
---
<center>
<p style='color:gray;font-size:14px;'>
🖤 <b>Global Human Impact Intelligence Dashboard</b><br>
Dark Theme | Powered by Data | Built with Streamlit ⚙️
</p>
</center>
""", unsafe_allow_html=True)

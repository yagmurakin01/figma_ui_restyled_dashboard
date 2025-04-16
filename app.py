
import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import BytesIO

# Sayfa ayarları
st.set_page_config(page_title="Figma UI Styled Dashboard", layout="wide")

# Tema seçimi
theme = st.sidebar.radio("🌙 Theme Mode", ["Dark", "Light"])
dark = theme == "Dark"

bg = "#1f1f2e" if dark else "#f5f6f8"
text = "#ffffff" if dark else "#000000"
card = "#2a2a3b" if dark else "#ffffff"
accent = "#8cc1f7" if dark else "#4f8df7"

# Stil
st.markdown(f"""
    <style>
    html, body, .stApp {{
        background-color: {bg};
        color: {text};
        font-family: 'Inter', sans-serif;
    }}
    h1, h2, h3, h4, h5, h6, p, label {{
        color: {text} !important;
    }}
    .card {{
        background-color: {card};
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }}
    .stButton>button {{
        background-color: {accent};
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }}
    .stFileUploader, .stRadio, .stSelectbox, .stMultiSelect {{
        padding: 1rem;
        background-color: {card};
        border-radius: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Figma UI Styled Dashboard")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = [c.strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].astype(str).str.replace("%", "").str.replace(",", ".")
        try:
            df[col] = pd.to_numeric(df[col])
        except:
            pass

    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("📌 Filters & Chart Type")
    x_axis = st.selectbox("X Axis", cat_cols)
    y_axis = st.selectbox("Y Axis", num_cols)
    filters = st.multiselect("Filter by X", df[x_axis].unique().tolist(), default=df[x_axis].unique().tolist())
    chart_type = st.radio("Chart Type", ["Bar", "Line", "Area", "Pie", "Scatter"], horizontal=True)
    st.markdown("</div>", unsafe_allow_html=True)

    filtered_df = df[df[x_axis].isin(filters)]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if chart_type == "Bar":
        fig = px.bar(filtered_df, x=x_axis, y=y_axis, text_auto=True)
    elif chart_type == "Line":
        fig = px.line(filtered_df, x=x_axis, y=y_axis)
    elif chart_type == "Area":
        fig = px.area(filtered_df, x=x_axis, y=y_axis)
    elif chart_type == "Pie":
        fig = px.pie(filtered_df, names=x_axis, values=y_axis)
    elif chart_type == "Scatter":
        fig = px.scatter(filtered_df, x=x_axis, y=y_axis, color=x_axis)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Export
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    buffer = BytesIO()
    fig.write_image(buffer, format="png")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{b64}" download="chart.png">📥 Download PNG</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Insight
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("🧠 Insight Summary")
    if not filtered_df.empty:
        max_val = filtered_df[y_axis].max()
        min_val = filtered_df[y_axis].min()
        avg_val = round(filtered_df[y_axis].mean(), 2)
        max_item = filtered_df[filtered_df[y_axis] == max_val][x_axis].values[0]
        min_item = filtered_df[filtered_df[y_axis] == min_val][x_axis].values[0]
        st.markdown(f"- **Max {y_axis}**: {max_val:.2f} ({max_item})")
        st.markdown(f"- **Min {y_axis}**: {min_val:.2f} ({min_item})")
        st.markdown(f"- **Average {y_axis}**: {avg_val}")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Please upload an Excel file to get started.")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Analytics Hub", layout="wide")
st.title("Intelligent Business Analytics")

# 1. The File Uploader
st.markdown("### Step 1: Upload Your Data")
uploaded_file = st.file_uploader("Drop your CSV or Excel file here", type=["csv", "xlsx"])

# 2. Process the Data
if uploaded_file is not None:
    # Check if it is a CSV or Excel file and read it
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("File uploaded successfully!")
    
    # Show a quick preview of the raw data
    with st.expander("View Raw Data Preview"):
        st.dataframe(df.head())

    # 3. Dynamic Chart Builder
    st.markdown("### Step 2: Analyze")
    col1, col2 = st.columns(2) # Create side-by-side dropdowns
    
    with col1:
        # Let the user pick any column from their uploaded file for the X-axis
        x_axis = st.selectbox("Select the X-Axis (e.g., Dates/Months):", df.columns)
    with col2:
        # Let the user pick any column for the Y-axis
        y_axis = st.selectbox("Select the Y-Axis (e.g., Revenue/Sales):", df.columns)

    # Draw the Chart instantly based on what they selected
    fig = px.line(df, x=x_axis, y=y_axis, markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 4. The AI Insights Engine
    st.markdown("### Step 3: AI Insights")
    st.info(f"**Analyzing {y_axis} trends...** \n\n*Note: This is ready for API integration. In a live environment, the exact data points for {y_axis} over {x_axis} would be securely sent to an LLM to automatically write a summary of performance and suggest business strategies.*")

else:
    # What the user sees before they upload a file
    st.info("👆 Please upload a spreadsheet to begin the analysis.")
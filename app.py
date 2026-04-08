import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

st.set_page_config(page_title="Business Analytics Hub", layout="wide")
st.title("Intelligent Business Analytics")
st.write(f"Is the API Key loaded? {'✅ Yes' if 'GEMINI_API_KEY' in st.secrets else '❌ No'}")

# 1. The File Uploader
st.markdown("### Step 1: Upload Your Data")
uploaded_file = st.file_uploader("Drop your CSV or Excel file here", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.success("File uploaded successfully!")
    
    with st.expander("View Raw Data Preview"):
        st.dataframe(df.head())

    # 2. Dynamic Chart Builder
    st.markdown("### Step 2: Analyze")
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox("Select the X-Axis (e.g., Dates/Months):", df.columns)
    with col2:
        y_axis = st.selectbox("Select the Y-Axis (e.g., Revenue/Sales):", df.columns)

    fig = px.line(df, x=x_axis, y=y_axis, markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 3. The Real AI Insights Engine
    st.markdown("### Step 3: AI Insights")
    
    # We create a button so the AI only runs when the user is ready
    if st.button("Generate AI Analysis"):
        with st.spinner("J.A.R.V.I.S. is analyzing the data trends..."):
            try:
                # Get the secret key we saved in Streamlit
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Turn a snapshot of the data into text for the AI to read
                data_summary = df[[x_axis, y_axis]].head(50).to_string(index=False)
                
                # Give the AI its instructions
                prompt = f"""
                You are a senior business analyst. I am looking at a chart of {y_axis} over {x_axis}. 
                Here is a sample of the data points:
                {data_summary}
                
                Please write a short, professional paragraph summarizing the trend. 
                Then, provide one highly actionable, strategic business recommendation based on this data.
                """
                
                # Send the prompt and print the response!
                response = model.generate_content(prompt)
                st.success("Analysis Complete:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Something went wrong connecting to the AI: {e}")

else:
    st.info("👆 Please upload a spreadsheet to begin the analysis.")

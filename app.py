import streamlit as st
import pandas as pd

st.set_page_config(page_title="Forecast CO₂ Chart", layout="centered")
st.title("📈 Forecasted CO₂ Emissions by Country")

# Upload the combined forecasted CSV
uploaded_file = st.file_uploader("Upload Combined Forecasted CSV", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Rename if necessary
        if 'predicted_co₂' in df.columns:
            df.rename(columns={'predicted_co₂': 'predicted_co2'}, inplace=True)

        # Ensure required columns exist
        required_cols = ['country', 'year', 'predicted_co2']
        if not all(col in df.columns for col in required_cols):
            st.error(f"Dataset must include: {', '.join(required_cols)}")
            st.stop()

        df['country'] = df['country'].str.upper()

        # Drop missing values just in case
        df.dropna(subset=['year', 'predicted_co2'], inplace=True)

        # Convert year to int if needed
        df['year'] = df['year'].astype(int)

        # Country selector
        selected_country = st.selectbox("Select Country", sorted(df['country'].unique()))
        country_data = df[df['country'] == selected_country]

        if country_data.empty:
            st.warning("No forecasted data found for the selected country.")
        else:
            st.subheader(f"🌍 CO₂ Emission Forecast for {selected_country}")
            st.line_chart(country_data.set_index('year')['predicted_co2'])

            # Optional: Display data table
            with st.expander("Show Forecast Data Table"):
                st.dataframe(country_data[['year', 'predicted_co2']].reset_index(drop=True))

    except Exception as e:
        st.error(f"Failed to process the file. Error: {e}")
else:
    st.info("Upload your CSV file containing forecasted CO₂ emissions.")

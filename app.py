import streamlit as st
import pandas as pd

st.set_page_config(page_title="Forecast Chart", layout="centered")
st.title("📈 Forecasted CO₂ Emission Over the Years")

# Upload the CSV that includes forecast_results
file = st.file_uploader("Upload forecast_results CSV", type=["csv"])

if file:
    try:
        df = pd.read_csv(file)
        df.columns = df.columns.str.strip().str.lower()

        # Rename if necessary
        if 'predicted_co₂' in df.columns:
            df.rename(columns={'predicted_co₂': 'predicted_co2'}, inplace=True)

        required_cols = ['country', 'year', 'predicted_co2']
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain: {', '.join(required_cols)}")
            st.write("Found columns:", df.columns.tolist())
            st.stop()

        df['country'] = df['country'].str.upper()
        selected_country = st.selectbox("Select Country", sorted(df['country'].unique()))

        # Filter data for selected country
        country_data = df[df['country'] == selected_country]

        if country_data.empty:
            st.warning(f"No forecasted data for {selected_country}")
        else:
            st.subheader(f"🌍 CO₂ Forecast for {selected_country}")
            st.line_chart(
                country_data.set_index('year')['predicted_co2']
            )

            # Optional: Show values in table
            with st.expander("📊 Forecast Table"):
                st.dataframe(country_data[['year', 'predicted_co2']].reset_index(drop=True))

    except Exception as e:
        st.error(f"Error reading CSV: {e}")
else:
    st.info("📌 Please upload the forecast CSV containing future year predictions.")

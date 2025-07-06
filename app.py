import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="CO₂ Forecast Dashboard", layout="centered")

st.title("🌍 CO₂ Emission Forecast per Country")

# Upload files
model_file = st.file_uploader("Upload trained model (.pkl)", type=["pkl"])
forecast_file = st.file_uploader("Upload forecasted CO₂ data (.csv)", type=["csv"])

if model_file and forecast_file:
    try:
        # Load model (optional use)
        model = joblib.load(model_file)

        # Load forecasted data
        forecast_df = pd.read_csv(forecast_file)
        forecast_df.columns = forecast_df.columns.str.strip().str.lower()  # Standardize

        required_columns = ['country', 'year', 'predicted_co2']
        if not all(col in forecast_df.columns for col in required_columns):
            st.error(f"Uploaded CSV must include these columns: {', '.join(required_columns)}")
            st.stop()

        # Format and select
        forecast_df['country'] = forecast_df['country'].str.upper()
        countries = sorted(forecast_df['country'].unique())
        selected_country = st.selectbox("Select Country", countries)

        country_data = forecast_df[forecast_df['country'] == selected_country]

        if country_data.empty:
            st.warning(f"No forecasted data available for {selected_country}")
        else:
            st.subheader(f"📈 Forecasted CO₂ Emissions for {selected_country}")
            st.line_chart(country_data.set_index('year')['predicted_co2'])

            # Optionally show raw table
            with st.expander("🔍 Show Forecasted Data"):
                st.dataframe(country_data[['year', 'predicted_co2']].reset_index(drop=True))

    except Exception as e:
        st.error(f"Something went wrong. Details:\n\n{e}")

else:
    st.info("Upload both a `.pkl` model and a forecasted `.csv` file to proceed.")

# Footer
st.markdown("---")
st.markdown("Developed using 🐍 Streamlit for Environmental Insights")

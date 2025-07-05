import streamlit as st
import pandas as pd
import joblib
import os

# Load the trained model
MODEL_PATH = "forecasting_co2_emmision.pkl"

st.title("🌍 CO₂ Emission Prediction by Country")

# Check for model
if not os.path.exists(MODEL_PATH):
    st.error("Model file not found. Please upload 'forecasting_co2_emmision.pkl'")
else:
    model = joblib.load(MODEL_PATH)

    # File upload
    uploaded_file = st.file_uploader("Upload Dataset (CSV containing country data)", type=['csv'])

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.write("📄 Uploaded Data Preview", data.head())

            # Dropdown for country selection
            country_list = data['country'].unique()
            selected_country = st.selectbox("Select a Country", country_list)

            # Filter the data for selected country
            country_data = data[data['country'] == selected_country]

            if country_data.empty:
                st.warning("⚠️ Selected country not found in dataset.")
            else:
                # Assuming only 1 row per country — or taking first match
                input_data = country_data[['country', 'gdp_per_cap', 'population', 'energy_use_per_cap']].iloc[0:1]

                if st.button("Predict CO₂ Emission"):
                    prediction = model.predict(input_data)[0]
                    st.success(f"🌿 Predicted CO₂ Emission for {selected_country}: {prediction:.2f} metric tons per capita")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")





   

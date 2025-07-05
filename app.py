import streamlit as st
import pandas as pd
import joblib
import os
import gdown

# Constants
FILE_ID = "1x-n9pUdVWZnL-_ZyE-pUrI2mrzv4xIRY"
MODEL_PATH = "forecasting_co2_emmision.pkl"

# Download the model if it doesn't exist
if not os.path.exists(MODEL_PATH):
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", MODEL_PATH, quiet=False)

# Load the trained model
model = joblib.load(MODEL_PATH)

# --- Streamlit UI ---
# Title
st.title("🌍 Carbon Emission Prediction per Country")

# Sidebar Inputs
st.sidebar.header("Enter Input Data")
country = st.sidebar.selectbox("Select Country", ['USA', 'IND', 'ARE', 'CHN', 'GBR'])
gdp = st.sidebar.number_input("GDP per Capita", min_value=0.0, step=100.0)
population = st.sidebar.number_input("Population (in millions)", min_value=0.0, step=1.0)
energy_use = st.sidebar.number_input("Energy Use per Capita", min_value=0.0, step=1.0)

# Create DataFrame for prediction
input_df = pd.DataFrame({
    'country': [country],
    'gdp_per_cap': [gdp],
    'population': [population],
    'energy_use_per_cap': [energy_use]
})

# Prediction
if st.sidebar.button("Predict CO₂ Emission"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"🌿 Predicted CO₂ Emission: {prediction:.2f} metric tons per capita")
    except Exception as e:
        st.error(f"Prediction failed: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

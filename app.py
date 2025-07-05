import streamlit as st
import pandas as pd
import joblib

# --- Upload Section ---
uploaded_file = st.sidebar.file_uploader("Upload Model File (.pkl)", type="pkl")

# If file is uploaded, save it and load the model
if uploaded_file is not None:
    with open("forecasting_co2_emmision.pkl", "wb") as f:
        f.write(uploaded_file.read())
    try:
        model = joblib.load("forecasting_co2_emmision.pkl")
        st.success("✅ Model uploaded and loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()
else:
    st.warning("⚠️ Please upload 'forecasting_co2_emmision.pkl' to continue.")
    st.stop()



# App title
st.title("Carbon Emission Prediction per Country")

# Sidebar - User input
st.sidebar.header("Enter Input Data")

# Input fields
country = st.sidebar.selectbox("Select Country", ['USA', 'IND', 'ARE', 'CHN', 'GBR'])
gdp = st.sidebar.number_input("GDP per Capita", min_value=0.0, step=100.0)
population = st.sidebar.number_input("Population (millions)", min_value=0.0, step=1.0)
energy_use = st.sidebar.number_input("Energy Use per Capita", min_value=0.0, step=1.0)

# Prepare input
input_df = pd.DataFrame({
    'country': [country],
    'gdp_per_cap': [gdp],
    'population': [population],
    'energy_use_per_cap': [energy_use]
})

# Predict
if st.sidebar.button("Predict CO₂ Emission"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted CO₂ Emission: {prediction:.2f} metric tons per capita")
    except Exception as e:
        st.error("Prediction failed. Please check your inputs or model compatibility.")

# Footer
st.markdown("---")
st.markdown("Made using Streamlit")




   

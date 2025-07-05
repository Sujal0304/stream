

import streamlit as st
import pandas as pd
import joblib

# Load trained model
... model = joblib.load('forecasting_co2_emmision.pkl')  # ensure this matches your actual model filename
... 
... # Page Title
... st.title("🌍 Carbon Emission Prediction per Country")
... 
... # Sidebar for input
... st.sidebar.header("Enter Input Data")
... 
... # Example input features - update as per your dataset features
... country = st.sidebar.selectbox("Select Country", ['USA', 'IND', 'ARE', 'CHN', 'GBR'])
... gdp = st.sidebar.number_input("GDP per Capita", min_value=0.0, step=100.0)
... population = st.sidebar.number_input("Population (millions)", min_value=0.0, step=1.0)
... energy_use = st.sidebar.number_input("Energy Use per Capita", min_value=0.0, step=1.0)
... 
... # Prepare input data
... input_df = pd.DataFrame({
...     'country': [country],
...     'gdp_per_cap': [gdp],
...     'population': [population],
...     'energy_use_per_cap': [energy_use]
... })
... 
... # Optionally, encode categorical if your model expects it (like LabelEncoder for 'country')
... # You may have to load encoder and transform input_df['country']
... 
... # Predict
... if st.sidebar.button("Predict CO₂ Emission"):
...     prediction = model.predict(input_df)[0]
...     st.success(f"🌿 Predicted CO₂ Emission: {prediction:.2f} metric tons per capita")
... 
... # Footer
... st.markdown("---")
... st.markdown("Made with ❤️ using Streamlit")

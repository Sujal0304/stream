


import streamlit as st
import pandas as pd
import joblib

# Page Title
st.title("🌍 Carbon Emission Prediction per Country")

# Upload the trained model
uploaded_model = st.file_uploader("Upload Trained Model (.pkl)", type="pkl")

if uploaded_model is not None:
    try:
        # Load the model
        model = joblib.load(uploaded_model)

        # Sidebar Input Form
        st.sidebar.header("Enter Input Data")
        country = st.sidebar.selectbox("Select Country", ['USA', 'IND', 'ARE', 'CHN', 'GBR'])
        gdp = st.sidebar.number_input("GDP per Capita", min_value=0.0, step=100.0)
        population = st.sidebar.number_input("Population (millions)", min_value=0.0, step=1.0)
        energy_use = st.sidebar.number_input("Energy Use per Capita", min_value=0.0, step=1.0)

        # Prepare input data
        input_df = pd.DataFrame({
            'country': [country],
            'gdp_per_cap': [gdp],
            'population': [population],
            'energy_use_per_cap': [energy_use]
        })

        # Predict button
        if st.sidebar.button("Predict CO₂ Emission"):
            prediction = model.predict(input_df)[0]
            st.success(f"🌿 Predicted CO₂ Emission: {prediction:.2f} metric tons per capita")

    except Exception as e:
        st.error("❌ Failed to load the model. Please upload a valid `.pkl` file.")
        st.exception(e)
else:
    st.info("📂 Please upload your trained `.pkl` model to begin predictions.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

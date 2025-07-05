
import streamlit as st
import pandas as pd
import joblib

st.title("🌍 Carbon Emission Prediction per Country")

# Upload model
model_file = st.sidebar.file_uploader("Upload Trained Model (.pkl)", type=["pkl"])
# Upload dataset
data_file = st.sidebar.file_uploader("Upload Dataset (CSV containing country data)", type=["csv"])

if model_file is not None and data_file is not None:
    try:
        # Load the model
        model = joblib.load(model_file)

        # Load the dataset
        df = pd.read_csv(data_file)

        # Dropdown for selecting country
        countries = df['country'].unique().tolist()
        selected_country = st.selectbox("Select Country", countries)

        # Get row for selected country
        input_row = df[df['country'] == selected_country]

        if input_row.empty:
            st.error("Selected country not found in dataset.")
        else:
            input_features = input_row[['country', 'gdp_per_cap', 'population', 'energy_use_per_cap']]

            # Make prediction
            try:
                prediction = model.predict(input_features)[0]
                st.success(f"🌿 Predicted CO₂ Emission for {selected_country}: {prediction:.2f} metric tons per capita")
            except Exception as e:
                st.error(f"Prediction failed. Please check your model and dataset. Error: {e}")

    except Exception as e:
        st.error(f"Error loading model or dataset. Details: {e}")

else:
    st.info("📤 Please upload both the model (.pkl) and dataset (.csv) to begin.")




   

import streamlit as st
import pandas as pd
import joblib

# Page Title
st.title("🌍 Carbon Emission Prediction per Country")

# Upload model
model_file = st.sidebar.file_uploader("Upload Trained Model (.pkl)", type=["pkl"])
# Upload dataset
data_file = st.sidebar.file_uploader("Upload Dataset (.csv)", type=["csv"])

# Once both files are uploaded
if model_file is not None and data_file is not None:
    try:
        model = joblib.load(model_file)
        df = pd.read_csv(data_file)

        # Normalize country names
        df['country'] = df['country'].str.upper()

        # Dropdown for countries
        selected_country = st.selectbox("Select a Country", sorted(df['country'].unique()))
        selected_country = selected_country.upper()

        # Find the matching row
        input_row = df[df['country'] == selected_country]

        if input_row.empty:
            st.error("Country data not found in the uploaded dataset.")
        else:
            try:
                # Extract only necessary features
                features = input_row[['gdp_per_cap', 'population', 'energy_use_per_cap']]
                prediction = model.predict(features)[0]
                st.success(f"🌿 Predicted CO₂ Emission for {selected_country}: **{prediction:.2f} metric tons per capita**")
            except Exception as e:
                st.error(f"Prediction failed. Please check your inputs or model compatibility.\n\nDetails: {e}")

    except Exception as e:
        st.error(f"Error loading model or dataset. Details: {e}")

else:
    st.info("Please upload both the model (.pkl) and dataset (.csv) to proceed.")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit")

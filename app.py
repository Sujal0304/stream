import streamlit as st
import pandas as pd
import joblib

# Page Title
st.title("🌍 Carbon Emission Prediction per Country")

# Upload the model
model_file = st.file_uploader("Upload the trained model (.pkl)", type=["pkl"])
data_file = st.file_uploader("Upload the dataset (.csv)", type=["csv"])

if model_file and data_file:
    try:
        # Load model
        model = joblib.load(model_file)

        # Load dataset
        df = pd.read_csv(data_file)

        # Normalize column names
        df.columns = df.columns.str.strip()

        # Rename to match model expectations
        df.rename(columns={
            'GDP per capita': 'gdp_per_cap',
            'Population (in millions)': 'population',
            'Energy use per capita': 'energy_use_per_cap'
        }, inplace=True)

        # Uppercase country for consistency
        df['country'] = df['country'].str.upper()

        # Country dropdown
        selected_country = st.selectbox("Select a Country", sorted(df['country'].unique()))
        selected_country = selected_country.upper()

        input_row = df[df['country'] == selected_country]

        if input_row.empty:
            st.error("Selected country data not found in the dataset.")
        else:
            try:
                features = input_row[['gdp_per_cap', 'population', 'energy_use_per_cap']]
                prediction = model.predict(features)[0]
                st.success(f"🌿 Predicted CO₂ Emission for {selected_country}: **{prediction:.2f} metric tons per capita**")
            except Exception as e:
                st.error(f"Prediction failed. Please check model compatibility.\n\nDetails: {e}")

    except Exception as e:
        st.error(f"Error loading model or dataset. Details: {e}")
else:
    st.info("👆 Please upload both the trained `.pkl` model and the dataset `.csv` to proceed.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")

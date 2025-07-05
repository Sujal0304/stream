import streamlit as st
import pandas as pd
import joblib

st.title("🌍 Carbon Emission Prediction per Country")

# Upload model and dataset
model_file = st.file_uploader("Upload your trained model (.pkl)", type=["pkl"])
data_file = st.file_uploader("Upload dataset (.csv)", type=["csv"])

if model_file and data_file:
    try:
        # Load model
        model = joblib.load(model_file)

        # Load dataset
        df = pd.read_csv(data_file)
        df.columns = df.columns.str.strip()

        # Create 'energy_use_per_cap' by copying 'en_per_cap'
        if 'en_per_cap' in df.columns:
            df['energy_use_per_cap'] = df['en_per_cap']
        else:
            st.error("Column 'en_per_cap' is missing in dataset.")
            st.stop()

        # Rename columns to match model's expected input
        rename_map = {
            'gni_per_cap': 'gdp_per_cap',
            'pop': 'population'
        }
        df.rename(columns=rename_map, inplace=True)

        expected_features = [
            'gdp_per_cap', 'population', 'energy_use_per_cap',
            'fdi_perc_gdp', 'en_per_cap', 'en_per_gdp', 'urb_pop_growth_perc'
        ]

        # Validate all required features
        missing = [f for f in expected_features if f not in df.columns]
        if missing:
            st.error(f"Dataset missing required columns: {', '.join(missing)}")
            st.stop()

        if 'country' not in df.columns:
            st.error("Dataset must contain a 'country' column.")
            st.stop()

        # Normalize country column
        df['country'] = df['country'].str.upper()
        selected_country = st.selectbox("Select Country", sorted(df['country'].unique()))

        input_row = df[df['country'] == selected_country]

        if input_row.empty:
            st.error("Selected country not found in dataset.")
        else:
            try:
                features = input_row[expected_features]
                prediction = model.predict(features)[0]
                st.success(f"🌿 Predicted CO₂ Emission for {selected_country}: **{prediction:.2f} metric tons per capita**")
            except Exception as e:
                st.error(f"Prediction failed. Please check model compatibility.\n\nDetails: {e}")

    except Exception as e:
        st.error(f"Error loading model or dataset.\n\nDetails: {e}")
else:
    st.info("Upload both the `.pkl` model and `.csv` dataset to proceed.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")


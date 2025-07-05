import streamlit as st
import pandas as pd
import joblib

st.title("🌍 Carbon Emission Forecast per Country")

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

        # Rename columns for model compatibility
        rename_map = {
            'gni_per_cap': 'gdp_per_cap',
            'pop': 'population',
            'en_per_cap': 'energy_use_per_cap'
        }
        df.rename(columns=rename_map, inplace=True)

        # Required features as per your model
        expected_features = [
            'gdp_per_cap', 'population', 'energy_use_per_cap',
            'fdi_perc_gdp', 'en_per_cap', 'en_per_gdp', 'urb_pop_growth_perc'
        ]

        # Validate presence of required columns
        if not all(feature in df.columns for feature in expected_features):
            missing = [f for f in expected_features if f not in df.columns]
            st.error(f"Dataset missing required columns: {', '.join(missing)}")
        elif 'country' not in df.columns or 'year' not in df.columns:
            st.error("Dataset must contain both 'country' and 'year' columns.")
        else:
            df['country'] = df['country'].str.upper()
            selected_country = st.selectbox("Select Country", sorted(df['country'].unique()))
            country_data = df[df['country'] == selected_country]

            if country_data.empty:
                st.error("Selected country not found in dataset.")
            else:
                # Predict for each year row of selected country
                features = country_data[expected_features]
                try:
                    predictions = model.predict(features)
                    country_data = country_data.copy()
                    country_data['Predicted_CO2'] = predictions

                    st.success(f"Predictions loaded for {selected_country}.")
                    
                    # Display table and chart
                    st.dataframe(country_data[['year', 'Predicted_CO2']].set_index('year'))
                    st.line_chart(country_data.set_index('year')['Predicted_CO2'])

                except Exception as e:
                    st.error(f"Prediction failed. Please check model compatibility.\n\nDetails: {e}")
    except Exception as e:
        st.error(f"Error loading model or dataset.\n\nDetails: {e}")
else:
    st.info("Upload both `.pkl` model and `.csv` dataset to proceed.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit")


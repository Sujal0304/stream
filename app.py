import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Carbon Emission Forecast", layout="centered")
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

        if 'country' not in df.columns or 'year' not in df.columns:
            st.error("Dataset must contain 'country' and 'year' columns.")
            st.stop()

        # Normalize country column
        df['country'] = df['country'].str.upper()
        selected_country = st.selectbox("Select Country", sorted(df['country'].unique()))

        input_data = df[df['country'] == selected_country]

        if input_data.empty:
            st.error("Selected country not found in dataset.")
        else:
            try:
                features = input_data[expected_features]
                predictions = model.predict(features)
                input_data['Predicted_CO2'] = predictions

                # Show latest prediction
                latest_pred = predictions[-1]
                st.success(f"🌿 Latest Predicted CO₂ Emission for {selected_country}: **{latest_pred:.2f} metric tons per capita**")

                # Forecast table with features
                st.subheader(f"📊 Predicted CO₂ Emissions & Features for {selected_country}")
                st.dataframe(
                    input_data[['year', 'gdp_per_cap', 'population', 'energy_use_per_cap',
                                'fdi_perc_gdp', 'en_per_cap', 'en_per_gdp', 'urb_pop_growth_perc', 'Predicted_CO2']]
                    .sort_values(by='year')
                    .rename(columns={'Predicted_CO2': 'CO₂ Emission Prediction (metric tons)'})
                )

                # Line chart of emissions
                st.subheader("📈 CO₂ Emission Forecast Over Years")
                st.line_chart(input_data.set_index('year')['Predicted_CO2'])

                # Insight
                change = predictions[-1] - predictions[0]
                trend = "increased 📈" if change > 0 else "decreased 📉"
                st.markdown(
                    f"**Insight**: Between {input_data['year'].min()} and {input_data['year'].max()}, "
                    f"CO₂ emissions for **{selected_country}** have {trend} by **{abs(change):.2f} metric tons per capita**."
                )

                st.subheader("📈 CO₂ Emission Forecast for Upcoming Years")
                if 'year' in input_data.columns:
                    last_year = input_data['year'].max()
                    future_years = list(range(last_year + 1, last_year + 6))  # e.g., 5 years ahead
                
                    # Use latest known values to forecast (simplified)
                    last_known = input_data.iloc[-1]  # last row
                    future_data = pd.DataFrame([last_known[expected_features]] * len(future_years))
                    future_data['year'] = future_years

                try:
                    future_preds = model.predict(future_data[expected_features])
                    forecast_df = pd.DataFrame({
                        'year': future_years,
                        'Predicted_CO2': future_preds
                    })
            
                    st.line_chart(forecast_df.set_index('year'))
                except Exception as e:
                    st.error(f"Future forecasting failed. Error: {e}")
                        
            except Exception as e:
                    st.error(f"Prediction failed. Please check model compatibility.\n\nDetails: {e}")

    except Exception as e:
        st.error(f"Error loading model or dataset.\n\nDetails: {e}")
else:
    st.info("Upload both the `.pkl` model and `.csv` dataset to proceed.")

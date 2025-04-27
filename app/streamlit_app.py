import streamlit as st
import pandas as pd
import os
import ast
import math

# ======= Recommender function (inside same file) =======
def recommend_best_store(filtered_data, search_query):
    """
    Recommend the best store based on the filtered GPU data and search query.
    """
    filtered_gpus = filtered_data[filtered_data['title'].str.contains(search_query, case=False)]
    
    if not filtered_gpus.empty:
        best_gpu = filtered_gpus.loc[filtered_gpus['price'].idxmin()]
        return best_gpu.to_dict()
    else:
        return {}

# ======= Load Cleaned Data =======
def load_cleaned_data():
    cleaned_file_path = os.path.join('..', 'data', 'cleaned', 'merged_data.csv')
    return pd.read_csv(cleaned_file_path)

# Load data once
data = load_cleaned_data()

# ======= Streamlit App =======
st.title("🛒 Quick Market Finder")

# Placeholder for showing/hiding table
data_placeholder = st.empty()

# --- Show/Hide Data Buttons ---
if st.button("Show Data"):
    with data_placeholder.container():
        st.subheader("📋 Cleaned GPU Data Table")
        st.write(data)
        if st.button("Hide Data"):
            data_placeholder.empty()

# --- Search GPU ---
search_query = st.text_input("🔍 Search for a GPU (e.g., RTX 4060)")

# Filtered Data
if search_query:
    filtered_data = data[data['title'].str.contains(search_query, case=False)]
else:
    filtered_data = data

# Recommend Best Store Button (comes after search bar, before cards)
recommendation = None
if st.button("Recommend Best Store"):
    recommendation = recommend_best_store(filtered_data, search_query)

# --- Helper function to check NaN or empty model ---
def is_valid_model(model_value):
    return isinstance(model_value, str) and model_value != 'Model not found' and model_value.strip() != '' and not pd.isna(model_value)

# --- Show Best Recommendation (Card) ---
if recommendation:
    st.subheader("🏆 Best Recommendation:")

    recommended_card = f"""
    <div style="padding: 10px; border: 2px solid #4CAF50; border-radius: 10px; text-align: center; margin-top: 20px;">
        <h2>{recommendation['title']}</h2>
    """

    if recommendation['price'] != 0.0:
        recommended_card += f"<p><strong>Price:</strong> {recommendation['price']}</p>"

    if is_valid_model(recommendation['model']):
        recommended_card += f"<p><strong>Model:</strong> {recommendation['model']}</p>"

    recommended_card += f"<p><strong>Store:</strong> {recommendation['store']}</p>"

    # Handle Features properly
    features_html = ""
    if isinstance(recommendation['features'], str):
        try:
            features_list = ast.literal_eval(recommendation['features'])
            if isinstance(features_list, list) and len(features_list) > 0:
                features_html += "<p><strong>Features:</strong></p><ul>"
                for feature in features_list:
                    features_html += f"<li>{feature}</li>"
                features_html += "</ul>"
        except Exception as e:
            st.warning(f"Error parsing features for recommendation: {e}")

    recommended_card += features_html
    recommended_card += "</div>"

    st.markdown(recommended_card, unsafe_allow_html=True)

# --- Show GPUs ---
if not filtered_data.empty:
    st.subheader("🖥️ Available GPUs")
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in filtered_data.iterrows():
        card = f"""
        <div style="padding: 10px; border: 1px solid #ddd; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h3>{row['title']}</h3>
        """

        if row['price'] != 0.0:
            card += f"<p><strong>Price:</strong> {row['price']}</p>"

        if is_valid_model(row['model']):
            card += f"<p><strong>Model:</strong> {row['model']}</p>"

        card += f"<p><strong>Store:</strong> {row['store']}</p>"

        # Handle Features properly
        features_html = ""
        if isinstance(row['features'], str):
            try:
                features_list = ast.literal_eval(row['features'])
                if isinstance(features_list, list) and len(features_list) > 0:
                    features_html += "<p><strong>Features:</strong></p><ul>"
                    for feature in features_list:
                        features_html += f"<li>{feature}</li>"
                    features_html += "</ul>"
            except Exception as e:
                st.warning(f"Error parsing features for {row['title']}: {e}")

        card += features_html
        card += "</div>"

        columns[idx % num_columns].markdown(card, unsafe_allow_html=True)
else:
    st.info("No GPUs match your search. Showing all products.")

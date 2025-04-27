# import pandas as pd

# def load_cleaned_data(file_path):
#     """Load the cleaned GPU data."""
#     return pd.read_csv(file_path)

# # In recommender.py

# def recommend_best_store(filtereddata, query):
#     """
#     Recommend the best store based on the filtered GPU data and search query.
#     """
#     # Filter the data based on the search query
#     filtered_gpus = filtereddata[filtereddata['title'].str.contains(query, case=False)]
    
#     # Check if there are any matching GPUs
#     if not filtered_gpus.empty:
#         # Find the GPU with the lowest price from the filtered data
#         best_gpu = filtered_gpus.loc[filtered_gpus['price'].idxmin()]
        
#         # Return the recommended GPU as a dictionary (JSON format)
#         return best_gpu.to_dict()
#     else:
#         # If no products found, return an empty dictionary
#         return {}

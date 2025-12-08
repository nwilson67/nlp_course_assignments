import pandas as pd

# Load the CSV
df = pd.read_csv("news_category_data.csv", encoding="latin-1")  # adjust encoding if needed

# Get all unique values in the 'category' column
unique_categories = df['category'].unique()

# Convert to a list and print
unique_categories_list = list(unique_categories)
print("All unique categories:", unique_categories_list)

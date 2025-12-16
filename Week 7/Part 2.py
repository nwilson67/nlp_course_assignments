import pandas as pd
import time
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY not found in environment variables!")

client = genai.Client(api_key=google_api_key)

# Load news dataset
df_news = pd.read_csv("news_category_data.csv", encoding="latin-1")

# Take 25 random rows
sample_news = df_news.sample(25, random_state=42)

# System prompt for news classification
system_prompt_news = """
You are a news category classifier. 
Given a headline, return ONLY one label corresponding to the category.
Do NOT explain your reasoning.
All unique categories: ['WELLNESS', 'ARTS, CULTURE, & ENTERTAINMENT', 'TRAVEL', 'POLITICS', 'FOOD & DRINK', 'STYLE & BEAUTY', 'RELIGION', 'WEDDINGS', 'INTERNATIONAL NEWS', 'EDUCATION', 'PARENTING', 'SCIENCE', 'SPORTS', 'DIVORCE', 'ENVIRONMENT', 'HOME & LIVING', 'QUEER VOICES', 'TECH']
Example:

Headline: "New study shows health benefits of walking"
Category: Wellness
"""

# Function to classify one headline
def classify_news(headline):
    user_query = f"Headline: \"{headline}\"\nCategory:"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt_news
        ),
        contents=user_query
    )

    # Extract token usage from response.usage_metadata
    usage = response.usage_metadata

    input_tokens = getattr(usage, "prompt_token_count", 0)
    output_tokens = getattr(usage, "candidates_token_count", 0)

    print(f"Total tokens: {usage}")

    return response.text.strip(), input_tokens, output_tokens

# Classify all 25 headlines
results_news = []
categories = []

total_in = 0
total_out = 0

for i, row in sample_news.iterrows():
    headline = row["headline"]
    true_category = row["category"]

    predicted, in_tok, out_tok = classify_news(headline)

    total_in += in_tok
    total_out += out_tok

    results_news.append((headline, predicted))
    categories.append((true_category, predicted))

    print(f"Headline: {headline}\nPredicted: {predicted}\n")

    # Rate limit safety (10 requests/min)
    time.sleep(6)

# Compute accuracy
correct_news = sum(
    1 for true_label, pred_label in categories
    if str(true_label).strip().lower() == str(pred_label).strip().lower()
)

accuracy_news = correct_news / len(sample_news)

# Print summary
print("==============================")
print(f"Accuracy on 25 news headlines: {accuracy_news:.2f}")
print(f"Total Input Tokens: {total_in}")
print(f"Total Output Tokens: {total_out}")
print("==============================")

# Save predictions
output_news_df = sample_news.copy()
output_news_df["llm_predicted"] = [pred for _, pred in categories]
output_news_df.to_csv("news_results.csv", index=False)

import pandas as pd
import random
from google import genai
from dotenv import load_dotenv
import os
import time

# ----------------------------
# Load API key and create client
# ----------------------------
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY not found in environment variables!")

client = genai.Client(api_key=google_api_key)

# ----------------------------
# Load the dataset
# ----------------------------
df = pd.read_csv("train.csv", encoding="latin-1")  # adjust encoding if needed

# Sample 25 rows
sample_df = df.sample(25, random_state=42)

# ----------------------------
# System prompt with few-shot examples
# ----------------------------
system_prompt = """
You are a sentiment analysis classifier. 
Given a piece of text, return ONLY one label: positive, negative, or neutral.
Do NOT explain your reasoning.

Examples:
Text: "I love this!"
Label: positive

Text: "This is terrible."
Label: negative

Text: "It was okay, nothing special."
Label: neutral
"""

# ----------------------------
# Function to classify one sentence and return token usage
# ----------------------------
def classify_sentiment(text):
    user_query = f"Text: \"{text}\"\nLabel:"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt
        ),
        contents=user_query
    )
    print(f"Total tokens {response.usage_metadata}")
    input_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
    output_tokens = getattr(response.usage_metadata, "thoughts_token_count", 0)

    return response.text.strip().lower(), input_tokens, output_tokens

# ----------------------------
# Classify all 25 rows
# ----------------------------
results = []
sentiments = []

total_input_tokens = 0
total_output_tokens = 0

for i, row in sample_df.iterrows():
    sentence = row["text"]
    sentiment = row["sentiment"]

    label, input_tokens, output_tokens = classify_sentiment(sentence)
    total_input_tokens += input_tokens
    total_output_tokens += output_tokens

    results.append((sentence, label))
    sentiments.append((sentiment, label))

    print(f"Sentence: {sentence}\nPredicted: {label}\n")


    # Rate limit safety (10 requests/min for 2.5 Flash)
    time.sleep(6)

# ----------------------------
# Compute accuracy
# ----------------------------
correct = sum(
    1 for true_label, predicted_label in sentiments
    if str(true_label).strip().lower() == str(predicted_label).strip().lower()
)
accuracy = correct / len(sample_df)

# ----------------------------
# Print summary
# ----------------------------
print("==============================")
print(f"Accuracy on 25 samples: {accuracy:.2f}")
print(f"Total Input Tokens: {total_input_tokens}")
print(f"Total Output Tokens: {total_output_tokens}")
print("==============================")

# I also saved the results to a CSV.
output_df = sample_df.copy()
output_df["llm_predicted"] = [pred for _, pred in sentiments]
output_df.to_csv("sentiment_results.csv", index=False)

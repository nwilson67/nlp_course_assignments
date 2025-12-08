import pandas as pd

def create_embedding(chunk):
    #create an array of embeddings per chunk and then pickle dump into vector_store.pkl
    return chunk
def main():
    filename = "C:\\Users\\Nathan\\Desktop\\Classwork\\DSAI 6810\\Project\\pokemon_docs.csv"

    #Load the file into a Pandas DataFrame
    df = pd.read_csv(filename)

    #Accessing the body of the first document
    print("\n--- First Document Body ---")
    print(df.iloc[0]['body'])

    # Assuming 'df' is the dataframe we created in the previous step

    # iterrows() gives you the index and the row content
    for index, row in df.iterrows():
        print(f"--- Processing Document #{row['doc_id']} ---")
        print(f"Title: {row['title']}")

        # You can access specific columns just like a dictionary
        content = row['body']

        # Example: Print the first 100 characters of the body

        # --- FOR YOUR PROJECT ---
        # This is where you would usually put your RAG logic.
        # For example:
        # embedding = create_embedding(row['body'])
        # database.add(id=row['doc_id'], vector=embedding)
        print(create_embedding(row['body']))
main()

import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

df = pd.read_csv("matches.csv")

print("Dataset loaded successfully")
print(df.head())


def convert_to_sentence(row):
    return (
        f"{row['team1']} vs {row['team2']} "
        f"at {row['venue']} "
        f"on {row['date']}. "
        f"{row['winner']} won the match. "
        f"Player of match: {row['player_of_match']}."
    )


match_sentences = df.apply(convert_to_sentence, axis=1).tolist()

print("\nSample sentences:")
print(match_sentences[:2])

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Model loaded successfully")



print("\nGenerating embeddings...")

embeddings = model.encode(match_sentences)

print("Embeddings generated")



client = chromadb.Client()
collection = client.create_collection(name="cricket_matches")



for i in range(len(match_sentences)):
    collection.add(
        ids=[str(i)],
        documents=[match_sentences[i]],
        embeddings=[embeddings[i]]
    )

print("\nData stored in ChromaDB")


import joblib
import numpy as np
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# Load Embeddings
# ============================================================

df = joblib.load("embeddings.joblib")

# ============================================================
# Embedding Function
# ============================================================

def create_embedding(text):

    response = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": [text]
        }
    )

    response.raise_for_status()
    return response.json()["embeddings"][0]


# ============================================================
# Evaluation Dataset
# IMPORTANT:
# Replace titles with EXACT names from your dataframe.
# ============================================================

test_questions = [

    {
        "question": "What is Pandas?",
        "expected_videos": [
            "Introduction To Pandas Module",
            "Creating Our First Pandas DataFrame",
            "Reading A CSV File In Python Pandas"
        ]
    },

    {
        "question": "How do you create a DataFrame?",
        "expected_videos": [
            "Creating Our First Pandas DataFrame",
            "Slicing And Adding Columns To A DataFrame"
        ]
    },

    {
        "question": "How do you read a CSV file?",
        "expected_videos": [
            "Reading A CSV File In Python Pandas"
        ]
    },

    {
        "question": "What is NumPy?",
        "expected_videos": [
            "Numpy Python Tutorial For Beginners- Python Data Science and Big Data Tutorials In Hindi Part-7.mp4",
            "Python Numpy Array Functions and Slicing-Python Data Science and Big Data Tutorials in Hindi Part-9.mp4"
        ]
    },

    {
        "question": "How do you slice a DataFrame?",
        "expected_videos": [
            "Slicing And Adding Columns To A DataFrame"
        ]
    }

]

# ============================================================
# Evaluation
# ============================================================

K = 5

results = []

print("\n")
print("=" * 90)
print("RAG RETRIEVAL EVALUATION")
print("=" * 90)

for sample in test_questions:

    query_embedding = create_embedding(sample["question"])

    similarities = cosine_similarity(
        np.vstack(df["embedding"]),
        [query_embedding]
    ).flatten()

    top_indices = similarities.argsort()[::-1][:K]

    retrieved_titles = df.iloc[top_indices]["title"].tolist()

    # Remove duplicates while preserving order
    retrieved_titles = list(dict.fromkeys(retrieved_titles))

    expected_titles = set(sample["expected_videos"])

    hits = [video for video in retrieved_titles if video in expected_titles]

    missed = list(expected_titles - set(hits))

    precision = len(hits) / len(retrieved_titles)

    results.append({
        "Question": sample["question"],
        "Precision": round(precision, 2)
    })

    print("\n" + "-" * 90)

    print(f"Question:\n{sample['question']}\n")

    print("Expected Videos:")
    for v in sample["expected_videos"]:
        print(f"  • {v}")

    print("\nRetrieved Videos:")
    for i, v in enumerate(retrieved_titles, start=1):
        marker = "✅" if v in hits else "❌"
        print(f"  {i}. {marker} {v}")

    print(f"\nRelevant Retrieved : {len(hits)}")
    print(f"Unique Retrieved   : {len(retrieved_titles)}")
    print(f"Precision          : {precision:.2f}")

    if missed:
        print("\nMissed Relevant Videos:")
        for v in missed:
            print(f"  • {v}")

# ============================================================
# Final Summary
# ============================================================

summary = pd.DataFrame(results)

average_precision = summary["Precision"].mean()

print("\n")
print("=" * 90)
print("SUMMARY")
print("=" * 90)

print(summary.to_string(index=False))

print("\n" + "=" * 90)
print(f"Average Precision            : {average_precision:.2f}")
print(f"Average Retrieval Accuracy   : {average_precision*100:.1f}%")
print("=" * 90)
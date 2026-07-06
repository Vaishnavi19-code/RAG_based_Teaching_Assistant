import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

# Load embeddings only once
df = joblib.load("embeddings.joblib")


def create_embedding(text_list):
    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "bge-m3",
            "input": text_list
        }
    )

    return r.json()["embeddings"][0]


def inference(prompt):
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()["response"]


def ask_question(incoming_query, selected_video="All Videos", chat_history=None):

    # -----------------------------
    # Generate query embedding
    # -----------------------------
    question_embedding = create_embedding([incoming_query])

    # Metadata filtering

    search_df = df

    if selected_video != "All Videos":
        search_df = df[df["title"] == selected_video]

    # -----------------------------
    # Cosine similarity search
    # -----------------------------
    similarities = cosine_similarity(
    np.vstack(search_df["embedding"]),
    [question_embedding]
    ).flatten()

    top_results = 5

    max_indx = similarities.argsort()[::-1][:top_results]

    new_df = search_df.iloc[max_indx]

    print("\n========== Retrieved Chunks ==========\n")

    for i, (_, row) in enumerate(new_df.iterrows(), 1):
        print(f"Rank {i}")
        print(f"Video     : {row['title']}")
        print(f"Timestamp : {row['start']} - {row['end']}")
        print(f"Transcript: {row['text']}")
        print("-" * 60)

    # -----------------------------
    # Build readable context
    # -----------------------------
    context = ""

    for _, row in new_df.iterrows():

        context += f"""
    Video Title : {row['title']}
    Video Number: {row['number']}
    Timestamp   : {row['start']} - {row['end']} sec
    Transcript  :
    {row['text']}

----------------------------------------

"""
    # -----------------------------
    # Build Conversation History
    # -----------------------------

    history = ""

    if chat_history:
        # Only keep last 3 conversations
        last_messages = chat_history[-3:]

        for chat in last_messages:

            history += f"""
            User: {chat['question']}
            Assistant: {chat['answer']}
            """

    prompt = f"""
    You are an AI Teaching Assistant for the course "Big Data Analysis and Python for Data Science".
    Your goal is to help students quickly find where a topic is taught in the course.

    Previous Conversation:
    {history}
    ------------------------------------------------------------
    Retrieved Course Content:

    {context}
    ------------------------------------------------------------
    Student Question:
    {incoming_query}

    Instructions:

    1. Answer ONLY using the retrieved course content.
    2. Never mention words like "retrieved context", "transcript", "the transcript says", or "the student asked".
    3. Speak naturally like a friendly course instructor.
    4. If the topic appears in multiple videos, recommend ALL relevant videos in learning order.
    5. For every recommended video include:
    • Video Title
    • Video Number
    • Timestamp
    • What the student will learn there (1-2 sentences).
    6. If the exact answer is not available but related videos exist, recommend those videos instead of saying you don't know.
    7. Only if absolutely nothing relevant exists, reply:
    "I couldn't find this topic in the uploaded course videos."

    Keep the answer concise and practical.
    Format your answer exactly like this:
    ### Answer
    <Brief answer in 2-3 sentences>
    ### Recommended Videos

    📹 Video:
    Video Number:
    ⏱ Timestamp:
    📘 You'll learn:

    📹 Video:
    Video Number:
    ⏱ Timestamp:
    📘 You'll learn:
    """

    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    response = inference(prompt)

    with open("response.txt", "w", encoding="utf-8") as f:
        f.write(response)

    # -----------------------------
    # Return result
    # -----------------------------
    return {
        "answer": response,
        "video": new_df.iloc[0]["title"],
        "video_number": new_df.iloc[0]["number"],
        "timestamp": f"{new_df.iloc[0]['start']} - {new_df.iloc[0]['end']} sec",
        "retrieved_chunks": new_df
    }


# ----------------------------------------------------
# Run only if executed directly
# ----------------------------------------------------
if __name__ == "__main__":

    question = input("Ask a Question: ")

    result = ask_question(question)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nVideo:")
    print(result["video"])

    print("\nTimestamp:")
    print(result["timestamp"])
# 🎓 RAG-Based AI Teaching Assistant

An AI-powered Teaching Assistant that enables students to ask natural language questions about recorded course videos and receive accurate, context-aware answers along with the relevant video and timestamp.

Instead of manually searching through hours of lectures, students can simply ask a question, and the system retrieves the most relevant transcript segments before generating a grounded response using a Large Language Model (LLM).

---

## 🚀 Features

- 🎥 Converts lecture videos into searchable transcripts
- 🎙️ Speech-to-text transcription using Whisper Large-v2
- 🧠 Semantic retrieval using BGE-M3 embeddings
- 🔍 Cosine similarity-based document retrieval
- 🤖 Context-aware answer generation using Llama 3.2
- ⏱️ Returns relevant video name and timestamp
- 💻 Runs completely locally using Ollama
- ⚡ Average response time: ~2–3 seconds

---

## 🏗️ Project Architecture

```
                OFFLINE INDEXING

Course Videos
      │
      ▼
FFmpeg
(Audio Extraction)
      │
      ▼
Whisper Large-v2
(Speech-to-Text)
      │
      ▼
Timestamped Transcripts
      │
      ▼
BGE-M3 Embeddings
      │
      ▼
embeddings.joblib


                ONLINE INFERENCE

User Question
      │
      ▼
Query Embedding
      │
      ▼
Cosine Similarity Search
      │
      ▼
Top-5 Relevant Transcript Segments
      │
      ▼
Prompt Construction
      │
      ▼
Llama 3.2 (Ollama)
      │
      ▼
Answer + Video + Timestamp
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming | Python |
| Speech-to-Text | Whisper Large-v2 |
| Audio Processing | FFmpeg |
| Embedding Model | BGE-M3 |
| LLM | Llama 3.2 |
| LLM Runtime | Ollama |
| Retrieval | Cosine Similarity |
| Storage | Joblib, Pandas |
| Libraries | NumPy, Pandas, Scikit-learn, Requests |

---

## 📂 Project Workflow

### 1. Video Processing

- Extract audio from lecture videos using FFmpeg.
- Convert speech into timestamped transcripts using Whisper.

### 2. Embedding Generation

- Generate semantic embeddings for each transcript segment using BGE-M3.
- Store embeddings with transcript metadata in `embeddings.joblib`.

### 3. User Query

- Convert the user's question into an embedding.
- Perform cosine similarity search.
- Retrieve the Top-5 most relevant transcript segments.

### 4. Response Generation

- Build a structured prompt using retrieved context.
- Generate the final answer using Llama 3.2 through Ollama.
- Return the answer along with the relevant video and timestamp.


## 📈 Results

- Processed **14 educational videos**
- Generated timestamped transcripts
- Semantic retrieval using **BGE-M3**
- Grounded responses using **Llama 3.2**
- Average response time **10 seconds**
- Improved learning experience by directing students to the exact lecture timestamp

---

## 🚧 Current Limitations

- Retrieval performs linear cosine similarity search.
- Embeddings are stored using Joblib instead of a dedicated vector database.
- Optimized for a single course.
- No conversation history.

---

## 🔮 Future Improvements

- Integrate FAISS/ChromaDB/Pinecone for scalable retrieval
- Hybrid Search (Keyword + Semantic)
- Reranking
- Conversation Memory
- Multi-course Support
- Streamlit Web Interface
- Retrieval Confidence Score
- RAG Evaluation Metrics

---

## 💡 Key Learnings

- Built a custom Retrieval-Augmented Generation (RAG) pipeline from scratch.
- Learned semantic retrieval using embeddings and cosine similarity.
- Understood prompt engineering for grounded LLM responses.
- Improved answer quality by reducing retrieved chunks from **30** to **5**, resulting in lower latency and more focused responses.

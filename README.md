# 🎓 RAG-Based AI Teaching Assistant

An end-to-end **Retrieval-Augmented Generation (RAG)** application that enables students to ask natural language questions about recorded course lectures and receive grounded answers with the corresponding **video title** and **timestamp**.

Instead of manually searching through hours of recorded lectures, students can simply ask a question, and the assistant retrieves the most relevant lecture content before generating a context-aware response.

---

# 🚀 Features

- 🎥 Converts lecture videos into searchable knowledge
- 🎙️ Speech-to-text transcription using Whisper
- 🧠 Semantic embeddings using BGE-M3
- 🔍 Cosine similarity-based semantic retrieval
- 🤖 Local LLM inference using Llama 3.2 via Ollama
- 💬 Streamlit chat interface
- 🧾 Conversation memory
- 🎯 Metadata-based video filtering
- ⏱️ Timestamp-aware answers
- 📊 Retrieval evaluation using Precision-based benchmark

---

# 🏗️ System Architecture

```
                    OFFLINE PIPELINE

Lecture Videos
      │
      ▼
   FFmpeg
      │
      ▼
 Whisper
      │
      ▼
Timestamped Transcript Chunks
      │
      ▼
 BGE-M3 Embeddings
      │
      ▼
embeddings.joblib


                    ONLINE PIPELINE

Student Question
        │
        ▼
Conversation Memory
        │
        ▼
Metadata Filter (Optional)
        │
        ▼
Question Embedding
        │
        ▼
Cosine Similarity Search
        │
        ▼
Top-5 Relevant Chunks
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

# 📂 Project Structure

```
RAG/

│── app.py                     # Streamlit application
│── process_incoming.py        # Online RAG pipeline
│── create_embeddings.py       # Offline embedding generation
│── evaluation.py             # Retrieval evaluation
│── embeddings.joblib         # Stored transcript embeddings
│── requirements.txt
│── README.md

│
├── videos/
│      Original lecture videos
│
├── audios/
│      Extracted audio files
│
├── jsons/
│      Whisper generated transcript chunks
│
└── images/
       Architecture diagrams and screenshots
```

---

# ⚙️ Tech Stack

### Programming

- Python

### AI / Machine Learning

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Semantic Search

### Libraries

- Whisper
- Ollama
- BGE-M3
- Llama 3.2
- Pandas
- Joblib
- NumPy
- Streamlit

---

# 🔄 Workflow

## Offline Pipeline

1. Lecture videos are converted to audio using FFmpeg.
2. Whisper generates timestamped transcripts.
3. Transcript chunks are embedded using BGE-M3.
4. Embeddings are stored inside `embeddings.joblib`.

---

## Online Pipeline

1. Student asks a question.
2. Question is embedded using BGE-M3.
3. Optional metadata filtering narrows the search space.
4. Cosine similarity retrieves the Top-5 relevant transcript chunks.
5. Retrieved context is combined with conversation history.
6. Llama 3.2 generates a grounded response.
7. Student receives the answer along with the relevant lecture and timestamp.

---

# 📊 Evaluation

The retrieval component was evaluated using a manually curated benchmark consisting of representative student questions and expected lecture videos.

**Evaluation Metric**

- Precision-based Retrieval Evaluation

Current benchmark performance:

- **Average Retrieval Precision:** **~53%**

This benchmark provides an objective baseline for measuring future retrieval improvements instead of relying solely on manual testing.

---

# 💡 Challenges & Improvements

## Challenges

- Large transcript size
- Maintaining low latency
- Retrieval quality
- Hallucination prevention

## Improvements Implemented

- Reduced retrieval from Top-30 to Top-5 chunks
- Metadata-based filtering
- Conversation memory
- Improved prompt engineering
- Precision-based retrieval evaluation

---

# 🔮 Future Improvements

- FAISS / ChromaDB / Pinecone integration
- Hybrid Search (Embeddings + BM25)
- Retrieval reranking
- Confidence thresholding
- Larger evaluation benchmark
- Recall@K & MRR evaluation
- Multi-course support
- Analytics dashboard
- Multilingual support

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/RAG_based_Teaching_Assistant.git
```

Move into the project

```bash
cd RAG_based_Teaching_Assistant
```

Install dependencies

```bash
pip install -r requirements.txt
```

Start Ollama

```bash
ollama serve
```

Pull required models

```bash
ollama pull llama3.2
ollama pull bge-m3
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

# 📷 Demo

The assistant allows students to:

- Ask natural language questions
- Retrieve relevant lecture content
- View corresponding video timestamps
- Continue conversations using memory
- Filter responses by lecture

---

# 📚 Learning Outcomes

This project helped me gain practical experience with:

- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Semantic Search
- Embedding Models
- Local LLM Deployment
- Streamlit Deployment
- AI System Evaluation
- End-to-End AI Application Development

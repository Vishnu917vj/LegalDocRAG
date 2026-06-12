

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** Question & Answer API over a corpus of fictional legal-style documents.

### Tech Stack

- **Python**
- **FastAPI**
- **LangGraph**
- **Pinecone** (Vector Database)
- **Google Gemini 2.0 Flash** (LLM)
- **BAAI/bge-small-en-v1.5** (Embeddings)

The system ingests documents, stores vector embeddings in Pinecone, retrieves relevant chunks, performs relevance evaluation via a LangGraph workflow, and generates grounded answers with citations.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vishnu917vj/LegalDocRAG
cd LegalDocRAG
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory (reference `.env.example`):

```env
GEMINI_API_KEY=your_gemini_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=legal-rag
```

## Pinecone Setup

1. Create a free Pinecone account and generate an API key.
2. Create a new index with the following settings:

   - **Index Name**: `legal-rag`
   - **Dimension**: `384`
   - **Metric**: `cosine`

> **Important**: Pinecone may prompt you to select an embedding model (e.g., `llama-text-embed-v2`, `multilingual-e5-large`). **Ignore this** — embeddings are generated locally using `BAAI/bge-small-en-v1.5`. Only the dimension (384) matters.

## Ingestion

1. Place your documents (`.txt` or `.md`) in the `data/raw/` directory.
2. Run the ingestion script:

```bash
python -m scripts.ingest
```

The ingestion pipeline will:
- Load documents
- Split them into chunks
- Generate embeddings locally
- Store vectors + metadata in Pinecone

**Metadata stored per chunk:**
- `chunk_id`
- `source`
- `text`

### Re-Ingestion Safety

This project uses **deterministic chunk IDs** (e.g., `01_matter_memo_arvind_v_northfield.md_chunk_0`). Running the ingestion script multiple times is safe Pinecone will simply upsert (update) existing vectors without creating duplicates.

## Running the API

```bash
uvicorn app.main:app --reload
```

Open the interactive Swagger UI at:  
**http://localhost:8000/docs**

### API Endpoint: `POST /ask`

**Request:**
```json
{
  "question": "When was the written contract signed?"
}
```

**Response:**
```json
{
  "answer": "The written contract was signed on 12 January 2024.",
  "citations": [
    {
      "source": "01_matter_memo_arvind_v_northfield.md",
      "chunk_id": "01_matter_memo_arvind_v_northfield.md_chunk_0",
      "text": "The written contract was signed on 12 January 2024."
    }
  ]
}
```

**Example cURL:**

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\":\"When was the written contract signed?\"}"
```

## Evaluation Dataset

Since the assignment's optional sample test files were not provided, a custom evaluation dataset was created at:

**`eval/test_cases.json`**

It includes:
- Direct fact retrieval questions
- Paraphrased questions
- Out-of-corpus (adversarial) questions

This enables thorough testing of retrieval quality, grounding, citation accuracy, and hallucination prevention.

## Design Decisions and Justifications

### Why Google Gemini 2.0 Flash?

This project uses **Google Gemini 2.0 Flash** for both answer generation and retrieval evaluation.

**Reasons:**
- Free tier available through Google AI Studio
- Strong instruction-following capabilities, especially useful for retrieval validation tasks
- Fast inference speed suitable for real-time API responses
- Excellent Python SDK integration

Since the assignment focuses on building a robust retrieval and orchestration system rather than model training or fine-tuning, Gemini provides a practical, high-performance LLM option.

### Why BAAI/bge-small-en-v1.5?

Embeddings are generated using the open-source model:

**`BAAI/bge-small-en-v1.5`**

**Reasons:**
- Completely free and open-source
- Runs locally with **SentenceTransformers** (no paid embedding API required)
- Lightweight and efficient
- Produces 384-dimensional embeddings
- Strong performance on semantic similarity and retrieval tasks for legal-style documents

This choice eliminates embedding costs while maintaining a production-grade architecture.

### Pinecone Index Configuration

When creating the Pinecone index, you can ignore the suggested embedding models (e.g., `llama-text-embed-v2`, `multilingual-e5-large`, etc.), as embeddings are generated locally.

**Key Configuration:**
- **Index Name**: `legal-rag`
- **Dimension**: `384` (must match BAAI/bge-small-en-v1.5)
- **Metric**: `cosine`
- All other settings can remain at defaults

## Retrieval Validation and Relevance Checking

After retrieving candidate chunks from Pinecone, the system performs an additional relevance validation step before generating an answer.

### Why Not Use Similarity Scores Alone?

Pinecone retrieves chunks using vector similarity. While this is effective for finding semantically related content, a high similarity score does not necessarily mean the retrieved chunk contains the information required to answer the user's question.

For example:

**Question**

```text
Who is the CEO of Northfield Logistics?
```

**Retrieved Chunk**

```text
Northfield Logistics disputed the invoices.
```

The chunk may receive a high similarity score because both the question and chunk reference the same organization. However, the chunk clearly does not answer the question.

Therefore, relying solely on similarity scores can lead to incorrect answer generation.

### LLM-Based Relevance Evaluation

To improve answer grounding, the workflow performs an additional relevance evaluation step using Gemini Flash.

The LLM receives:

- The user's question
- The retrieved context

and determines whether the retrieved context is sufficient to answer the question.

The model is instructed to respond only with:

```text
YES
```

or

```text
NO
```

This creates a meaningful decision point within the LangGraph workflow and helps reduce hallucinations by preventing answer generation when supporting evidence is insufficient.

### Design Rationale

This approach was selected because:

- The assignment explicitly requires a retrieval evaluation stage with branching logic.
- Similarity search alone cannot determine answerability.
- Gemini Flash is available through a free tier and provides low-cost semantic evaluation.
- It improves grounding quality and reduces the likelihood of generating unsupported answers.

In a larger production system, this step could be replaced or supplemented with reranking models, hybrid search, metadata filtering, or confidence-based retrieval strategies.

---

## Retry Mechanism

The workflow includes a controlled retry mechanism to improve retrieval reliability and prevent premature failures.

### Workflow

```text
retrieve
   ↓
relevance_check
   ↓
YES ─────────► generate_answer
                  ↓
                 END

NO
 ↓
retry_retrieve
 ↓
retry_router
 ↓
retry_count >= MAX_RETRIES ?

NO ──────────► retrieve

YES ─────────► no_answer
                  ↓
                 END
```

### Retry Mechanism

To improve retrieval reliability, the workflow does not immediately return a failure response when the first retrieval attempt is not relevant.

Instead, it:

1. Increments a retry counter.
2. Expands the retrieval search space (`top_k`).
3. Slightly relaxes the similarity threshold.
4. Re-runs retrieval and relevance evaluation.

This process continues until:

- Relevant context is found, or
- The maximum retry limit is reached.

### Configuration

```python
MAX_RETRIES = 2

BASE_TOP_K = 2
BASE_MIN_SCORE = 0.60
```

Example retrieval behavior:

```text
Attempt 1 → top_k=2, min_score=0.60
Attempt 2 → top_k=4, min_score=0.50
Attempt 3 → top_k=6, min_score=0.50
```

### No Answer Response

If no sufficiently relevant context is found after all retry attempts, the workflow routes to the `no_answer` node and returns:

```text
I could not find the answer in the provided documents.
```

with an empty citations list.

### Notes

The retry count, retrieval depth (`top_k`), and similarity thresholds were chosen after basic experimentation on the provided sample corpus. Since the assignment corpus is relatively small, these settings provided a reasonable balance between retrieval quality, latency, and resource usage.

### Benefits

- Reduces the chance of missing relevant information.
- Improves retrieval coverage on difficult queries.
- Helps reduce hallucinations by requiring relevant supporting context.
- Demonstrates conditional routing and retry logic in LangGraph.
- Prevents infinite loops through a configurable retry limit.

### Citation Strategy

The assignment requires answers to be grounded with citations. However, legal information often spans multiple document chunks due to the chunking strategy.

**Approach:**
- Retrieve multiple top chunks from Pinecone
- Filter using similarity scores
- Perform LLM-based relevance validation
- Generate citations from **all** chunks used in the final answer

This multi-chunk citation strategy provides more accurate grounding than forcing a single-chunk attribution.

### Evaluation Dataset

The original assignment mentioned optional sample test files, but they were not included in the provided corpus. Therefore, a custom evaluation dataset was created at:

**`eval/test_cases.json`**

**Contains:**
- Direct fact lookup questions
- Paraphrased retrieval questions
- Out-of-corpus (adversarial) questions

This dataset enables comprehensive testing of retrieval quality, grounding accuracy, citation correctness, and hallucination resistance.


## Retry Mechanism

The LangGraph workflow includes a retry mechanism to avoid immediately failing when retrieved chunks are not relevant.

```text
retrieve
   ↓
relevance_check
   ↓
YES → generate_answer → END

NO
 ↓
retry_retrieve
 ↓
retry_router
 ↓
retrieve (until MAX_RETRIES reached)
 ↓
no_answer → END
```

If the retrieved context cannot answer the question, the system retries retrieval up to a configured limit:

```python
MAX_RETRIES = 2
```

Once the retry limit is reached, the workflow routes to the `no_answer` node and returns:

```text
I could not find the answer in the provided documents.
```

This prevents infinite loops while demonstrating conditional branching within the LangGraph workflow.

## Testing

Individual components of the system can be tested using the scripts available in the `scripts/` directory.

All test files follow the naming convention:

```text
test_*.py
```

Examples:

```bash
python -m scripts.test_embeddings
python -m scripts.test_pinecone
python -m scripts.test_retrieval
python -m scripts.test_chunking
python -m scripts.test_relevance
```

These scripts were used during development to verify embeddings, Pinecone connectivity, document chunking, retrieval quality, and relevance evaluation before integrating the complete LangGraph workflow.

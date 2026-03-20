# AI News Summarizer

A full-stack AI-powered news summarizer. Search any topic, get a structured summary of the latest news, and ask follow-up questions in a chat interface.

## Demo

1. Enter a topic (e.g. "AI breakthroughs", "climate change", "stock market")
2. Get an AI-generated summary with source links
3. Ask follow-up questions about the articles

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite, Tailwind CSS |
| Backend | FastAPI, Python |
| AI Agent | LangGraph, LangChain |
| LLM | OpenAI GPT-4o |
| Web Search | Tavily Search API |

---

## Architecture

```
User → React Frontend → FastAPI → LangGraph Agent
                                      ├── fetch_news  (Tavily)
                                      ├── summarize   (GPT-4o)
                                      └── qa          (GPT-4o + chat history)
```

See [`ai-news-summarizer/architecture.md`](./ai-news-summarizer/architecture.md) for the full diagram.

---

## Project Structure

```
ai-news-summarizer/
├── backend/
│   ├── main.py                  # FastAPI app + routes
│   ├── session_store.py         # In-memory session management
│   ├── agent/
│   │   ├── state.py             # AgentState TypedDict
│   │   ├── tools.py             # Tavily search wrapper
│   │   ├── nodes.py             # fetch_news, summarize, qa nodes
│   │   └── graph.py             # LangGraph StateGraph definitions
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── SearchBar.jsx    # Topic input
│   │   │   ├── NewsSummary.jsx  # Summary + source articles
│   │   │   └── ChatBox.jsx      # Follow-up Q&A chat
│   │   └── api/
│   │       └── newsApi.js       # Axios calls to FastAPI
│   └── package.json
└── architecture.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- [OpenAI API key](https://platform.openai.com/api-keys)
- [Tavily API key](https://app.tavily.com)

### 1. Backend

```bash
cd ai-news-summarizer/backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys:
#   OPENAI_API_KEY=sk-...
#   TAVILY_API_KEY=tvly-...

# Start the server
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd ai-news-summarizer/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at `http://localhost:5173`.

---

## API Endpoints

| Method | Endpoint | Body | Response |
|--------|----------|------|----------|
| `GET` | `/api/health` | — | `{ "status": "ok" }` |
| `POST` | `/api/summarize` | `{ "topic": "AI" }` | `{ "summary": "...", "articles": [...], "session_id": "uuid" }` |
| `POST` | `/api/followup` | `{ "question": "...", "session_id": "..." }` | `{ "answer": "..." }` |

### Example

```bash
# Summarize news on a topic
curl -X POST http://localhost:8000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"topic": "artificial intelligence"}'

# Ask a follow-up question
curl -X POST http://localhost:8000/api/followup \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the risks mentioned?", "session_id": "<uuid from above>"}'
```

---

## How It Works

### LangGraph Agent

Two compiled state graphs handle the two workflows:

**Summarize graph** (`POST /api/summarize`):
```
START → fetch_news (Tavily) → summarize (GPT-4o) → END
```

**Q&A graph** (`POST /api/followup`):
```
START → qa (GPT-4o + chat history) → END
```

### Session Management

After summarization, the full agent state (articles, summary, chat history) is stored in an in-memory dict keyed by a UUID `session_id`. Each follow-up question loads the session, runs the Q&A node, and saves the updated chat history back — enabling multi-turn conversations grounded in the original articles.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o |
| `TAVILY_API_KEY` | Tavily API key for web search |

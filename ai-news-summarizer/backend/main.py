from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from agent import summarize_graph, qa_graph
from session_store import create_session, get_session, update_session

app = FastAPI(title="AI News Summarizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    topic: str


class FollowupRequest(BaseModel):
    question: str
    session_id: str


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/summarize")
async def summarize_news(request: SummarizeRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")

    initial_state = {
        "topic": request.topic,
        "articles": [],
        "summary": "",
        "chat_history": [],
        "question": None,
        "answer": None,
    }

    try:
        result = summarize_graph.invoke(initial_state)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    session_id = create_session(result)

    return {
        "summary": result["summary"],
        "articles": result["articles"],
        "session_id": session_id,
    }


@app.post("/api/followup")
async def followup(request: FollowupRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    state = get_session(request.session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Session not found")

    state_with_question = {**state, "question": request.question}

    try:
        result = qa_graph.invoke(state_with_question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    update_session(request.session_id, result)

    return {"answer": result["answer"]}

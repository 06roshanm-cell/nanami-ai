from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# --------------------------------------------------
# Imports
# --------------------------------------------------

try:
    from .rag import search_feedback
    from .dashboard import get_dashboard_data
    from .hindsight import (
        create_memory,
        search_solution,
        get_all_memory
    )
    from .agents import (
        rag_agent,
        sentiment_agent,
        root_cause_agent,
        recommendation_agent
    )

except ImportError:
    from rag import search_feedback
    from dashboard import get_dashboard_data
    from hindsight import (
        create_memory,
        search_solution,
        get_all_memory
    )
    from agents import (
        rag_agent,
        sentiment_agent,
        root_cause_agent,
        recommendation_agent
    )


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Nanami AI"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# Request models
# --------------------------------------------------

class Query(BaseModel):
    question: str


class SearchIssue(BaseModel):
    issue: str


# --------------------------------------------------
# Home endpoint
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Nanami AI Backend Running"
    }


# --------------------------------------------------
# Dashboard endpoint
# --------------------------------------------------

@app.get("/dashboard")
def dashboard():

    return get_dashboard_data()


# --------------------------------------------------
# Analyze endpoint
# --------------------------------------------------

@app.post("/analyze")
def analyze(data: Query):

    docs = search_feedback(
        data.question
    )

    if isinstance(docs, list):

        answer = "\n\n".join(docs)

    else:

        answer = str(docs)

    return {
        "answer": answer
    }


# --------------------------------------------------
# Multi-Agent endpoint
# --------------------------------------------------

@app.post("/multi-agent")
def multi_agent(data: Query):

    question = data.question.strip()

    # Check empty question
    if not question:

        return {
            "question": "",
            "context": "Please provide a question.",
            "sentiment": "Unknown",
            "root_cause": "Not detected",
            "recommendation": "No recommendation"
        }


    # ----------------------------------------------
    # Agent 1
    # RAG Agent
    # ----------------------------------------------

    context = rag_agent(
        question
    )


    # ----------------------------------------------
    # Agent 2
    # Sentiment Agent
    # ----------------------------------------------

    sentiment = sentiment_agent(
        context
    )


    # ----------------------------------------------
    # Agent 3
    # Root Cause Agent
    # ----------------------------------------------

    root_cause = root_cause_agent(
        context
    )


    # ----------------------------------------------
    # Agent 4
    # Recommendation Agent
    # ----------------------------------------------

    recommendation = recommendation_agent(
        root_cause
    )


    # ----------------------------------------------
    # Return result
    # ----------------------------------------------

    return {
        "question": question,
        "context": context,
        "sentiment": sentiment,
        "root_cause": root_cause,
        "recommendation": recommendation
    }


# --------------------------------------------------
# Remember endpoint
# --------------------------------------------------

@app.post("/remember")
def remember():

    create_memory()

    return {
        "message": "Hindsight memory created successfully"
    }


# --------------------------------------------------
# Solution endpoint
# --------------------------------------------------

@app.post("/solution")
def solution(data: SearchIssue):

    result = search_solution(
        data.issue
    )

    if result:

        return result

    return {
        "solution": "No previous solution found",
        "success": 0
    }


# --------------------------------------------------
# Timeline endpoint
# --------------------------------------------------

@app.get("/timeline")
def timeline():

    return get_all_memory()
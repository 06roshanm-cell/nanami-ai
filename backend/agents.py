# Safe import
try:
    from .rag import search_feedback
except ImportError:
    from rag import search_feedback


# -----------------------------
# Agent 1 : RAG
# -----------------------------
def rag_agent(question):
    docs = search_feedback(question)

    if isinstance(docs, list):
        return "\n".join(docs)

    return str(docs)


# -----------------------------
# Agent 2 : Sentiment
# -----------------------------
def sentiment_agent(context):
    text = context.lower()

    positive = ["good", "excellent", "great", "happy", "love"]
    negative = ["bad", "poor", "drain", "issue", "problem", "disconnect"]

    score = 0

    for word in positive:
        if word in text:
            score += 1

    for word in negative:
        if word in text:
            score -= 1

    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"


# -----------------------------
# Agent 3 : Root Cause
# -----------------------------
def root_cause_agent(context):
    text = context.lower()

    if "battery" in text:
        return "Battery performance issue"
    elif "camera" in text:
        return "Camera software issue"
    elif "wifi" in text:
        return "Connectivity issue"
    else:
        return "General customer issue"


# -----------------------------
# Agent 4 : Recommendation
# -----------------------------
def recommendation_agent(root):

    if "Battery" in root:
        return "Update firmware and recalibrate battery."
    elif "Camera" in root:
        return "Clear cache and install latest camera patch."
    elif "Connectivity" in root:
        return "Reset network settings."
    else:
        return "Perform complete diagnostics."
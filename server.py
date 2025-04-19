from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import os
from agent import AgenticWorkflow

app = FastAPI()

# Replace this with your actual Chrome extension ID
chrome_extension_id = "haiijconnjhoihblofkkakddmfgaefmb"

origins = [
    f"chrome-extension://{chrome_extension_id}"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load questions from local JSON file
def load_questions():
    file_path = os.path.join(os.path.dirname(__file__), 'my_extension', 'data', 'questions.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize questions data
questions_data = load_questions()

@app.post("/")
async def handle_query(request: Request):
    data = await request.json()
    query = data.get("query", "").strip().lower()
    agent_states = []

    # Step 1: Perception
    agent_states.append(f"Perception: Received query '{query}'")

    # Step 2: Memory search
    for subject, questions in questions_data.items():
        for q in questions:
            if query in q["text"].lower():
                agent_states.append("Memory: Answer found in local storage")
                return JSONResponse(content={
                    "answer": q["answer"],
                    "agent_states": agent_states
                })

    # Step 3: Memory miss
    agent_states.append("Memory: No matching answer found in local storage")

    # Step 4: Decision + Action + Observation (call LLM via agent)
    subject = "science"  # You can improve this later by dynamically determining the subject
    agent = AgenticWorkflow(subject=subject, query=query)
    answer = agent.run()

    agent_states.append("Action: Called LLM for answer")
    agent_states.append("Observation: LLM returned the answer")

    return JSONResponse(content={
        "answer": answer,
        "agent_states": agent_states
    })
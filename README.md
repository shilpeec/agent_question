# agent_question

This project is a Chrome Extension + FastAPI backend that helps students quickly find answers to Science questions. It uses a two-level system:

Memory Lookup: Searches in a local database (JSON file).

LLM Fallback: If no match is found, it queries Google Gemini for an answer.

Every response includes an agentic trace (Perception → Memory → Decision → Action → Observation) for transparency and learning insights.

🔧 Features

🧠 Searches known questions from local memory

🤖 Falls back to LLM when memory fails

🔍 Shows how the answer was derived (agent trace)

⚙️ Chrome extension interface

🧪 Includes a CLI script for testing

Answermethirduc/
├── my_extension/
│   ├── popup.html            # Extension popup UI
│   ├── popup.js              # Logic for sending query to background
│   ├── background.js         # Chrome service worker to handle API requests
│   └── data/
│       └── questions.json    # Local memory of questions
├── backend_files/
│   ├── memory.py             # Loads local questions into Paper object
│   ├── models.py             # Pydantic models for Question, Paper, etc.
├── prompts/
│   └── system_prompt.txt     # Prompt template for LLM
├── agent.py                  # AgenticWorkflow class (LLM handler)
├── server.py                 # FastAPI backend server
├── main.py                   # Optional script to run the logic in CLI
├── .env                      # Gemini API key
└── README.md                 # You're here!

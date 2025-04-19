from backend_files.models import Paper, Question
from backend_files.memory import load_science_questions

import google.generativeai as genai
import logging
from jinja2 import Template

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
import os
import google.generativeai as genai


load_dotenv()  # This tells Python to load the .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # This grabs the API key from it

class AgenticWorkflow:
    def __init__(self, subject: str, query: str):
        self.subject = subject
        self.query = query
        self.paper = None
        self.answer = None

    def perceive(self):
        """Perception step: Receive and log the query."""
        logger.info(f"Perception: Received query '{self.query}' for subject '{self.subject}'.")

    def search_memory(self):
        """Memory step: Search for the question in local data."""
        logger.info(f"Memory: Searching for relevant questions in memory for subject '{self.subject}'.")
        self.paper = load_science_questions()  # Adjusted to match your memory.py
        logger.info(f"Memory: Loaded mock paper with {len(self.paper.questions)} questions.")

    def decide(self):
        """Decision step: Build prompt for LLM based on query."""
        if self.subject.lower() not in ["physics", "chemistry", "biology", "maths", "science"]:
            self.subject = "general"  # fallback subject

        try:
            with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
                template = Template(file.read())
            prompt = template.render(subject=self.subject, query=self.query)
            logger.info("Decision: Built LLM prompt from file.")
            return prompt
        except Exception as e:
            logger.error(f"Decision: Error loading or rendering prompt file: {e}")
            # fallback prompt
            fallback = f"You are a helpful tutor. Subject: {self.subject}\nQuestion: {self.query}\nAnswer briefly."
            return fallback

    def act(self, prompt):
        """Action step: Generate answer using LLM."""
        try:
            MODEL_NAME = "models/gemini-1.5-flash"
            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)
            logger.info(f"Raw LLM response: {response}")
            self.answer = response.text.strip()
            logger.info(f"Action: Generated answer '{self.answer}'.")
        except Exception as e:
            self.answer = "Error generating answer from LLM."
            logger.error(f"Action: Error during LLM generation: {e}")

    def observe(self):
        """Observation step: Return the answer."""
        logger.info("Observation: Returning the generated answer.")
        return self.answer

    def run(self):
        """Run the full agentic workflow."""
        self.perceive()
        self.search_memory()
        prompt = self.decide()
        self.act(prompt)
        return self.observe()

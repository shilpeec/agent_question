import json
from backend_files.models import Paper, Question

LOCAL_JSON_PATH = "my_extension/data/questions.json"

# Function to load science questions
def load_science_questions():
    with open(LOCAL_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "science" not in data:
        raise ValueError("Science data not found in the JSON.")

    questions = data["science"]
    question_list = []
    question_number = 1
    for item in questions:
        question_list.append(Question(
            number=question_number,
            text=item["text"],
            marks=2,  # Example mark; adjust according to your requirements
            answer=item["answer"],
            chapter=None,  # If you have chapters, adjust accordingly
            type="Short Answer"
        ))
        question_number += 1

    return Paper(subject="Science", year=2022, questions=question_list)

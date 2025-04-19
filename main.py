# main.py
from backend_files.models import UserQuery, Output
from backend_files.memory import load_mock_paper
from backend_files.prompts import generate_solutions
from pydantic import TypeAdapter

output_adapter = TypeAdapter(Output)

def main():
    query = UserQuery(subject="Science", year=2022, need_solutions=True)
    paper = load_mock_paper(query.subject, query.year)
    answers = generate_solutions(paper) if query.need_solutions else None
    output = Output(paper=paper, answers=answers)
    print(output_adapter.dump_json(output, indent=2))


if __name__ == "__main__":



    main()
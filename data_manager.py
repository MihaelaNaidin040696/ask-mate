import csv
import os

QUESTIONS = os.getenv('QUESTIONS')

def list_questions():
    questions = []
    with open(QUESTIONS, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return sorted(questions, key=lambda question:question['submission_time'])
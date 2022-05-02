import csv
import os

QUESTIONS = os.getenv('QUESTIONS')


def read_questions():
    questions = []
    with open(QUESTIONS, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions

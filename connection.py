import csv
import os

QUESTIONS = os.getenv('QUESTIONS') if 'QUESTIONS' in os.environ else 'question.csv'
ANSWERS = os.getenv('ANSWERS') if 'ANSWERS' in os.environ else 'answer.csv'


def read_questions():
    questions = []
    with open(QUESTIONS, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions

def read_answers():
    answers = []
    with open(ANSWERS, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            answers.append(row)
    return answers


import csv
import os

import data_manager

QUESTIONS = os.getenv('QUESTIONS') if 'QUESTIONS' in os.environ else 'question.csv'
ANSWERS = os.getenv('ANSWERS') if 'ANSWERS' in os.environ else 'answer.csv'
QUESTIONS_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


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


def write_new_question(question):
    with open(QUESTIONS, "a") as f:
        writer = csv.DictWriter(f, QUESTIONS_HEADERS)
        writer.writerow(question)


def write_new_answer(answer):
    with open(ANSWERS, "a") as f:
        writer = csv.DictWriter(f, ANSWERS_HEADERS)
        writer.writerow(answer)


def delete_question(questions):
    with open(QUESTIONS, "w") as f:
        writer = csv.DictWriter(f, QUESTIONS_HEADERS)
        writer.writeheader()
        for question in questions:
            writer.writerow(question)


def delete_answers(answers):
    with open(ANSWERS, "w") as f:
        writer = csv.DictWriter(f, ANSWERS_HEADERS)
        writer.writeheader()
        for answer in answers:
            writer.writerow(answer)
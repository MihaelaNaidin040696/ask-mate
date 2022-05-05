import csv
import os

QUESTIONS = os.getenv('QUESTIONS') if 'QUESTIONS' in os.environ else 'question.csv'
ANSWERS = os.getenv('ANSWERS') if 'ANSWERS' in os.environ else 'answer.csv'
QUESTIONS_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWERS_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') if 'UPLOAD_FOLDER' in os.environ else 'images'


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


def delete_question(question_to_delete):
    questions = read_questions()
    questions.remove(question_to_delete)
    with open(QUESTIONS, "w") as f:
        writer = csv.DictWriter(f, QUESTIONS_HEADERS)
        writer.writeheader()
        for question in questions:
            writer.writerow(question)


def rewrite_questions(question_list):
    with open(QUESTIONS, "w") as f:
        writer = csv.DictWriter(f, QUESTIONS_HEADERS)
        writer.writeheader()
        for question in question_list:
            writer.writerow(question)


def rewrite_answers(answer_list):
    with open(ANSWERS, "w") as f:
        writer = csv.DictWriter(f, ANSWERS_HEADERS)
        writer.writeheader()
        for answer in answer_list:
            writer.writerow(answer)


def delete_answers_by_question_id(question_id):
    answers = read_answers()
    new_answers = []
    for answer in answers:
        if answer['question_id'] == question_id:
            if answer['image']:
                path = os.path.join(os.path.dirname(UPLOAD_FOLDER), 'images', answer['image'])
                os.remove(path)
        if answer['question_id'] != question_id:
            new_answers.append(answer)
    with open(ANSWERS, "w") as f:
        writer = csv.DictWriter(f, ANSWERS_HEADERS)
        writer.writeheader()
        for answer in new_answers:
            writer.writerow(answer)


def delete_answers_by_answer_id(answer_id):
    question_id = ""
    answers = read_answers()
    new_answers = []
    for answer in answers:
        if answer['id'] != answer_id:
            new_answers.append(answer)
        else:
            if answer['image']:
                path = os.path.join(os.path.dirname(UPLOAD_FOLDER), 'images', answer['image'])
                os.remove(path)
            question_id = answer['question_id']
    with open(ANSWERS, "w") as f:
        writer = csv.DictWriter(f, ANSWERS_HEADERS)
        writer.writeheader()
        for answer in new_answers:
            writer.writerow(answer)
    return question_id


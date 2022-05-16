import csv
import os

QUESTIONS = os.path.join(os.path.dirname(__file__), "sample_data", "question.csv")
ANSWERS = os.path.join(os.path.dirname(__file__), "sample_data", "answer.csv")

QUESTIONS_HEADERS = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image",
]
ANSWERS_HEADERS = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "images")


def read_file(file):
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)


def read_questions():
    return read_file(QUESTIONS)


def read_answers():
    return read_file(ANSWERS)


def write_file(file, headers, data):
    with open(file, "a") as f:
        writer = csv.DictWriter(f, headers)
        writer.writerow(data)


def write_new_question(question):
    write_file(QUESTIONS, QUESTIONS_HEADERS, question)


def write_new_answer(answer):
    write_file(ANSWERS, ANSWERS_HEADERS, answer)


def rewrite_file(file, headers, data):
    with open(file, "w") as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)


def delete_question(question_to_delete):
    questions = read_questions()
    questions.remove(question_to_delete)

    rewrite_file(QUESTIONS, QUESTIONS_HEADERS, questions)


def rewrite_questions(question_list):
    rewrite_file(QUESTIONS, QUESTIONS_HEADERS, question_list)


def rewrite_answers(answer_list):
    rewrite_file(ANSWERS, ANSWERS_HEADERS, answer_list)


def delete_image_from_file(image):
    if image:
        path = os.path.join(os.path.dirname(UPLOAD_FOLDER), "images", image)
        os.remove(path)


def delete_answers_by_question_id(question_id):
    new_answers = []

    for answer in read_answers():
        if answer["question_id"] == question_id:
            delete_image_from_file(answer.get("image"))

        if answer["question_id"] != question_id:
            new_answers.append(answer)

    rewrite_file(ANSWERS, ANSWERS_HEADERS, new_answers)


def delete_answers_by_answer_id(answer_id):
    question_id = ""
    new_answers = []

    for answer in read_answers():
        if answer["id"] != answer_id:
            new_answers.append(answer)
        else:
            delete_image_from_file(answer.get("image"))
            question_id = answer["question_id"]

    rewrite_file(ANSWERS, ANSWERS_HEADERS, new_answers)

    return question_id

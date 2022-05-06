import connection
import os
from connection import UPLOAD_FOLDER


def list_questions():
    questions = connection.read_questions()
    return sorted(questions, key=lambda question: question["submission_time"])


def get_question_by_id(id):
    questions = connection.read_questions()
    for question in questions:
        if question["id"] == id:
            question["view_number"] = str(int(question["view_number"]) + 1)
            rewrite_questions(questions)
            return question


def get_answers_by_question_id(id):
    return [
        answer for answer in connection.read_answers() if answer["question_id"] == id
    ]


def write_question(new_question):
    connection.write_new_question(new_question)


def rewrite_questions(question_list):
    connection.rewrite_questions(question_list)


def write_answer(new_answer):
    connection.write_new_answer(new_answer)


def sort_questions(questions, criteria, direction):
    for question in questions:
        question["view_number"] = int(question["view_number"])
        question["vote_number"] = int(question["vote_number"])

    condition = direction == "desc"
    return sorted(questions, key=lambda question: question[criteria], reverse=condition)


def delete_question(question_id):
    question = get_question_by_id(question_id)
    connection.delete_image_from_file(question["image"])
    connection.delete_answers_by_question_id(question_id)
    connection.delete_question(question)


def delete_answer(answer_id):
    return connection.delete_answers_by_answer_id(answer_id)


def vote_question(id, modifier):
    questions = connection.read_questions()
    for question in questions:
        if question["id"] == id:
            question["vote_number"] = int(question["vote_number"]) + modifier
    connection.rewrite_questions(questions)


def vote_answer(id, modifier):
    answers = connection.read_answers()
    for answer in answers:
        if answer["id"] == id:
            answer["vote_number"] = int(answer["vote_number"]) + modifier
            question_id = answer["question_id"]
            connection.rewrite_answers(answers)
            return question_id


def vote_up_question(id):
    vote_question(id, 1)


def vote_down_question(id):
    vote_question(id, -1)


def vote_up_answer(id):
    return vote_answer(id, 1)


def vote_down_answer(id):
    return vote_answer(id, -1)

import connection
import util


def list_questions():
    questions = connection.read_questions()
    for question in questions:
        question['time'] = util.get_datetime_format(question['submission_time'])
    return sorted(questions, key=lambda question: question['submission_time'])


def get_question_by_id(id):
    questions = connection.read_questions()
    for question in questions:
        if question['id'] == id:
            return question


def get_answers_by_question_id(id):
    answers = connection.read_answers()
    question_answers = []
    for answer in answers:
        if answer['question_id'] == id:
            question_answers.append(answer)
    return question_answers


def write_question(new_question):
    connection.write_new_question(new_question)


def write_answer(new_answer):
    connection.write_new_answer(new_answer)


def sort_questions(questions, criteria, direction):
    if direction == 'asc':
        return sorted(questions, key=lambda question: question[criteria])
    else:
        return sorted(questions, key=lambda question: question[criteria], reverse=True)


def delete_question(question_id):
    question = get_question_by_id(question_id)
    connection.delete_answers_by_question_id(question_id)
    connection.delete_question(question)


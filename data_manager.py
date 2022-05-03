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
            question['submission_time'] = util.get_datetime_format(question['submission_time'])
            return question


def get_answers_by_question_id(id):
    answers = connection.read_answers()
    question_answers = []
    for answer in answers:
        if answer['question_id'] == id:
            answer['submission_time'] = util.get_datetime_format(answer['submission_time'])
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


def delete_question(id):
    questions = connection.read_questions()
    answers = connection.read_answers()
    deleted_question = {}
    deleted_answers = get_answers_by_question_id(id)
    for question in questions:
        if question['id'] == id:
            deleted_question = question
    questions.remove(deleted_question)
    connection.delete_question(questions)
    for answer in deleted_answers:
        answers.remove(answer)

    connection.delete_answers(answers)



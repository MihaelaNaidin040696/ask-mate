import connection


def list_questions():
    questions = connection.read_questions()
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

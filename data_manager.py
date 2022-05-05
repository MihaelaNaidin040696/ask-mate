import connection


def list_questions():
    questions = connection.read_questions()
    return sorted(questions, key=lambda question: question['submission_time'])


def get_question_by_id(id):
    questions = connection.read_questions()
    for question in questions:
        if question['id'] == id:
            question['view_number'] = int(question['view_number']) + 1
            rewrite_questions(questions)
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


def rewrite_questions(question_list):
    connection.rewrite_questions(question_list)


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


def delete_answer(answer_id):
    return connection.delete_answers_by_answer_id(answer_id)


def vote_up_question(id):
    questions = connection.read_questions()
    for question in questions:
        if question['id'] == id:
            question['vote_number'] = int(question['vote_number']) + 1
    connection.rewrite_questions(questions)


def vote_down_question(id):
    questions = connection.read_questions()
    for question in questions:
        if question['id'] == id:
            question['vote_number'] = int(question['vote_number']) - 1
    connection.rewrite_questions(questions)


def vote_up_answer(id):
    answers = connection.read_answers()
    for answer in answers:
        if answer['id'] == id:
            answer['vote_number'] = int(answer['vote_number']) + 1
            question_id = answer['question_id']
            connection.rewrite_answers(answers)
            return question_id


def vote_down_answer(id):
    answers = connection.read_answers()
    for answer in answers:
        if answer['id'] == id:
            answer['vote_number'] = int(answer['vote_number']) - 1
            question_id = answer['question_id']
            connection.rewrite_answers(answers)
            return question_id


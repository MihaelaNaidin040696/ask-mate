from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    query = """select * from question order by submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor,id):
    query=f"""
        SELECT title, message
        FROM question
        WHERE id = {id}"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, id) -> list:
    query = """select * from answer where question_id = id"""
    value = {"id": id}
    cursor.execute(query, value)
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, criteria, direction) -> list:
    query =  f"""select * from question order by {criteria} {direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_question(cursor, title, message, image):
    query = f"""
    INSERT INTO question (submission_time,view_number, vote_number, title, message, image)
    VALUES (now(), 0, 0, '{title}', '{message}', '{image}')"""
    cursor.execute(query)

#     connection.write_new_question(new_question)
#
#

#
#
# def write_answer(new_answer):
#     connection.write_new_answer(new_answer)
#
#
#
#
# def delete_question(question_id):
#     question = get_question_by_id(question_id)
#     connection.delete_image_from_file(question["image"])
#     connection.delete_answers_by_question_id(question_id)
#     connection.delete_question(question)
#
#
# def delete_answer(answer_id):
#     return connection.delete_answers_by_answer_id(answer_id)
#
#
# def vote_question(id, modifier):
#     questions = connection.read_questions()
#     for question in questions:
#         if question["id"] == id:
#             question["vote_number"] = int(question["vote_number"]) + modifier
#     connection.rewrite_questions(questions)
#
#
# def vote_answer(id, modifier):
#     answers = connection.read_answers()
#     for answer in answers:
#         if answer["id"] == id:
#             answer["vote_number"] = int(answer["vote_number"]) + modifier
#             question_id = answer["question_id"]
#             connection.rewrite_answers(answers)
#             return question_id
#
#
# def vote_up_question(id):
#     vote_question(id, 1)
#
#
# def vote_down_question(id):
#     vote_question(id, -1)
#
#
# def vote_up_answer(id):
#     return vote_answer(id, 1)
#
#
# def vote_down_answer(id):
#     return vote_answer(id, -1)

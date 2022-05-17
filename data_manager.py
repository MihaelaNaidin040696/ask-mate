from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_questions(cursor: RealDictCursor) -> list:
    cursor.execute(
        """
        SELECT * 
        FROM question 
        ORDER BY submission_time"""
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT title, message
        FROM question
        WHERE id = %(id)s;""",
        {"id": id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_answers_by_question_id(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT * 
        FROM answer 
        WHERE question_id = %(id)s;""",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def sort_questions(cursor: RealDictCursor, criteria, direction) -> list:
    query = f"""
        SELECT * 
        FROM question 
        ORDER BY {criteria} {direction}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_question(cursor, title, message, image):
    cursor.execute(
        """
    INSERT INTO question (submission_time,view_number, vote_number, title, message, image)
    VALUES (now()::timestamp(0), 0, 0, %(title)s, %(message)s, %(image)s);""",
        {"title": title, "message": message, "image": image},
    )


@database_common.connection_handler
def write_answer(cursor: RealDictCursor, question_id, message, image):
    cursor.execute(
        """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (now()::timestamp(0), 0, %(question_id)s, %(message)s, %(image)s);""",
        {"question_id": question_id, "message": message, "image": image},
    )


@database_common.connection_handler
def delete_question(cursor: RealDictCursor, id):
    print(
        cursor.execute(
            """
            DELETE FROM comment WHERE question_id = %(id)s;
            DELETE FROM answer WHERE question_id = %(id)s;
            DELETE FROM question_tag WHERE question_id = %(id)s;
            DELETE FROM question WHERE id = %(id)s;""",
            {"id": id},
        )
    )


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

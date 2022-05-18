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
def get_answers_by_answer_id(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        f"""
        SELECT * 
        FROM answer 
        WHERE id = {id};"""

    )
    return cursor.fetchone()


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


def delete_answer(cursor: RealDictCursor, id):
    print(
        cursor.execute(
            """
            DELETE FROM comment WHERE answer_id = %(id)s;
            DELETE FROM answer WHERE id = %(id)s;""",
            {"id": id},
        )
    )


@database_common.connection_handler
def edit_question(cursor: RealDictCursor, id, title, message):
    cursor.execute(
        """
        UPDATE question SET title = %(title)s, message = %(message)s
        WHERE id = %(id)s;""",
        {"id": id, "title": title, "message": message},
    )


@database_common.connection_handler
def vote_up_question(cursor: RealDictCursor, id):
    cursor.execute(
        """
        UPDATE question SET vote_number = vote_number + 1
        WHERE id = %(id)s;""",
        {"id": id},
    )


@database_common.connection_handler
def vote_down_question(cursor: RealDictCursor, id):
    cursor.execute(
        """
        UPDATE question SET vote_number = vote_number - 1
        WHERE id = %(id)s;""",
        {"id": id},
    )


@database_common.connection_handler
def vote_up_answer(cursor: RealDictCursor, id):
    cursor.execute(
        """
        UPDATE answer SET vote_number = vote_number + 1
        WHERE id = %(id)s ;""",
        {"id": id},

    )


@database_common.connection_handler
def vote_down_answer(cursor: RealDictCursor, id):
    cursor.execute(
        """
        UPDATE answer SET vote_number = vote_number - 1
        WHERE id = %(id)s;""",
        {"id": id},
    )


@database_common.connection_handler
def get_question_comments(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT message, submission_time
        FROM comment
        WHERE question_id = %(id)s;""",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_comments(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT message, submission_time
        FROM comment
        WHERE answer_id = %(id)s;""",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def add_question_comment(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        INSERT INTO comment (question_id, message, submission_time, edited_count)
        VALUES (%(id)s, %(message)s, now()::timestamp(0), 0);""",
        {'id': id, 'message': message}
    )


@database_common.connection_handler
def add_answer_comment(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        INSERT INTO comment (answer_id, message, submission_time, edited_count)
        VALUES (%(id)s, %(message)s, now()::timestamp(0), 0);""",
        {'id': id, 'message': message}
    )


def get_id_question_by_id_answer(cursor, answer_id):
    cursor.execute(
        """
        SELECT question_id FROM answer
        WHERE question_id = %(answer_id)s;""",
        {"answer_id": answer_id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        UPDATE answer SET message = %(message)s
        WHERE id = %(id)s;""",
        {"id": id, "message": message},
    )


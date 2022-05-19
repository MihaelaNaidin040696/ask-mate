from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_headers(cursor: RealDictCursor) -> list:
    cursor.execute(
        """
        SELECT * 
        FROM question 
        ORDER BY submission_time"""
    )
    return cursor.fetchone()


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
def get_answer_id_by_question_id(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT id
        FROM answer
        WHERE question_id = %(id)s;""",
        {"id": id},
    )
    answer_dict = cursor.fetchone()
    return dict(answer_dict)["id"]


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
def get_answers_by_answer_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute(
        f"""
        SELECT * 
        FROM answer 
        WHERE id = {id};"""
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_comments_by_comment_id(cursor: RealDictCursor, id: int) -> list:
    cursor.execute(
        f"""
        SELECT * 
        FROM comment 
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
    VALUES (now()::timestamp(0), 0, 0, %(title)s, %(message)s, %(image)s) returning id;""",
        {"title": title, "message": message, "image": image},
    )
    return cursor.fetchone()


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


@database_common.connection_handler
def delete_answer(cursor: RealDictCursor, id):
    cursor.execute(
        """
            DELETE FROM comment WHERE answer_id = %(id)s;
            DELETE FROM answer WHERE id = %(id)s;""",
        {"id": id},
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
        SELECT *
        FROM comment
        WHERE question_id = %(id)s;""",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_answer_comments(cursor: RealDictCursor, id) -> list:
    cursor.execute(
        """
        SELECT message, submission_time, edited_count
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
        {"id": id, "message": message},
    )


@database_common.connection_handler
def add_answer_comment(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        INSERT INTO comment (answer_id, message, submission_time, edited_count)
        VALUES (%(id)s, %(message)s, now()::timestamp(0), 0);""",
        {"id": id, "message": message},
    )


@database_common.connection_handler
def get_id_question_by_id_answer(cursor: RealDictCursor, answer_id):
    cursor.execute(
        """
        SELECT question_id FROM answer
        WHERE id = %(answer_id)s;""",
        {"answer_id": answer_id},
    )
    answer_dict = cursor.fetchone()
    return answer_dict["question_id"]


@database_common.connection_handler
def get_id_question_by_id_comment(cursor: RealDictCursor, comment_id):
    cursor.execute(
        """
        SELECT question_id FROM comment
        WHERE id = %(comment_id)s;""",
        {"comment_id": comment_id},
    )
    answer_dict = cursor.fetchone()
    return dict(answer_dict)["question_id"]


@database_common.connection_handler
def get_id_answer_by_id_comment(cursor: RealDictCursor, comment_id):
    cursor.execute(
        """
        SELECT answer_id FROM comment
        WHERE id = %(comment_id)s;""",
        {"comment_id": comment_id},
    )
    answer_dict = cursor.fetchone()
    return dict(answer_dict)["answer_id"]


@database_common.connection_handler
def edit_answer(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        UPDATE answer SET message = %(message)s, submission_time = now()::timestamp(0) 
        WHERE id = %(id)s;""",
        {"id": id, "message": message},
    )


@database_common.connection_handler
def edit_comment(cursor: RealDictCursor, id, message):
    cursor.execute(
        """
        UPDATE comment 
        SET message = %(message)s, 
            submission_time = now()::timestamp(0),
            edited_count = edited_count + 1
        WHERE id = %(id)s;""",
        {"id": id, "message": message},
    )


@database_common.connection_handler
def get_tags(cursor: RealDictCursor):
    cursor.execute(
        """
        SELECT name 
        FROM tag"""
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id(cursor, name):
    cursor.execute("SELECT id FROM tag WHERE name = %(name)s;", {"name": name})
    return cursor.fetchone()


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute(
        """
        SELECT * FROM tag
        JOIN question_tag qt on tag.id = qt.tag_id
        WHERE qt.question_id=%(question_id)s""",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def add_new_tag(cursor: RealDictCursor, name):
    cursor.execute(
        """
    INSERT INTO tag( name )
    VALUES(%(name)s)
    """,
        {"name": name},
    )


@database_common.connection_handler
def delete_comment(cursor: RealDictCursor, id):
    cursor.execute(
        """
        DELETE FROM comment 
        WHERE id = %(id)s;""",
        {"id": id},
    )


@database_common.connection_handler
def add_question_tag(cursor: RealDictCursor, question_id, tag_id):
    cursor.execute(
        """
        INSERT INTO question_tag (question_id, tag_id)
        VALUES(%(question_id)s, %(tag_id)s)""",
        {"question_id": question_id, "tag_id": tag_id},
    )


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute(
        """    
    DELETE FROM question_tag WHERE question_id = %(question_id)s and tag_id = %(tag_id)s""",
        {"tag_id": tag_id, "question_id": question_id},
    )

from psycopg2._psycopg import cursor
from psycopg2.extras import RealDictCursor
import database_common


@database_common.connection_handler
def get_headers(cursor):
    cursor.execute("SELECT * FROM question ORDER BY submission_time;")
    return cursor.fetchone()


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("SELECT * FROM question ORDER BY submission_time;")
    return cursor.fetchall()


@database_common.connection_handler
def get_question_by_id(cursor, id):
    cursor.execute(
        "SELECT title, message FROM question WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_answer_id_by_question_id(cursor, id):
    cursor.execute(
        "SELECT id FROM answer WHERE question_id = %(id)s;",
        {"id": id},
    )
    answer_dict = cursor.fetchall()
    return dict(answer_dict)["id"]


@database_common.connection_handler
def get_answers_by_question_id(cursor, id):
    cursor.execute(
        "SELECT * FROM answer WHERE question_id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_by_answer_id(cursor, id):
    cursor.execute(
        "SELECT * FROM answer WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_comments_by_comment_id(cursor, id):
    cursor.execute(
        "SELECT * FROM comment WHERE id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchone()


@database_common.connection_handler
def sort_questions(cursor, criteria, direction):
    query = f"""
        SELECT * 
        FROM question 
        ORDER BY {criteria} {direction};
        """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def write_question(cursor, title, message, image):
    cursor.execute(
        """
            INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
            VALUES (now()::timestamp(0), 0, 0, %(title)s, %(message)s, %(image)s) RETURNING id;
        """,
        {
            "title": title,
            "message": message,
            "image": image,
        },
    )
    return cursor.fetchone()


@database_common.connection_handler
def write_answer(cursor, question_id, message, image):
    cursor.execute(
        """
            INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES (now()::timestamp(0), 0, %(question_id)s, %(message)s, %(image)s);
        """,
        {
            "question_id": question_id,
            "message": message,
            "image": image,
        },
    )


@database_common.connection_handler
def delete_question(cursor, id):
    cursor.execute(
        """
            DELETE FROM comment WHERE question_id = %(id)s;
            DELETE FROM answer WHERE question_id = %(id)s;
            DELETE FROM question_tag WHERE question_id = %(id)s;
            DELETE FROM question WHERE id = %(id)s;
        """,
        {"id": id},
    )


@database_common.connection_handler
def delete_answer(cursor, id):
    cursor.execute(
        """
            DELETE FROM comment WHERE answer_id = %(id)s;
            DELETE FROM answer WHERE id = %(id)s;
        """,
        {"id": id},
    )


@database_common.connection_handler
def edit_question(cursor, id, title, message):
    cursor.execute(
        "UPDATE question SET title = %(title)s, message = %(message)s WHERE id = %(id)s;",
        {
            "id": id,
            "title": title,
            "message": message,
        },
    )


@database_common.connection_handler
def vote_item(cursor, table, id, modifier):
    cursor.execute(
        f"UPDATE {table} SET vote_number = vote_number + %(modifier)s WHERE id = %(id)s;",
        {
            "id": id,
            "modifier": modifier,
        },
    )


def vote_up_question(id):
    vote_item(id, "question", 1)


def vote_down_question(id):
    vote_item(id, "question", -1)


def vote_up_answer(id):
    vote_item(id, "answer", 1)


def vote_down_answer(id):
    vote_item(id, "answer", -1)


@database_common.connection_handler
def get_question_comments(cursor, id):
    cursor.execute(
        "SELECT * FROM comment WHERE question_id = %(id)s;",
        {"id": id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_comments(cursor):
    cursor.execute("SELECT * FROM comment;")
    return cursor.fetchall()


@database_common.connection_handler
def add_question_comment(cursor, id, message):
    cursor.execute(
        """
            INSERT INTO comment (question_id, message, submission_time, edited_count)
            VALUES (%(id)s, %(message)s, now()::timestamp(0), 0);
        """,
        {
            "id": id,
            "message": message,
        },
    )


@database_common.connection_handler
def add_answer_comment(cursor, id, message):
    cursor.execute(
        """
            INSERT INTO comment (answer_id, message, submission_time, edited_count)
            VALUES (%(id)s, %(message)s, now()::timestamp(0), 0);
        """,
        {
            "id": id,
            "message": message,
        },
    )


@database_common.connection_handler
def get_id_for_item(cursor, item, table, id):
    cursor.execute(
        f"SELECT {item} FROM {table} WHERE id = %(id)s;",
        {"id": id},
    )
    answer_dict = cursor.fetchone()
    return answer_dict[item]


def get_id_question_by_id_answer(answer_id):
    return get_id_for_item("question_id", "answer", answer_id)


def get_id_question_by_id_comment(comment_id):
    return get_id_for_item("question_id", "comment", comment_id)


def get_id_answer_by_id_comment(comment_id):
    return get_id_for_item("answer_id", "comment", comment_id)


@database_common.connection_handler
def edit_answer(cursor, id, message):
    cursor.execute(
        "UPDATE answer SET message = %(message)s, submission_time = now()::timestamp(0) WHERE id = %(id)s;",
        {
            "id": id,
            "message": message,
        },
    )


@database_common.connection_handler
def edit_comment(cursor, id, message):
    cursor.execute(
        "UPDATE comment SET message = %(message)s, submission_time = now()::timestamp(0), edited_count = edited_count + 1 WHERE id = %(id)s;",
        {
            "id": id,
            "message": message,
        },
    )


@database_common.connection_handler
def get_tags(cursor):
    cursor.execute("SELECT name FROM tag;")
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id(cursor, name):
    cursor.execute(
        "SELECT id FROM tag WHERE name = %(name)s;",
        {"name": name},
    )
    return cursor.fetchone()


@database_common.connection_handler
def get_tags_by_question_id(cursor, question_id):
    cursor.execute(
        "SELECT * FROM tag JOIN question_tag qt ON tag.id = qt.tag_id WHERE qt.question_id = %(question_id)s;",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@database_common.connection_handler
def add_new_tag(cursor, name):
    cursor.execute(
        "INSERT INTO tag(name) VALUES (%(name)s);",
        {"name": name},
    )


@database_common.connection_handler
def delete_comment(cursor, id):
    cursor.execute(
        "DELETE FROM comment WHERE id = %(id)s;",
        {"id": id},
    )


@database_common.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    cursor.execute(
        "INSERT INTO question_tag (question_id, tag_id) VALUES (%(question_id)s, %(tag_id)s);",
        {
            "question_id": question_id,
            "tag_id": tag_id,
        },
    )


@database_common.connection_handler
def delete_tag(cursor, question_id, tag_id):
    cursor.execute(
        "DELETE FROM question_tag WHERE question_id = %(question_id)s and tag_id = %(tag_id)s;",
        {
            "tag_id": tag_id,
            "question_id": question_id,
        },
    )


@database_common.connection_handler
def get_data_for_search_question(cursor, search):
    cursor.execute(
        "SELECT * FROM question WHERE title ILIKE %(search)s OR message ILIKE %(search)s OR image ILIKE %(search)s;",
        {"search": f"%{search}%"},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_data_for_search_answer(cursor, search):
    cursor.execute(
        "SELECT * FROM answer WHERE message ILIKE %(search)s or image ILIKE %(search)s;",
        {"search": f"%{search}%"},
    )
    return cursor.fetchall()


@database_common.connection_handler
def get_latest_questions(cursor):
    cursor.execute(
        "SELECT submission_time, title, message FROM question ORDER BY submission_time LIMIT 5;"
    )
    return cursor.fetchall()


@database_common.connection_handler
def select_user(cursor, username):
    cursor.execute(
        "SELECT * FROM user_registration "
        "WHERE username ILIKE %(username)s;",
        {"username": f"%{username}%"}
    )
    return cursor.fetchone()


@database_common.connection_handler
def insert_user_credentials(cursor, username, email, password):
    cursor.execute(
        "INSERT INTO user_registration (submission_time, username, email, password)"
        "VALUES (now()::timestamp(0), %(username)s, %(email)s, %(password)s);",
        {'username': username, 'email': email, 'password': password}
    )



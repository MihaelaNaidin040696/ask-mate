import connection
from datetime import timedelta


def get_id():
    return max([int(question.get("id")) for question in connection.read_questions()]) + 1


def get_datetime_format():
    questions = connection.read_questions()
    sec = questions['submission_time']
    datetime_format = timedelta(seconds=sec)
    return datetime_format


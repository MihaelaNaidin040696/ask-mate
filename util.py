import connection
from datetime import datetime


def get_id():
    return max([int(question.get("id")) for question in connection.read_questions()]) + 1


def get_datetime_format(sec):
    datetime_format = datetime.fromtimestamp(float(sec) / 1000.0)
    datetime_format=datetime_format.strftime("%B %d, %Y %I:%M")
    return datetime_format


def get_now_datetime():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S:%fff")
    now = datetime.strptime(now, "%d/%m/%Y %H:%M:%S:%fff")
    current_time = now.timestamp() * 1000
    return current_time


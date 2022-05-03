import connection
# from datetime import timedelta
from datetime import datetime
import time


def get_id():
    return max([int(question.get("id")) for question in connection.read_questions()]) + 1


def get_datetime_format(sec):
    datetime_format = datetime.fromtimestamp(int(sec)).strftime("%B %d, %Y %I:%M")
    return datetime_format


def get_now_datetime():
    dt = round(time.time())
    return dt




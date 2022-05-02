import connection

def list_questions():
    questions = connection.read_questions()
    return sorted(questions, key=lambda question:question['submission_time'])

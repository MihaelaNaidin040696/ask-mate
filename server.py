from flask import Flask, render_template

import data_manager

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def display_questions():
    questions= data_manager.list_questions()
    return render_template('list_of_questions.html', questions=questions)

@app.route("/question/<question_id>")
def display_question_by_id(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template("individual_question.html", question=question, answers = answers)

if __name__ == "__main__":
    app.run()

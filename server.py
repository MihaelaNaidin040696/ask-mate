from flask import Flask, render_template, request, url_for, redirect

import data_manager
import util

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


@app.route("/add-question", methods=['GET','POST'])
def add_new_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":
        new_question = {}
        new_question["id"] = util.get_id()
        new_question["submission_time"] = 0
        new_question["view_number"] = 0
        new_question["vote_number"] = 0
        new_question["title"] = request.form.get('title')
        new_question["message"] = request.form.get('message')
        new_question["image"] = ""
        data_manager.write_question(new_question)
        return redirect(url_for('display_question_by_id', question_id=new_question['id']))


if __name__ == "__main__":
    app.run()

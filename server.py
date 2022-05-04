from flask import Flask, render_template, request, url_for, redirect
import data_manager
import util
import os

app = Flask(__name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER') if 'UPLOAD_FOLDER' in os.environ else 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def display_questions():
    questions = data_manager.list_questions()
    criteria = request.args.get('order_by', 'submission_time')
    direction = request.args.get('order_direction', 'desc')
    sorted_questions = data_manager.sort_questions(questions, criteria, direction)
    return render_template('list_of_questions.html', questions=sorted_questions)


@app.template_filter('datetime')
def convert_datetime(sec):
    return util.get_datetime_format(sec)


@app.route("/question/<question_id>")
def display_question_by_id(question_id):
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    return render_template("individual_question.html", question=question, answers=answers)


@app.route("/add-question", methods=['GET', 'POST'])
def add_new_question():
    if request.method == "GET":
        return render_template("add_question.html")
    elif request.method == "POST":
        new_question = {}
        file = request.files["image"]
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            new_question["image"] = file.filename
        else:
            new_question["image"] = ""
        new_question["id"] = util.get_id()
        new_question["submission_time"] = util.get_now_datetime()
        new_question["view_number"] = 0
        new_question["vote_number"] = 0
        new_question["title"] = request.form.get('title')
        new_question["message"] = request.form.get('message')

        data_manager.write_question(new_question)
        return redirect(url_for('display_question_by_id', question_id=new_question['id']))


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_new_answer(question_id):
    if request.method == "GET":
        return render_template("add_answer.html", question_id=question_id)
    if request.method == "POST":
        file = request.files["image"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        new_answer = {}
        new_answer['id'] = util.get_id()
        new_answer['submission_time'] = util.get_now_datetime()
        new_answer["vote_number"] = 0
        new_answer["question_id"] = question_id
        new_answer['message'] = request.form.get('message')
        new_answer["image"] = file.filename
        data_manager.write_answer(new_answer)
        return redirect(url_for('display_question_by_id', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_questions(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for('display_questions'))


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def edit_question(question_id):
    questions = data_manager.list_questions()
    entry = [question for question in questions if question['id'] == question_id][0]
    if request.method == "POST":
        for question in questions:
            if question["id"] == question_id:
                question["title"] = request.form.get('title')
                question["message"] = request.form.get('message')
        data_manager.rewrite_questions(questions)
        return redirect(url_for('display_question_by_id', question_id=question_id))
    return render_template('edit_question.html', question=entry)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answers(answer_id):
    question_id = data_manager.delete_answer(answer_id)
    return redirect(url_for('display_question_by_id', question_id=question_id))


@app.route('/question/<question_id>/vote-up')
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect(url_for('display_questions'))


@app.route('/question/<question_id>/vote-down')
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect(url_for('display_questions'))


@app.route('/answer/<answer_id>/vote-up')
def vote_up_answer(answer_id):
    question_id = data_manager.vote_up_answer(answer_id)
    return redirect(url_for('display_question_by_id', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down')
def vote_down_answer(answer_id):
    question_id = data_manager.vote_down_answer(answer_id)
    return redirect(url_for('display_question_by_id', question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)

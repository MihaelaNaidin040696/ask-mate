from flask import Flask, render_template, request, url_for, redirect, session

import data_manager
import os
import re
import hash_pass
from bonus_questions import SAMPLE_QUESTIONS


app = Flask(__name__)
app.secret_key = "_5#y2LF4Q8z\xec]/"


UPLOAD_FOLDER = (
    os.getenv("UPLOAD_FOLDER") if "UPLOAD_FOLDER" in os.environ else "images"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


def get_request_data():
    return (
        request.values.get("order_by", "submission_time"),
        request.values.get("order_direction", "desc"),
        request.values.get("info"),
    )


def upload_image():
    image = ""
    file = request.files["image"]
    if file:
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
        image = file.filename
    return image


@app.route("/")
def display_latest_questions():
    latest_questions = data_manager.get_latest_questions()
    return render_template("latest_questions.html", questions=latest_questions)


@app.route("/list")
def display_questions():
    criteria, direction, search = get_request_data()
    sorted_questions = data_manager.sort_questions(criteria, direction)
    return render_template(
        "list_of_questions.html",
        questions=sorted_questions,
        search=search,
    )


@app.route("/search", methods=["GET", "POST"])
def search_list():
    criteria, direction, search = get_request_data()
    dates_question = data_manager.get_data_for_search_question(search)
    dates_answer = data_manager.get_data_for_search_answer(search)
    sorted_questions = data_manager.sort_questions(criteria, direction)
    return render_template(
        "list_of_questions.html",
        questions=sorted_questions,
        dates=dates_question,
        search=search,
        date=dates_answer,
    )


@app.route("/question/<question_id>")
def display_question_by_id(question_id):
    view_number = data_manager.view_number(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comment = data_manager.get_question_comments(question_id)
    answer_comment = data_manager.get_comments()
    return render_template(
        "individual_question.html",
        question=question,
        view_number=view_number,
        answers=answers,
        question_id=question_id,
        question_comment=question_comment,
        answer_comment=answer_comment,
        tags=data_manager.get_tags_by_question_id(question_id),
    )


@app.route("/add-question", methods=["GET", "POST"])
def add_new_question():
    if request.method == "POST":
        image = upload_image()
        qid = data_manager.write_question(
            request.form.get("title").capitalize(),
            request.form.get("message").capitalize(),
            image,session['id']
        )

        return redirect(
            url_for(
                "display_question_by_id",
                question_id=qid.get("id"),
            )
        )
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id):
    if request.method == "POST":
        image = upload_image()
        data_manager.write_answer(
            question_id,
            request.form.get("message").capitalize(),
            image,
            session['id'],
        )
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "add_answer.html",
        question_id=question_id,
    )


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_questions(question_id):
    data_manager.delete_question(question_id, session['id'])
    return redirect(
        url_for(
            "display_questions",
            question_id=question_id,
        )
    )


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answers(answer_id):
    question_id = data_manager.get_answers_by_answer_id(answer_id)["question_id"]
    data_manager.delete_answer(answer_id, session['id'])
    return redirect(
        url_for(
            "display_question_by_id",
            answer_id=answer_id,
            question_id=question_id,
        )
    )


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = data_manager.get_question_by_id(question_id)
    if request.method == "POST":
        title = request.form.get("title")
        message = request.form.get("message")
        data_manager.edit_question(question_id, title, message)
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "edit_question.html",
        question=question,
        question_id=question_id,
    )


def vote_question(qid, callback):
    callback(qid)
    return redirect(url_for("display_questions"))


def vote_answer(aid, callback):
    question_id = data_manager.get_id_question_by_id_answer(aid)
    callback(aid)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=question_id,
        )
    )


@app.route("/question/<question_id>/vote-up")
def vote_up_question(question_id):
    return vote_question(question_id, data_manager.vote_up_question)


@app.route("/question/<question_id>/vote-down")
def vote_down_question(question_id):
    return vote_question(question_id, data_manager.vote_down_question)


@app.route("/answer/<answer_id>/vote-up")
def vote_up_answer(answer_id):
    return vote_answer(answer_id, data_manager.vote_up_answer)


@app.route("/answer/<answer_id>/vote-down")
def vote_down_answer(answer_id):
    return vote_answer(answer_id, data_manager.vote_down_answer)


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        data_manager.add_question_comment(question_id, request.form.get("message"), session['id'])
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "add_question_comment.html",
        question_id=question_id,
    )


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment(answer_id):
    question_id = data_manager.get_id_question_by_id_answer(answer_id)
    if request.method == "POST":
        data_manager.add_answer_comment(answer_id, request.form.get("message"), session['id'])
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "add_answer_comment.html",
        answer_id=answer_id,
        question_id=question_id,
    )


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    answer = data_manager.get_answers_by_answer_id(answer_id)
    if request.method == "POST":
        question_id = data_manager.get_id_question_by_id_answer(answer_id)
        message = request.form.get("message")
        data_manager.edit_answer(answer_id, message)
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "edit_answer.html",
        answer=answer,
        answer_id=answer_id,
    )


@app.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment(comment_id):
    question_id = data_manager.get_id_question_by_id_comment(comment_id)
    comment = data_manager.get_comments_by_comment_id(comment_id)
    if request.method == "POST":
        data_manager.edit_comment(comment_id, request.form.get("message"))
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
    return render_template(
        "edit_comment.html",
        comment=comment,
        comment_id=comment_id,
        question_id=question_id,
    )


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    question_id = data_manager.get_id_question_by_id_comment(comment_id)
    data_manager.delete_comment(comment_id)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=question_id,
        )
    )


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_question_tag(question_id):
    if request.method == "POST":
        tag = request.form.get("tag", request.form.get("name"))
        tag_id = data_manager.get_tag_id(tag)

        if tag_id is None:
            data_manager.add_new_tag(tag)
            tag_id = data_manager.get_tag_id(tag)

        data_manager.add_question_tag(question_id, dict(tag_id)["id"])
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=question_id,
            )
        )
        
    return render_template(
        "add_tag.html",
        question_id=question_id,
        tags=data_manager.get_tags(),
    )


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_question_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=question_id,
        )
    )


@app.route("/registration", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user_credentials = data_manager.select_user(username)
        if not username or not password or not email:
            msg = 'Please fill out the form!'
        elif user_credentials:
            msg = 'Account already exists!'
        elif re.match(r"^[A-Za-z\d]$", username):
            msg = 'Username must contain only characters and numbers!'
        else:
            password = hash_pass.hash_password(password)
            data_manager.insert_user_credentials(username, email, password)
            latest_questions = data_manager.get_latest_questions()
            return render_template('latest_questions.html', questions=latest_questions)
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template(
        "registration.html", msg=msg
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' \
            and 'username' in request.form \
            and 'password' in request.form \
            and hash_pass.verify_password(request.form['password'],
                                          dict(data_manager.select_user(request.form['username']))['password']):
        user_credentials = data_manager.select_user(request.form['username'])
        if user_credentials:
            session['loggedin'] = True
            session['id'] = user_credentials['user_id']
            session['username'] = user_credentials['username']
            latest_questions = data_manager.get_latest_questions()
            return render_template('latest_questions.html', questions=latest_questions)
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/users')
def list_users():
    list_of_users = data_manager.get_user_details_without_id()
    number_of_questions = data_manager.get_number_of_questions_by_user_id(session['id'])
    number_of_answers = data_manager.get_number_of_answers_by_user_id(session['id'])
    number_of_comments = data_manager.get_number_of_comments_by_user_id(session['id'])
    return render_template('list_of_users.html',
                           users=list_of_users,
                           number_of_questions=number_of_questions,
                           number_of_answers=number_of_answers,
                           number_of_comments=number_of_comments,)


@app.route('/user/<user_id>')
def user_page(user_id):
    user_details= data_manager.get_user_details_with_id()
    number_of_questions = data_manager.get_number_of_questions_by_user_id(user_id)
    number_of_answers = data_manager.get_number_of_answers_by_user_id(user_id)
    number_of_comments = data_manager.get_number_of_comments_by_user_id(user_id)
    questions_of_user = data_manager.get_questions_by_user_id(user_id)
    answers_of_user = data_manager.get_answers_by_user_id(user_id)
    comments_of_user = data_manager.get_comments_by_user_id(user_id)
    return render_template('user_page.html', user_details=user_details,
                           number_of_questions=number_of_questions,
                           number_of_answers=number_of_answers,
                           number_of_comments=number_of_comments,
                           questions_of_user=questions_of_user,
                           answers_of_user=answers_of_user,
                           comments_of_user=comments_of_user,)


@app.route('/accept_answer/<question_id>/<answer_id>')
def get_accepted_answer(question_id, answer_id):
    data_manager.cancel_other_accepted_answer(question_id)
    data_manager.accept_answer(answer_id)
    return redirect(url_for('display_question_by_id', question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)

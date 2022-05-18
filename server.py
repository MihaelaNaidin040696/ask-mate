from flask import Flask, render_template, request, url_for, redirect
import data_manager
import os

app = Flask(__name__)

UPLOAD_FOLDER = (
    os.getenv("UPLOAD_FOLDER") if "UPLOAD_FOLDER" in os.environ else "images"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
@app.route("/list")
def display_questions():
    criteria = request.args.get("order_by", "submission_time")
    direction = request.args.get("order_direction", "desc")
    sorted_questions = data_manager.sort_questions(criteria, direction)
    return render_template(
        "list_of_questions.html",
        questions=sorted_questions,
    )


@app.route("/question/<question_id>", methods=["GET", "POST"])
def display_question_by_id(question_id):
    if request.method == "POST":
        print(15)
        print(question_id)
        return redirect(
            "{{ url_for('display_question_by_id', question_id=question_id) }}"
        )
    question = data_manager.get_question_by_id(question_id)
    answers = data_manager.get_answers_by_question_id(question_id)
    question_comment = data_manager.get_question_comments(question_id)
    return render_template(
        "individual_question.html",
        question=question,
        answers=answers,
        question_id=question_id,
        question_comment=question_comment,
    )


@app.route("/add-question", methods=["GET", "POST"])
def add_new_question():
    if request.method == "POST":
        image = ""
        file = request.files["image"]
        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            image = file.filename
        data_manager.write_question(
            request.form.get("title").capitalize(),
            request.form.get("message").capitalize(),
            image,
        )
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=id,
            )
        )
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_new_answer(question_id):
    if request.method == "POST":
        file = request.files["image"]
        image = ""
        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            image = file.filename
        data_manager.write_answer(
            question_id, request.form.get("message").capitalize(), image
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
    data_manager.delete_question(question_id)
    return redirect(
        url_for(
            "display_questions",
            question_id=question_id,
        )
    )


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answers(answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=id,
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


@app.route("/question/<question_id>/vote-up")
def vote_up_question(question_id):
    data_manager.vote_up_question(question_id)
    return redirect(url_for("display_questions"))


@app.route("/question/<question_id>/vote-down")
def vote_down_question(question_id):
    data_manager.vote_down_question(question_id)
    return redirect(url_for("display_questions"))


@app.route("/answer/<answer_id>/vote-up")
def vote_up_answer(answer_id):
    answer_id = int(answer_id)
    data_manager.vote_up_answer(answer_id)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=dict(data_manager.get_answers_by_answer_id(answer_id))[
                "question_id"
            ],
        )
    )


@app.route("/answer/<answer_id>/vote-down")
def vote_down_answer(answer_id):
    answer_id = int(answer_id)
    data_manager.vote_down_answer(answer_id)
    return redirect(
        url_for(
            "display_question_by_id",
            question_id=dict(data_manager.get_answers_by_answer_id(answer_id))[
                "question_id"
            ],
        )
    )


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment(question_id):
    if request.method == "POST":
        data_manager.add_question_comment(question_id, request.form.get("message"))
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
    if request.method == "POST":
        answer_comment = data_manager.add_answer_comment(answer_id)
        data_manager.add_answer_comment(answer_id, request.form.get("message"))
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=dict(data_manager.get_answers_by_answer_id(answer_id))[
                    "question_id"
                ],
                answer_comment=answer_comment,
            )
        )
    return render_template(
        "add_question_comment.html",
        answer_id=answer_id,
    )


@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    answer = data_manager.get_answers_by_answer_id(answer_id)
    if request.method == "POST":
        message = request.form.get("message")
        data_manager.edit_answer(answer_id, message)
        return redirect(
            url_for(
                "display_question_by_id",
                question_id=id,
            )
        )
    return render_template(
        "edit_answer.html",
        answer=answer,
        answer_id=answer_id,
    )


@app.route("/comment/<comment_id>/edit")
def edit_comment():
    pass


@app.route("/comments/<comment_id>/delete")
def delete_comment():
    pass


@app.route("/question/<question_id>/new-tag")
def add_question_tag():
    pass


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_question_tag():
    pass


if __name__ == "__main__":
    app.run(debug=True)

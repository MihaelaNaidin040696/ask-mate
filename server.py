from flask import Flask, render_template

import data_manager

app = Flask(__name__)


@app.route("/list")
def display_questions():
    questions= data_manager.list_questions()
    return render_template('list.html', questions=questions)

if __name__ == "__main__":
    app.run()

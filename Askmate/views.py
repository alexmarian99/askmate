"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, url_for, request, send_file, session
from Askmate import app
from Askmate import data_handler
import os

app.secret_key = "$2b$12$yxOGxF593XCL.wWfL3xrLbu"

app.config["UPLOAD_FOLDER"] = "Askmate/images"

@app.route("/question/<question_id>/add-coment", methods=["POST"])
def add_question_comment(question_id):
    data_handler.add_comment(question_id, request.form["message"], session["username"][0])
    return redirect(url_for("view_question", question_id=question_id))

@app.route("/question/<question_id>/<answer_id>/add-comment", methods=["POST"])
def add_answer_comment(question_id, answer_id):
    data_handler.add_comment(answer_id, request.form["message"], session["username"][0], "answer")
    return redirect(url_for("view_question", question_id=question_id))

@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        data_handler.add_user(request.form["username"], request.form["password"])
        return redirect(url_for("login"))

    return render_template(
        "register.html",
        title="Register",
        year=datetime.now().year,
    )

@app.route("/users")
def list_users():
    return render_template(
        "users.html",
        title="List users",
        year=datetime.now().year,
        user_data=data_handler.get_user_data()
    )


@app.route("/tags")
def list_tags():
    return render_template(
        "tags.html",
        title="List tags",
        year=datetime.now().year,
        tags=data_handler.get_tags()
    )


@app.route("/user/<user_id>")
def user(user_id):
    return render_template(
        "user_page.html",
        title="User page",
        user = data_handler.get_details_user(user_id),
        year=datetime.now().year,
        questions = data_handler.get_questions_user(user_id),
        comments = data_handler.get_comments(user_id, type="user"),
        answers = data_handler.get_answers_user(user_id)
    )

@app.route("/user/<user_id>/delete")
def delete_user(user_id):
    if session["username"][2] == True:
        data_handler.delete_user(user_id)
        return redirect(url_for("list_user"))
    return redirect(url_for("home"))

@app.route("/question/<question_id>/delete-tag/<tag_name>")
def delete_question_tag(question_id, tag_name):
    tags = data_handler.get_tags()
    for tag in tags:
        if tag["name"] == tag_name:
            data_handler.delete_question_tag(question_id, tag["id"])
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = "Username or password wrong, Try again!"

    if request.method == "POST":
        login = data_handler.login(request.form["username"], request.form["password"])

        if len(login) != 0:
            session["username"] = [login[0]["id"], login[0]["username"], login[0]["administrator"]]
            return redirect(url_for("home"))

        return render_template(
            "login.html",
            title="Login",
            year=datetime.now().year,
            error_message=error_message,
        )

    return render_template(
        "login.html",
        title="Login",
        year=datetime.now().year,
    )


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/tag/add-tag", methods=["POST"])
def add_tag():
    data_handler.add_tag(request.form["name"])
    return redirect(url_for("list_tags"))

@app.route("/<question_id>/add-tag", methods=["POST"])
def add_question_tag(question_id):
    data_handler.add_question_tag(question_id, request.form["tag"])
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/")
@app.route("/home")
def home():
    order = request.args.get("order", "submission_time")
    direction = request.args.get("direction", "DESC")

    return render_template(
        "index.html",
        title="Home Page",
        year=datetime.now().year,
        questions=data_handler.get_questions_home(order, direction, 5),
    )

def compute_arrows(ordering, order, direction):
    return "▼" if order==ordering and direction == "DESC" else "▲" if order == ordering and direction == "ASC" else ""

@app.route("/list")
def list():
    """Renders the contact page."""
    order = request.args.get("order", "submission_time")
    direction = request.args.get("direction", "DESC")
    keywords = request.args.get("keywords", "")
    questions=data_handler.get_questions(order, direction)
    toDelete = []
    if keywords != "":
        for question in questions:
            if keywords in question["title"] or keywords in (question["tags"] if question["tags"] != None else ""):
                continue
            toDelete.append(question)
        for question in toDelete:
            questions.remove(question)
        for question in questions:
            question["title"] = question["title"].replace(keywords, f"<a style='background-color:yellow;'>{keywords}</a>")
            if question["tags"] != None:
                question["tags"] = question["tags"].replace(keywords, f"<a style='background-color:yellow;'>{keywords}</a>")


    ordering = {
        "id": compute_arrows("id", order, direction),
        "title": compute_arrows("title", order, direction),
        "vote_number": compute_arrows("vote_number", order, direction),
        "view_number": compute_arrows("view_number", order, direction),
    }

    return render_template(
        "list.html",
        title="Questions",
        year=datetime.now().year,
        order=order,
        direction=direction,
        questions=questions,
        ordering=ordering
    )

@app.route("/bonus-questions-list")
def list_bonus_questions():
    """Renders the contact page."""
    order = request.args.get("order", "submission_time")
    direction = request.args.get("direction", "DESC")
    keywords = request.args.get("keywords", "")
    questions=data_handler.get_bonus_questions(order, direction)
    toDelete = []
    if keywords != "":
        for question in questions:
            if keywords in question["title"] or keywords in (question["tags"] if question["tags"] != None else ""):
                continue
            toDelete.append(question)
        for question in toDelete:
            questions.remove(question)
        for question in questions:
            question["title"] = question["title"].replace(keywords, f"<a style='background-color:yellow;'>{keywords}</a>")
            if question["tags"] != None:
                question["tags"] = question["tags"].replace(keywords, f"<a style='background-color:yellow;'>{keywords}</a>")


    ordering = {
        "id": compute_arrows("id", order, direction),
        "title": compute_arrows("title", order, direction),
        "vote_number": compute_arrows("vote_number", order, direction),
        "view_number": compute_arrows("view_number", order, direction),
    }

    return render_template(
        "bonus-questions-list.html",
        title="Bonus Questions",
        year=datetime.now().year,
        order=order,
        direction=direction,
        questions=questions,
        ordering=ordering
    )


@app.route("/add-question", methods=["POST", "GET"])
def add_question():
    """Renders the about page."""
    if request.method == "POST":
        id = data_handler.add_question(request.form["title"],request.form["message"],session["username"][0])
        if "image" in request.files:
            image_file = request.files["image"]
            if image_file.filename != '':
                image_file.save(os.path.join(app.config["UPLOAD_FOLDER"],f"question{id}.jpg"))
                data_handler.set_image_question(id)
        return redirect(url_for("view_question", question_id=id))

    return render_template(
       "add_question.html",
        title="Ask a question",
        year=datetime.now().year,
    )


@app.route("/question/<int:question_id>/edit", methods=["POST", "GET"])
def edit_question(question_id):
    """Renders the about page."""
    if request.method == "POST":
        data_handler.update_question(
            question_id,
            request.form["title"],
            request.form["message"],
        )
        return redirect(url_for("view_question", question_id=question_id))

    return render_template(
        "edit_question.html",
        title="Ask a question",
        year=datetime.now().year,
        question=data_handler.get_question(question_id),
        question_id=question_id,
    )


@app.route("/images/question/<int:question_id>")
def image_question(question_id):
    question = data_handler.get_question(question_id)
    try:
        return send_file(os.path.join(question["image"]), mimetype="image/jpg")
    except:
        return None


@app.route("/answer/<int:answer_id>/delete")
def delete_answer(answer_id):
    question_id = data_handler.delete_answer(answer_id)
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/answer/<int:answer_id>/vote/<int:up>")
def vote_answer(answer_id, up):
    question_id = data_handler.vote_answer(answer_id, up)
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/question/<int:question_id>/vote/<int:up>")
def vote_question(question_id, up):
    data_handler.vote_question(question_id, up)
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/question/<int:question_id>")
def view_question(question_id):
    data_handler.add_view(question_id)
    answers = data_handler.get_answers(question_id)
    comments = []
    comments.append(data_handler.get_comments(question_id))
    for answer in answers:
        comments.append(data_handler.get_comments(answer["id"], "answer"))
    return render_template(
        "view_question.html",
        title=f"Question {question_id}",
        year=datetime.now().year,
        question_data=data_handler.get_question(question_id),
        answers_data=answers,
        comments_data=comments,
        tags = data_handler.get_tags()
    )


@app.route("/question/<int:question_id>/new-answer", methods=["POST"])
def add_answer(question_id):
    if request.method == "POST":
        data_handler.add_answer(
            question_id,
            request.form["message"],
            session["username"][0]
        )
    return redirect(url_for("view_question", question_id=question_id))


@app.route("/question/<int:question_id>/delete")
def delete_question(question_id):
    data_handler.delete_question(question_id)
    return redirect(url_for("list"))


@app.route("/question/<int:question_id>/<int:answer_id>/bow/<bow_value>")
def add_bow_to_answer(question_id,answer_id, bow_value):
    if bow_value == False:
        bow_value = True
    data_handler.set_bow(answer_id, bow_value)
    return redirect(url_for("view_question", question_id=question_id))

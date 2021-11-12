from psycopg2.extras import RealDictCursor
import database_connection

@database_connection.connection_handler
def get_comments(cursor, id, type="question"):
    cursor.execute(f"SELECT comment.id, comment.message, comment.submission_time, comment.edited_count, users.username FROM comment INNER JOIN users ON comment.user_id = users.id WHERE {type}_id = %(id)s;",
                   {
                       "id": id
                       })
    return cursor.fetchall()

@database_connection.connection_handler
def set_bow(cursor, answer_id, bow_value):
    # bow_value is true or false
    cursor.execute("UPDATE answer SET bow=%(bow_value)s WHERE id=%(answer_id)s;",
    {"answer_id": answer_id, "bow_value": bow_value})

@database_connection.connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    # bow_value is true or false
    cursor.execute("DELETE FROM question_tag WHERE question_id=%(question_id)s AND tag_id=%(tag_id)s;",
    {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def get_tags(cursor):
    cursor.execute("SELECT tag.id, tag.name ,(SELECT COUNT(*) FROM question_tag WHERE question_tag.tag_id = tag.id) AS number_of_questions FROM tag;")
    return cursor.fetchall()

@database_connection.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    cursor.execute("INSERT INTO question_tag(question_id, tag_id) VALUES(%(question_id)s, %(tag_id)s);", {"question_id" : question_id, "tag_id" : tag_id})


@database_connection.connection_handler
def get_details_user(cursor, user_id):
    cursor.execute("""SELECT users.id, users.username, users.registered , users.administrator,
    (SELECT COUNT(*) FROM question WHERE question.user_id = users.id) as question_count, 
    (SELECT COUNT(*) FROM answer WHERE answer.user_id = users.id) as answer_count, 
    (SELECT COUNT(*) FROM comment WHERE comment.user_id = users.id) as comment_count,
    (SELECT SUM(question.vote_number) FROM question WHERE question.user_id = users.id) * 5 + (SELECT SUM(answer.vote_number) 
    FROM answer WHERE answer.user_id = users.id) * 10 as reputation FROM users WHERE users.id=%(user_id)s;""",
                  {
                      "user_id":user_id,
                  })
    return cursor.fetchone()


@database_connection.connection_handler
def get_user_data(cursor):
    cursor.execute("""SELECT users.id, users.username, users.registered ,
    (SELECT COUNT(*) FROM question WHERE question.user_id = users.id) as question_count, 
    (SELECT COUNT(*) FROM answer WHERE answer.user_id = users.id) as answer_count, 
    (SELECT COUNT(*) FROM comment WHERE comment.user_id = users.id) as comment_count,
    (SELECT SUM(question.vote_number) FROM question WHERE question.user_id = users.id) * 5 + (SELECT SUM(answer.vote_number) 
    FROM answer WHERE answer.user_id = users.id) * 10 as reputation FROM users;""",
                  )
    return cursor.fetchall()


@database_connection.connection_handler
def add_comment(cursor, id, message, user_id, type="question"):
    cursor.execute(f"INSERT INTO comment({type}_id, message, user_id) VALUES(%(id)s, %(message)s, %(user_id)s);",
                   {
                       "id": id,
                       "message": message,
                       "user_id": user_id
                       })


@database_connection.connection_handler
def get_user(cursor, user_id):
    cursor.execute("""SELECT * FROM users WHERE user_id=%(user_id)s;""")
    return cursor.fetchall()

@database_connection.connection_handler
def add_tag(cursor, name):
    cursor.execute("""INSERT INTO tag(name) VALUES(%(name)s);""", { "name": name })


@database_connection.connection_handler
def get_questions(cursor, order, direction):
    cursor.execute(f"SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username, string_agg(CAST(tags.name as TEXT), ',') AS tags FROM question INNER JOIN users ON users.id = question.user_id FULL JOIN (SELECT question_tag.question_id, tag.name FROM question_tag INNER JOIN tag ON question_tag.tag_id = tag.id) as tags ON tags.question_id = question.id WHERE question.bonus_question = False GROUP BY question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username ORDER BY {order} {direction};")
    return cursor.fetchall()

@database_connection.connection_handler
def get_bonus_questions(cursor, order, direction):
    cursor.execute(f"SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username, string_agg(CAST(tags.name as TEXT), ',') AS tags FROM question INNER JOIN users ON users.id = question.user_id FULL JOIN (SELECT question_tag.question_id, tag.name FROM question_tag INNER JOIN tag ON question_tag.tag_id = tag.id) as tags ON tags.question_id = question.id WHERE question.bonus_question = True GROUP BY question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username ORDER BY {order} {direction};")
    return cursor.fetchall()


@database_connection.connection_handler
def get_questions_home(cursor, order, direction, limit=5):
    cursor.execute(f"SELECT * FROM question WHERE bonus_question=False ORDER BY {order} {direction} LIMIT {limit};")
    return cursor.fetchall()


@database_connection.connection_handler
def get_question(cursor, question_id):
    cursor.execute(
        "SELECT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username, string_agg(CAST(tags.name as TEXT), ',') AS tags FROM question INNER JOIN users ON users.id = question.user_id FULL JOIN (SELECT question_tag.question_id, tag.name FROM question_tag INNER JOIN tag ON question_tag.tag_id = tag.id) as tags ON tags.question_id = question.id WHERE question.id = %(id)s GROUP BY question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image, question.user_id, users.username",
        {
            "id": question_id,
        },
    )
    return cursor.fetchone()


@database_connection.connection_handler
def add_view(cursor, question_id):
    cursor.execute(
        "UPDATE question SET view_number = view_number + 1 WHERE id=%(question_id)s;",
        {"question_id": question_id},
    )


@database_connection.connection_handler
def vote_question(cursor, question_id, up=True):
    vote = 1 if up else -1
    cursor.execute(
        "UPDATE question SET vote_number = vote_number + %(vote)s WHERE id=%(question_id)s;",
        {"vote": vote, "question_id": question_id},
    )


@database_connection.connection_handler
def vote_answer(cursor, answer_id, up=True):
    vote = 1 if up else -1
    cursor.execute(
        """UPDATE answer
            SET vote_number = vote_number + %(vote)s
            WHERE id=%(answer_id)s;
        SELECT question.id
        FROM question
        INNER JOIN answer
        ON question.id = answer.question_id
        WHERE answer.id = %(answer_id)s;""",
        {
            "vote": vote,
            "answer_id": answer_id,
        },
    )
    return cursor.fetchone()["id"]


@database_connection.connection_handler
def vote_question(cursor, question_id, up=True):
    vote = 1 if up else -1
    cursor.execute(
        "UPDATE question SET vote_number = vote_number + %(vote)s WHERE id=%(question_id)s;",
        {
            "vote": vote,
            "question_id": question_id,
        },
    )


@database_connection.connection_handler
def get_answers(cursor, question_id):
    cursor.execute(
        "SELECT answer.id, answer.submission_time, answer.vote_number, answer.question_id, answer.message, users.username, answer.bow FROM answer INNER JOIN users ON answer.user_id = users.id WHERE question_id=%(question_id)s ORDER BY answer.bow DESC, answer.submission_time DESC;",
        {"question_id": question_id},
    )
    return cursor.fetchall()


@database_connection.connection_handler
def get_answers_user(cursor, user_id):
    cursor.execute(
        "SELECT * FROM answer WHERE user_id=%(user_id)s;",
        {"user_id": user_id},
    )
    return cursor.fetchall()


@database_connection.connection_handler
def get_questions_user(cursor, user_id):
    cursor.execute(
        "SELECT * FROM question WHERE user_id=%(user_id)s;",
        {"user_id": user_id},
    )
    return cursor.fetchall()


@database_connection.connection_handler
def add_question(cursor, title, message, user_id):
    cursor.execute(
        "INSERT INTO question(title, message, user_id) VALUES(%(title)s, %(message)s, %(user_id)s) RETURNING id;",
        {
            "title": title,
            "message": message,
            "user_id": user_id,
        },
    )
    return cursor.fetchone()["id"]


@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute(
        "DELETE FROM answer WHERE id=%(answer_id)s RETURNING question_id;",
        {"answer_id": answer_id},
    )
    return cursor.fetchone()["question_id"]


@database_connection.connection_handler
def update_question(cursor, question_id, title, message):
    cursor.execute(
        "UPDATE question SET title=%(title)s, message=%(message)s WHERE id=%(question_id)s;",
        {
            "title": title,
            "message": message,
            "question_id": question_id,
        },
    )


@database_connection.connection_handler
def set_image_question(cursor, question_id):
    cursor.execute(
        "UPDATE question SET image=%(image)s WHERE id=%(question_id)s;",
        {"image": f"images/question{question_id}.jpg", "question_id": question_id},
    )


@database_connection.connection_handler
def add_answer(cursor, question_id, message, user_id):
    cursor.execute(
        "INSERT INTO answer(question_id, message, user_id) VALUES(%(question_id)s, %(message)s, %(user_id)s);",
        {"question_id": question_id, "message": message, "user_id": user_id},
    )


@database_connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute(
        "DELETE FROM question WHERE id=%(question_id)s;",
        {"question_id": question_id},
    )


@database_connection.connection_handler
def delete_user(cursor, user_id):
    cursor.execute(
        "DELETE FROM users WHERE id=%(user_id)s;",
        {"user_id": user_id},
    )


@database_connection.connection_handler
def add_user(cursor, username, password):
    cursor.execute(
        "INSERT INTO users(username, password) VALUES(%(username)s, sha256(%(password)s));",
        {"username": username, "password": password},
    )


@database_connection.connection_handler
def login(cursor, username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=%(username)s AND password=sha256(%(password)s);",
        {"username": username, "password": password},
    )
    return cursor.fetchall()

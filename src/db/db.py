import mysql.connector


def get_db_connection():
    db = mysql.connector.connect(
        user="admin",
        password="password",
        host="127.0.0.1",
        port="3308",
        database="libreria",
        charset="utf8",
        collation="utf8_general_ci",
        use_unicode=True,
    )
    return db

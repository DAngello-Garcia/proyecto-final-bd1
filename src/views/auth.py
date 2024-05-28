import bcrypt
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

auth = Blueprint("auth", __name__)

ciudades: list[str] = []
id_ciudades: list[str] = []


def cargar_ciudades():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""SELECT idCiudad, nombre FROM Ciudad""")
    ciudades_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, ciudad in ciudades_cursor:
        id_ciudades.append(valor)
        ciudades.append(ciudad)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        query = """SELECT idCliente, password FROM Cliente WHERE email = %s"""
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result:
            hashed_password = result[1].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                session["email"] = email
                session["cliente"] = result[0]
                return redirect(url_for("index"))
            else:
                return render_template(
                    "cliente/login.html", error="Contraseña incorrecta"
                )
        else:
            return render_template("cliente/login.html", error="Usuario no encontrado")
    else:
        return render_template("cliente/login.html")


@auth.route("/login-empleado", methods=["GET", "POST"])
def login_empleado():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        query = """SELECT password, idEmpleado FROM Empleado WHERE email = %s"""
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        cursor.close()
        db.close()

        if result:
            hashed_password = result[0].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                session["email"] = email
                session["empleado"] = result[1]
                return redirect(url_for("index"))
            else:
                return render_template(
                    "empleado/login-empleado.html", error="Contraseña incorrecta"
                )
        else:
            return render_template(
                "empleado/login-empleado.html", error="Usuario no encontrado"
            )
    else:
        return render_template("empleado/login-empleado.html")


@auth.route("/logout")
def logout():
    session.pop("email", None)
    session["cliente"] = 1
    session["empleado"] = 1
    if session["cliente"] is not None:
        session.pop("cliente", None)
    if session["empleado"] is not None:
        session.pop("empleado", None)
    ciudades = []
    id_ciudades = []
    return redirect(url_for("index"))


@auth.route("/registro", methods=["GET", "POST"])
def registro():
    cargar_ciudades()
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        fecha_nacimiento = request.form["fecha_nacimiento"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        id_ciudad = request.form["id_ciudad"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        query = """INSERT INTO Cliente (nombre, apellido, fecha_nacimiento, direccion, telefono, id_ciudad, username, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (
            nombre,
            apellido,
            fecha_nacimiento,
            direccion,
            telefono,
            id_ciudad,
            username,
            email,
            hashed_password.decode("utf-8"),
        )
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("auth.login"))
    else:
        select_options = "".join(
            f'<option value="{value}">{label}</option>'
            for label, value in zip(ciudades, id_ciudades)
        )

        return render_template("cliente/registro.html", ciudades=select_options)

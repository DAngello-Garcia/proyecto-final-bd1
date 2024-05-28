import bcrypt
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

autor = Blueprint("autor", __name__)

paises: list[str] = []
id_paises: list[str] = []
autores: list[str] = []
id_autores: list[str] = []


@autor.route("/crear-autor", methods=["POST"])
def crear():
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    if request.form["fecha_defuncion"] is not "":
        fecha_defuncion = request.form["fecha_defuncion"]
        query = """INSERT INTO Autor (nombre, apellido, fecha_nacimiento, fecha_defuncion, biografia, id_pais) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (
            nombre,
            apellido,
            fecha_nacimiento,
            fecha_defuncion,
            biografia,
            id_pais,
        )
    biografia = request.form["biografia"]
    id_pais = request.form["id_pais"]

    query = """INSERT INTO Autor (nombre, apellido, fecha_nacimiento, biografia, id_pais) VALUES (%s, %s, %s, %s, %s)"""
    values = (
        nombre,
        apellido,
        fecha_nacimiento,
        biografia,
        id_pais,
    )
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("autor.gestion"))


@autor.route("/gestion-autores", methods=["GET"])
def gestion():
    cargar_paises()
    autores = cargar_autores()
    paises_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(paises, id_paises)
    )

    return render_template("autor/gestion.html", autores=autores, paises=paises_options)


@autor.route("/gestion_autor/<autor_id>", methods=["GET", "POST"])
def gestion_autor(autor_id: int):
    db = get_db_connection()
    paises.clear()
    id_paises.clear()
    autores.clear()
    id_autores.clear()
    cargar_paises()
    paises_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(paises, id_paises)
    )

    cursor = db.cursor(buffered=True)
    query = """SELECT a.idAutor, a.nombre, a.apellido, a.fecha_nacimiento, a.fecha_defuncion, a.biografia, p.nombre FROM Autor a JOIN Pais p ON a.id_pais = p.idPais WHERE idAutor = %s"""
    values = (autor_id,)
    cursor.execute(query, values)
    autor = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template(
        "autor/gestion-autor.html",
        autor=autor,
        paises=paises_options,
    )


@autor.route("/actualizar-autor/<id_autor>", methods=["POST"])
def actualizar(id_autor: int):
    db = get_db_connection()
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    fecha_defuncion = request.form["fecha_defuncion"]
    biografia = request.form["biografia"]
    id_pais = request.form["id_pais"]

    query = """UPDATE Autor SET nombre = %s, apellido = %s, fecha_nacimiento = %s, fecha_defuncion = %s, biografia = %s, id_pais = %s WHERE idAutor = %s"""
    values = (
        nombre,
        apellido,
        fecha_nacimiento,
        fecha_defuncion,
        biografia,
        id_pais,
        id_autor,
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()
    return redirect(url_for("autor.gestion_autor", autor_id=id_autor))


@autor.route("/eliminar-autor/<id_autor>", methods=["POST"])
def eliminar(id_autor: int):
    query = """DELETE FROM AutorLibro WHERE id_autor = %s"""
    values = (id_autor,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """DELETE FROM Autor WHERE idAutor = %s"""
    values = (id_autor,)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("autor.gestion"))


def cargar_paises():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""SELECT idPais, nombre FROM Pais""")
    paises_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, pais in paises_cursor:
        id_paises.append(valor)
        paises.append(pais)


def cargar_autores():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""SELECT idAutor, nombre, biografia, apellido FROM Autor""")
    autores_cursor = cursor.fetchall()
    cursor.close()
    db.close()
    return autores_cursor

from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

genero = Blueprint("genero", __name__)


@genero.route("/crear_genero", methods=["POST"])
def crear_genero():
    db = get_db_connection()
    nombre = request.form["nombre"]
    query = """INSERT INTO Genero (nombre) VALUES (%s)"""
    values = (nombre,)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("genero.gestion"))


@genero.route("/actualizar-genero/<id_genero>", methods=["POST"])
def actualizar(id_genero: int):
    db = get_db_connection()
    nombre = request.form["nombre"]

    query = """UPDATE Genero SET nombre = %s WHERE idGenero = %s"""
    values = (
        nombre,
        id_genero,
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()
    return redirect(url_for("genero.gestion_genero", genero_id=id_genero))


@genero.route("/gestion_genero/<genero_id>")
def gestion_genero(genero_id: int):
    db = get_db_connection()

    cursor = db.cursor(buffered=True)
    query = """SELECT idGenero, nombre FROM Genero WHERE idGenero = %s"""
    values = (genero_id,)
    cursor.execute(query, values)
    genero = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template(
        "genero/gestion-genero.html",
        genero=genero,
    )


@genero.route("/eliminar-genero/<id_genero>", methods=["POST"])
def eliminar(id_genero: int):
    query = """DELETE FROM Genero WHERE idGenero = %s"""
    values = (id_genero,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("genero.gestion"))


@genero.route("/gestion-genero")
def gestion():
    generos = cargar_todos_generos()
    return render_template(
        "genero/gestion.html",
        generos=generos,
    )


def cargar_todos_generos():
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT idGenero, nombre FROM Genero""")
    generos_cursor = cursor.fetchall()
    cursor.close()
    db.close()
    return generos_cursor

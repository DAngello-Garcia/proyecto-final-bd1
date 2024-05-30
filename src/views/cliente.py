import bcrypt
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

cliente = Blueprint("cliente", __name__)

ciudades: list[str] = []
id_ciudades: list[str] = []


def cargar_ciudades() -> list[str]:
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""SELECT idCiudad, nombre FROM Ciudad""")
    ciudades_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, ciudad in ciudades_cursor:
        id_ciudades.append(valor)
        ciudades.append(ciudad)


@cliente.route("/perfil/<id_cliente>")
def perfil(id_cliente: int):
    cargar_ciudades()
    db = get_db_connection()
    cursor = db.cursor()
    query = """SELECT nombre, apellido, fecha_nacimiento, direccion,
        telefono, id_ciudad, username, email, idCliente
        FROM Cliente WHERE idCliente = %s"""
    values = (id_cliente,)
    cursor.execute(query, values)
    cliente = cursor.fetchone()
    ciudad = cliente[5]
    query = "SELECT idCiudad FROM Ciudad WHERE idCiudad = %s"
    values = (ciudad,)
    cursor.execute(query, values)
    ciudad = cursor.fetchone()
    cursor.close()
    db.close()
    cliente = list(cliente)
    ciudad_cliente = ciudad[0]
    ciudades_zip = zip(ciudades, id_ciudades)
    return render_template(
        "cliente/perfil.html",
        ciudades=ciudades_zip,
        ciudad_cliente=ciudad_cliente,
        cliente=cliente,
    )


@cliente.route("/editar-cliente/<id_cliente>", methods=["POST"])
def editar(id_cliente: int):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    id_ciudad = request.form["id_ciudad"]
    username = request.form["username"]
    email = request.form["email"]

    query = """UPDATE Cliente
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, direccion = %s,
            telefono = %s, id_ciudad = %s, username = %s, email = %s
            WHERE idCliente = %s"""
    values = (
        nombre,
        apellido,
        fecha_nacimiento,
        direccion,
        telefono,
        id_ciudad,
        username,
        email,
        id_cliente,
    )
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("cliente.perfil", id_cliente=id_cliente))


@cliente.route("/eliminar-cliente/<id_cliente>", methods=["POST"])
def eliminar(id_cliente: int):
    query = """DELETE FROM Cliente WHERE idCliente = %s"""
    values = (id_cliente,)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    session.pop("email", None)
    if session["cliente"]:
        session.pop("cliente", None)
    return redirect(url_for("auth.registro"))

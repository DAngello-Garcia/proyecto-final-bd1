import bcrypt
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

empleado = Blueprint("empleado", __name__)

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


@empleado.route("/perfil-empleado/<id_empleado>")
def perfil(id_empleado: int):
    cargar_ciudades()
    db = get_db_connection()
    cursor = db.cursor()
    query = """SELECT e.nombre, e.apellido, e.fecha_nacimiento, e.direccion, e.telefono,
        e.id_ciudad, e.username, e.email, e.idEmpleado, e.fecha_contratacion, s.nombre, c.nombre, c.salario
        FROM Empleado e JOIN Sucursal s ON e.id_sucursal = s.idSucursal
        JOIN Cargo c ON e.id_cargo = c.idCargo
        WHERE idEmpleado = %s"""
    values = (id_empleado,)
    cursor.execute(query, values)
    empleado = cursor.fetchone()
    ciudad = empleado[5]
    query = "SELECT idCiudad FROM Ciudad WHERE idCiudad = %s"
    values = (ciudad,)
    cursor.execute(query, values)
    ciudad = cursor.fetchone()
    cursor.close()
    db.close()
    empleado = list(empleado)
    ciudad_empleado = ciudad[0]
    ciudades_zip = zip(ciudades, id_ciudades)
    return render_template(
        "empleado/perfil.html",
        ciudades=ciudades_zip,
        ciudad_empleado=ciudad_empleado,
        empleado=empleado,
    )


@empleado.route("/editar-empleado/<id_empleado>", methods=["POST"])
def editar(id_empleado: int):
    nombre = request.form["nombre"]
    apellido = request.form["apellido"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    direccion = request.form["direccion"]
    telefono = request.form["telefono"]
    id_ciudad = request.form["id_ciudad"]
    username = request.form["username"]
    email = request.form["email"]

    query = """UPDATE Empleado
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, direccion = %s,
            telefono = %s, id_ciudad = %s, username = %s, email = %s
            WHERE idEmpleado = %s"""
    values = (
        nombre,
        apellido,
        fecha_nacimiento,
        direccion,
        telefono,
        id_ciudad,
        username,
        email,
        id_empleado,
    )
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("empleado.perfil", id_empleado=id_empleado))


@empleado.route("/eliminar-empleado/<id_empleado>", methods=["POST"])
def eliminar(id_empleado: int):

    query = """DELETE FROM Empleado WHERE idEmpleado = %s"""
    values = (id_empleado,)
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    session.pop("email", None)
    if session["empleado"]:
        session.pop("empleado", None)
    return redirect(url_for("index"))

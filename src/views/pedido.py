from datetime import datetime, timedelta

from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection
from views.libro import cargar_generos, cargar_libros

pedido = Blueprint("pedido", __name__)
libros: list[str] = []
generos: list[str] = []
estado_pedidos: list[str] = []
id_estado_pedidos: list[str] = []


@pedido.route("/pedir", methods=["POST"])
def pedir():
    id_libro = request.args.get("id_libro", type=int)
    id_cliente = request.args.get("id_cliente", type=int)
    id_cliente_str = str(id_cliente)
    if f"pedido_{id_cliente_str}" not in session:
        session[f"pedido_{id_cliente_str}"] = [id_libro]
    else:
        libros_pedido = session[f"pedido_{id_cliente_str}"]
        libros_pedido.append(id_libro)
        session[f"pedido_{id_cliente_str}"] = libros_pedido
    libros = cargar_libros()
    generos = cargar_generos()
    return render_template("inicio.html", libros=libros, generos=generos)


@pedido.route("/carro/<id_cliente>", methods=["GET", "POST"])
def carro(id_cliente: int):
    id_cliente_str = str(id_cliente)
    if f"pedido_{id_cliente_str}" in session:
        tupla_libros = tuple(
            session[f"pedido_{id_cliente_str}"],
        )
        db = get_db_connection()
        cursor = db.cursor(buffered=True)
        query = """SELECT l.idLibro, l.titulo, e.nombre, l.precio, l.cantidad_disponible,
            d.alto, d.ancho, d.largo, GROUP_CONCAT(g.nombre) AS generos, a.nombre, a.apellido
            FROM Libro l JOIN Editorial e ON l.id_editorial = e.idEditorial
            JOIN Dimensiones d ON l.id_dimensiones = d.idDimensiones
            JOIN LibroGenero lg ON l.idLibro = lg.id_libro
            JOIN Genero g ON lg.id_genero = g.idGenero
            JOIN AutorLibro al ON al.id_libro = l.idLibro
            JOIN Autor a ON al.id_autor = a.idAutor
            WHERE l.idLibro IN ({})
            GROUP BY l.idLibro, l.titulo, e.nombre, l.precio, l.cantidad_disponible, d.alto, d.ancho, d.largo, a.nombre, a.apellido""".format(
            ", ".join(["%s"] * len(tupla_libros))
        )
        cursor.execute(query, tupla_libros)
        libros = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("pedido/carro.html", libros=libros)
    else:
        return redirect(url_for("index"))


@pedido.route("/pagar/<id_cliente>", methods=["POST"])
def pagar(id_cliente: int):
    cantidades_actualizadas = {}
    id_metodoPago = int(request.form["metodo_pago"])
    db = get_db_connection()
    query = """INSERT INTO Pedido (id_cliente, fecha) VALUES (%s, %s)"""
    values = (id_cliente, datetime.now())
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    id_pedido = cursor.lastrowid

    for key, value in request.form.items():
        if key.startswith("cantidad_"):
            libro_id = key.split("_")[1]
            cantidad = int(value)
            cantidades_actualizadas[libro_id] = cantidad
            query = """SELECT precio FROM Libro WHERE idLibro = %s"""
            values = (libro_id,)
            cursor = db.cursor(buffered=True)
            cursor.execute(query, values)
            precio = cursor.fetchone()

            query = """INSERT INTO DetallePedido (id_pedido, id_libro, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"""
            subtotal = precio[0] * cantidad
            values = (id_pedido, libro_id, cantidad, precio[0], subtotal)
            cursor = db.cursor(buffered=True)
            cursor.execute(query, values)
            db.commit()

            query = """SELECT cantidad_disponible FROM Libro WHERE idLibro = %s"""
            values = (libro_id,)
            cursor = db.cursor(buffered=True)
            cursor.execute(query, values)
            cantidad_antes = cursor.fetchone()

            query = """UPDATE Libro SET cantidad_disponible = %s WHERE idLibro = %s"""
            nueva_cantidad = cantidad_antes[0] - cantidad
            values = (nueva_cantidad, libro_id)
            cursor = db.cursor(buffered=True)
            cursor.execute(query, values)
            db.commit()

    query = """INSERT INTO HistorialEstadoPedido (id_pedido, id_estado, fecha) VALUES (%s, %s, %s)"""
    values = (id_pedido, 1, datetime.now())
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """UPDATE Pedido
        SET total = (
            SELECT SUM(subtotal) FROM DetallePedido
            WHERE id_pedido = %s
            GROUP BY id_pedido
            )
        WHERE idPedido = %s"""
    values = (id_pedido, id_pedido)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """SELECT total
        FROM Pedido
        WHERE idPedido = %s"""
    values = (id_pedido,)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    total_pedido = cursor.fetchone()
    fechaEmision = datetime.now() + timedelta(minutes=10)
    fechaPago = fechaEmision

    query = """INSERT INTO Factura
        (id_pedido, id_cliente, fechaEmision, total, fechaPago, id_metodoPago)
        VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (
        id_pedido,
        id_cliente,
        fechaEmision,
        total_pedido[0],
        fechaPago,
        id_metodoPago,
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    borrar_pedido(id_cliente)

    return redirect(url_for("index"))


def borrar_pedido(id_cliente: int):
    id_cliente_str = str(id_cliente)
    session.pop(f"pedido_{id_cliente_str}", None)


@pedido.route("/lista-pedidos", methods=["GET"])
def listar_pedidos():
    db = get_db_connection()
    query = """SELECT p.idPedido, p.total, h.fecha, e.estado
        FROM Pedido p JOIN HistorialEstadoPedido h ON p.idPedido = h.id_pedido
        JOIN EstadoPedido e ON h.id_estado = e.idEstadoPedido
        JOIN (SELECT id_pedido, MAX(fecha) as max_fecha 
            FROM HistorialEstadoPedido 
            GROUP BY id_pedido)
            AS subquery ON h.id_pedido = subquery.id_pedido
            AND h.fecha = subquery.max_fecha"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    pedidos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("pedido/lista-pedidos.html", pedidos=pedidos)


@pedido.route("/gestion-pedido/<id_pedido>", methods=["GET"])
def gestion(id_pedido: int):
    estado_pedidos.clear()
    id_estado_pedidos.clear()
    cargar_estado_pedidos()

    db = get_db_connection()
    query = """SELECT p.idPedido, p.total, h.fecha, e.estado
        FROM Pedido p JOIN HistorialEstadoPedido h ON p.idPedido = h.id_pedido
        JOIN EstadoPedido e ON h.id_estado = e.idEstadoPedido
        WHERE p.idPedido = %s"""
    cursor = db.cursor(buffered=True)
    values = (id_pedido,)
    cursor.execute(query, values)
    pedido = cursor.fetchone()
    cursor.close()
    db.close()

    estado_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(estado_pedidos, id_estado_pedidos)
    )

    return render_template(
        "pedido/gestion.html", pedido=pedido, estado_pedido=estado_options
    )


@pedido.route("/actualizar_estado/<id_pedido>", methods=["GET"])
def actualizar_estado(id_pedido: int):
    id_estado = request.args.get("idEstadoPedido")
    db = get_db_connection()
    query = """INSERT INTO HistorialEstadoPedido
        (id_estado, fecha, id_pedido)
        VALUES (%s, %s, %s)"""
    cursor = db.cursor(buffered=True)
    values = (int(id_estado), str(datetime.now()), int(id_pedido))
    cursor.execute(query, values)
    db.commit()

    id_empleado = session["empleado"]

    query = """UPDATE Pedido
        SET id_empleado = %s
        WHERE idPedido = %s"""
    cursor = db.cursor(buffered=True)
    values = (int(id_empleado), int(id_pedido))
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("pedido.listar_pedidos"))


def cargar_estado_pedidos():
    db = get_db_connection()
    query = """SELECT idEstadoPedido, estado
        FROM EstadoPedido"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    estado_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, estado in estado_cursor:
        id_estado_pedidos.append(valor)
        estado_pedidos.append(estado)

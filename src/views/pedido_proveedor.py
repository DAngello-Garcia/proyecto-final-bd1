from datetime import datetime, timedelta

from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

pedido_proveedor = Blueprint("pedido_proveedor", __name__)
estado_pedidos: list[str] = []
id_estado_pedidos: list[str] = []


@pedido_proveedor.route("/pedido_proveedor/<libro_id>/<proveedor_id>", methods=["GET"])
def pedir(libro_id: int, proveedor_id: int):
    libro_id_str = session["empleado"]
    if f"pedido_proveedor_{libro_id_str}" not in session:
        session[f"pedido_proveedor_{libro_id_str}"] = [libro_id]
        session["proveedor"] = proveedor_id
    else:
        libros_pedido = session[f"pedido_proveedor_{libro_id_str}"]
        libros_pedido.append(libro_id)
        session[f"pedido_proveedor_{libro_id_str}"] = libros_pedido
    return redirect(
        url_for("pedido_proveedor.gestion_proveedor", proveedor_id=proveedor_id)
    )


@pedido_proveedor.route(
    "/carro-pedido_proveedor/<id_empleado>", methods=["GET", "POST"]
)
def carro(id_empleado: int):
    id_cliente_str = str(id_empleado)
    if f"pedido_proveedor_{id_cliente_str}" in session:
        tupla_libros = tuple(
            session[f"pedido_proveedor_{id_cliente_str}"],
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
        return render_template("pedidos_proveedor/carro.html", libros=libros)
    else:
        return redirect(url_for("pedido_proveedor.listar_pedidos"))


@pedido_proveedor.route("/pagar-pedido_proveedor/<id_empleado>", methods=["POST"])
def pagar(id_empleado: int):
    cantidades_actualizadas = {}
    id_metodoPago = int(request.form["metodo_pago"])
    db = get_db_connection()
    query = """SELECT id_sucursal FROM Empleado WHERE idEmpleado = %s"""
    values = (id_empleado,)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    id_sucursal = cursor.fetchone()

    query = """INSERT INTO PedidosProveedor (id_sucursal, fecha, id_proveedor, id_estado) VALUES (%s, %s, %s, %s)"""
    values = (id_sucursal[0], datetime.now(), int(session["proveedor"]), 1)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    id_pedido = cursor.lastrowid
    session.pop("proveedor", None)

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

            query = """INSERT INTO DetallePedidosProveedor (id_pedidoProveedor, id_libro, cantidad, precio_unitario, subtotal) VALUES (%s, %s, %s, %s, %s)"""
            subtotal = precio[0] * cantidad
            values = (id_pedido, libro_id, cantidad, float(precio[0]) * 0.7, subtotal)
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

    query = """UPDATE PedidosProveedor
        SET total = (
            SELECT SUM(subtotal) FROM DetallePedidosProveedor
            WHERE id_pedidoProveedor = %s
            GROUP BY id_pedidoProveedor
            )
        WHERE idPedidosProveedor = %s"""
    values = (id_pedido, id_pedido)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    borrar_pedido(id_empleado)

    return redirect(url_for("index"))


def borrar_pedido(id_empleado: int):
    id_cliente_str = str(id_empleado)
    session.pop(f"pedido_proveedor_{id_cliente_str}", None)


@pedido_proveedor.route("/lista-pedido_proveedor", methods=["GET"])
def listar_pedidos():
    db = get_db_connection()
    query = """SELECT p.idPedidosProveedor, p.total, p.fecha, e.estado, pro.nombre
        FROM PedidosProveedor p JOIN Proveedor pro ON p.id_proveedor = pro.idProveedor
        JOIN EstadoPedido e ON p.id_estado = e.idEstadoPedido"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    pedidos = cursor.fetchall()

    query = """SELECT idProveedor, nombre, telefono, email
        FROM Proveedor"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    proveedores = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template(
        "pedidos_proveedor/lista-pedidos.html", pedidos=pedidos, proveedores=proveedores
    )


@pedido_proveedor.route("/gestion_proveedor/<proveedor_id>", methods=["GET", "POST"])
def gestion_proveedor(proveedor_id: int):
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    query = """SELECT idProveedor, nombre, telefono, email
        FROM Proveedor
        WHERE idProveedor = %s"""
    values = (proveedor_id,)
    cursor.execute(query, values)
    proveedor = cursor.fetchone()

    query = """SELECT l.idLibro, l.titulo, l.precio, l.cantidad_disponible, e.nombre
        FROM Libro l JOIN Editorial e ON l.id_editorial = e.idEditorial
        JOIN LibroProveedor lp ON l.idLibro = lp.id_libro
        JOIN Proveedor p ON lp.id_proveedor = p.idProveedor
        WHERE idProveedor = %s"""
    values = (proveedor_id,)
    cursor.execute(query, values)
    libros = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template(
        "pedidos_proveedor/gestion.html", proveedor=proveedor, libros=libros
    )


@pedido_proveedor.route("/gestion-pedido_proveedor/<id_pedido>", methods=["GET"])
def gestion(id_pedido: int):
    estado_pedidos.clear()
    id_estado_pedidos.clear()
    cargar_estado_pedidos()

    db = get_db_connection()
    query = """SELECT p.idPedidosProveedor, p.total, p.fecha, e.estado
        FROM PedidosProveedor p JOIN EstadoPedido e ON p.id_estado = e.idEstadoPedido
        WHERE p.idPedidosProveedor = %s"""
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
        "pedidos_proveedor/gestion-pedido.html",
        pedido=pedido,
        estado_pedido=estado_options,
    )


@pedido_proveedor.route("/actualizar_pedido_proveedor/<id_pedido>", methods=["GET"])
def actualizar_estado(id_pedido: int):
    id_estado = request.args.get("idEstadoPedido")
    db = get_db_connection()

    query = """UPDATE PedidosProveedor
        SET id_estado = %s
        WHERE idPedidosProveedor = %s"""
    cursor = db.cursor(buffered=True)
    values = (int(id_estado), int(id_pedido))
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("pedido_proveedor.listar_pedidos"))


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

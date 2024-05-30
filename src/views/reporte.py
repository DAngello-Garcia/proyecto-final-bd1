import base64
from io import BytesIO

import matplotlib.pyplot as plt
import numpy as np
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

reporte = Blueprint("reporte", __name__)


@reporte.route("/reportes")
def lista():
    return render_template("reportes.html")


@reporte.route("/reportes-simple", methods=["GET", "POST"])
def simples():
    grafico_base64 = generar_grafico()
    reporte1 = ""
    reporte2 = ""
    reporte3 = ""
    div_visible = False
    div_visible2 = False
    div_visible3 = False
    if request.method == "POST":
        if request.args.get("rep1") is not None:
            reporte1 = simple_1()
            div_visible = True

        if request.args.get("rep2") is not None:
            fechaInicio = request.form["fechaInicio"]
            fechaFin = request.form["fechaFin"]
            reporte2 = simple_2(fechaInicio, fechaFin)
            div_visible2 = True

        if request.args.get("rep3") is not None:
            reporte3 = simple_3()
            div_visible3 = True

    return render_template(
        "reportes/simples.html",
        grafico_base64=grafico_base64,
        reporte1=reporte1,
        reporte2=reporte2,
        reporte3=reporte3,
        div_visible=div_visible,
        div_visible2=div_visible2,
        div_visible3=div_visible3,
    )


@reporte.route("/reportes-intermedio")
def intermedios():
    grafico_base64 = generar_grafico()
    reporte1 = ""
    if request.args.get("rep1") is not None:
        reporte1 = simple_1()
    return render_template(
        "reportes.html", grafico_base64=grafico_base64, reporte1=reporte1
    )


@reporte.route("/reportes-complejo")
def complejos():
    grafico_base64 = generar_grafico()
    reporte1 = ""
    if request.args.get("rep1") is not None:
        reporte1 = simple_1()
    return render_template(
        "reportes.html", grafico_base64=grafico_base64, reporte1=reporte1
    )


def generar_grafico():
    x = np.arange(0, 10, 0.1)
    y = np.sin(x)

    # Cambiar el backend de Matplotlib a 'Agg' (sin GUI)
    plt.switch_backend("agg")

    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gráfico de ejemplo")

    # Guardar el gráfico como un archivo de imagen en memoria
    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    # Codificar el gráfico en base64 para incrustarlo en la plantilla HTML
    img_base64 = base64.b64encode(img.getvalue()).decode()
    return img_base64


@reporte.route("/descargar_reporte_pdf")
def descargar_reporte_pdf():
    # Generar el gráfico
    grafico_base64 = generar_grafico()

    # Crear el gráfico nuevamente para guardarlo como PDF
    x = np.arange(0, 10, 0.1)
    y = np.sin(x)
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Gráfico de ejemplo")

    # Guardar el gráfico como un archivo PDF
    pdf_output = BytesIO()
    plt.savefig(pdf_output, format="pdf")
    pdf_output.seek(0)

    # Devolver el archivo PDF como una descarga
    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        attachment_filename="grafico.pdf",
    )


def simple_1():
    db = get_db_connection()
    query = """SELECT c.nombre, c.apellido, ci.nombre AS ciudad,
        d.nombre AS departamento, p.nombre AS pais,
        ROUND(DATEDIFF(CURRENT_DATE(), c.fecha_nacimiento) / 365, 1) AS edad
        FROM Cliente c JOIN Ciudad ci ON c.id_ciudad = ci.idCiudad 
        JOIN Departamento d ON ci.id_dpto = d.idDepartamento
        JOIN Pais p ON d.id_pais = p.idPais 
        ORDER BY c.fecha_nacimiento"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def simple_2(fecha1, fecha2):
    db = get_db_connection()
    query = """SELECT idPedido, total, fecha
        FROM Pedido
        WHERE fecha BETWEEN %s AND %s
        ORDER BY fecha"""
    cursor = db.cursor(buffered=True)
    values = (fecha1, fecha2)
    cursor.execute(query, values)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def simple_3():
    db = get_db_connection()
    query = """SELECT e.nombre, e.apellido, c.nombre AS cargo, c.salario 
        FROM Empleado e JOIN Cargo c ON e.id_cargo = c.idCargo"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def intermedia_1():
    db = get_db_connection()
    query = """SELECT g.nombre AS genero, SUM(dp.subtotal) AS ventas
        FROM Genero g JOIN LibroGenero lg ON g.idGenero = lg.id_genero
        JOIN Libro l ON lg.id_libro = l.idLibro
        JOIN DetallePedido dp ON l.idLibro = dp.id_libro
        GROUP BY g.nombre"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def intermedia_2():
    db = get_db_connection()
    query = """SELECT l.titulo AS libro, p.nombre AS proveedor, (l.precio - dp.precio_unitario) AS ganancia
        FROM Libro l JOIN LibroProveedor lp ON l.idLibro = lp.id_libro
        JOIN Proveedor p ON lp.id_proveedor = p.idProveedor
        JOIN DetallePedidosProveedor dp ON l.idLibro = dp.id_libro"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def intermedia_3():
    db = get_db_connection()
    query = """SELECT a.nombre, a.apellido, SUM(dp.subtotal) AS total_ventas
        FROM Autor a JOIN AutorLibro al ON a.idAutor = al.id_autor
        JOIN Libro l ON al.id_libro = l.idLibro
        JOIN DetallePedido dp ON l.idLibro = dp.id_libro
        GROUP BY a.idAutor
        ORDER BY total_ventas DESC"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def intermedia_4():
    db = get_db_connection()
    query = """SELECT ci.nombre AS ciudad, g.nombre AS genero, SUM(dp.subtotal) AS ventas
        FROM Ciudad ci JOIN Cliente c ON ci.idCiudad = c.id_ciudad
        JOIN Pedido p ON c.idCliente = p.id_cliente 
        JOIN DetallePedido dp ON p.idPedido = dp.id_pedido
        JOIN Libro l ON dp.id_libro = l.idLibro
        JOIN LibroGenero lg ON l.idLibro = lg.id_libro
        JOIN Genero g ON lg.id_genero = g.idGenero
        GROUP BY ci.nombre, g.nombre"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def complejo_1():
    db = get_db_connection()
    query = """SELECT s.nombre, AVG(dp.subtotal) AS promedio_ventas
        FROM Sucursal s JOIN Empleado e ON s.idSucursal = e.id_sucursal
        JOIN Pedido p ON e.idEmpleado = p.id_empleado
        JOIN DetallePedido dp ON p.idPedido = dp.id_pedido
        WHERE p.fecha >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
            AND s.idSucursal IN (SELECT id_sucursal
                    FROM Empleado
                    GROUP BY id_sucursal
                    )
        GROUP BY s.idSucursal
        ORDER BY promedio_ventas DESC"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def complejo_2():
    db = get_db_connection()
    query = """SELECT l.titulo, SUM(dp.cantidad) AS total_vendido
        FROM Libro l JOIN DetallePedido dp ON l.idLibro = dp.id_libro
        JOIN Pedido p ON dp.id_pedido = p.idPedido
        GROUP BY l.idLibro
        HAVING SUM(dp.cantidad) > (SELECT AVG(total_vendido)
                FROM (SELECT SUM(dp.cantidad) AS total_vendido
                    FROM Libro l JOIN DetallePedido dp ON l.idLibro = dp.id_libro
                    JOIN Pedido p ON dp.id_pedido = p.idPedido
                    GROUP BY l.idLibro
                    ) AS subquery
                )
        ORDER BY total_vendido DESC"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado


def complejo_3():
    db = get_db_connection()
    query = """SELECT e.nombre AS editorial, l.titulo AS libro, l.cantidad_disponible AS stock
        FROM Editorial e JOIN Libro l ON e.idEditorial = l.id_editorial
        WHERE l.cantidad_disponible < (SELECT AVG(cantidad_disponible)
                FROM Libro
                WHERE id_editorial = e.idEditorial
                )
        ORDER BY e.nombre, l.cantidad_disponible"""
    cursor = db.cursor(buffered=True)
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    db.close()

    return resultado

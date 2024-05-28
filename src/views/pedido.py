from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection
from views.libro import cargar_generos, cargar_libros

pedido = Blueprint("pedido", __name__)
libros: list[str] = []
generos: list[str] = []


@pedido.route("/pedir", methods=["POST"])
def pedir():
    id_libro = request.args.get("id_libro", type=int)
    id_cliente = request.args.get("id_cliente", type=int)
    print(f"id_libro: {id_libro} id_cliente: {id_cliente}")
    libros = cargar_libros()
    generos = cargar_generos()
    return render_template("inicio.html", libros=libros, generos=generos)


@pedido.route("/carro/<id_cliente>", methods=["GET", "POST"])
def carro(id_cliente: int):
    return f"Cliente: {id_cliente}"

from flask import Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection
from views.auth import auth
from views.autor import autor
from views.cliente import cliente
from views.empleado import empleado
from views.genero import genero
from views.libro import cargar_generos, cargar_libros, libro_bp
from views.pedido import pedido
from views.pedido_proveedor import pedido_proveedor
from views.reporte import reporte

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z]/'

app.register_blueprint(auth)
app.register_blueprint(libro_bp)
app.register_blueprint(cliente)
app.register_blueprint(empleado)
app.register_blueprint(autor)
app.register_blueprint(genero)
app.register_blueprint(pedido)
app.register_blueprint(pedido_proveedor)
app.register_blueprint(reporte)
libros: list[str] = []
generos: list[str] = []


@app.route("/")
def index():
    libros = cargar_libros()
    generos = cargar_generos()
    return render_template("inicio.html", libros=libros, generos=generos)


if __name__ == "__main__":
    app.run(debug=True)

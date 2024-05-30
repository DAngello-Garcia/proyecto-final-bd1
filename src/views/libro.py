from flask import Blueprint, Flask, redirect, render_template, request, session, url_for

from db.db import get_db_connection

libro_bp = Blueprint("libro", __name__)

autores: list[str] = []
id_autores: list[str] = []
editoriales: list[str] = []
id_editoriales: list[str] = []
presentaciones: list[str] = []
id_presentaciones: list[str] = []
todos_generos: list[str] = []
id_todos_generos: list[str] = []


@libro_bp.route("/detalle_libro/<libro_id>")
def detalle_libro(libro_id: int):
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    query = """SELECT l.idLibro, l.titulo, l.ISBN, l.fecha_publicacion, e.nombre, l.precio, l.cantidad_disponible, l.sinopsis, l.numero_paginas, l.idioma, l.peso, d.alto, d.ancho, d.largo, GROUP_CONCAT(g.nombre) AS generos, a.nombre, a.apellido, p.presentacion
        FROM Libro l JOIN Editorial e ON l.id_editorial = e.idEditorial
        JOIN Dimensiones d ON l.id_dimensiones = d.idDimensiones
        JOIN LibroGenero lg ON l.idLibro = lg.id_libro
        JOIN Genero g ON lg.id_genero = g.idGenero
        JOIN AutorLibro al ON al.id_libro = l.idLibro
        JOIN Autor a ON al.id_autor = a.idAutor
        JOIN LibroPresentacion lp ON lp.id_libro = l.idLibro
        JOIN Presentacion p ON p.idPresentacion = lp.id_presentacion
        WHERE l.idLibro = %s
        GROUP BY l.idLibro, l.titulo, l.ISBN, l.fecha_publicacion, e.nombre, l.precio, l.cantidad_disponible, l.sinopsis, l.numero_paginas, l.idioma, l.peso, d.alto, d.ancho, d.largo, a.nombre, a.apellido, p.presentacion"""
    values = (libro_id,)
    cursor.execute(query, values)
    libro = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template("libro/detalle-libro.html", libro=libro)


@libro_bp.route("/crear_libro", methods=["POST"])
def crear_libro():
    db = get_db_connection()
    titulo = request.form["titulo"]
    id_autor = request.form["autor"]
    fecha_publicacion = request.form["fecha_publicacion"]
    isbn = request.form["isbn"]
    id_editorial = request.form["editorial"]
    precio = request.form["precio"]
    cantidad_disponible = request.form["cantidad_disponible"]
    numero_paginas = request.form["numero_paginas"]
    sinopsis = request.form["sinopsis"]
    idioma = request.form["idioma"]
    peso = request.form["peso"]
    alto = request.form["alto"]
    ancho = request.form["ancho"]
    largo = request.form["largo"]
    id_presentacion = request.form["presentacion"]
    id_genero = request.form["id_genero"]

    query = """INSERT INTO Dimensiones (alto, ancho, largo) VALUES (%s, %s, %s)"""
    values = (alto, ancho, largo)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    id_dimensiones = cursor.lastrowid

    query = """INSERT INTO Libro (titulo, fecha_publicacion, isbn, id_editorial, precio, cantidad_disponible, numero_paginas, sinopsis, idioma, peso, id_dimensiones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        titulo,
        fecha_publicacion,
        isbn,
        id_editorial,
        precio,
        cantidad_disponible,
        numero_paginas,
        sinopsis,
        idioma,
        peso,
        id_dimensiones,
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    id_libro = cursor.lastrowid

    query = """INSERT INTO AutorLibro (id_libro, id_autor) VALUES (%s, %s)"""
    values = (id_libro, id_autor)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """INSERT INTO LibroGenero (id_libro, id_genero) VALUES (%s, %s)"""
    values = (id_libro, id_genero)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = (
        """INSERT INTO LibroPresentacion (id_libro, id_presentacion) VALUES (%s, %s)"""
    )
    values = (id_libro, id_presentacion)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()
    return redirect(url_for("libro.gestion"))


@libro_bp.route("/actualizar-libro/<id_libro>", methods=["POST"])
def actualizar(id_libro: int):
    db = get_db_connection()
    titulo = request.form["titulo"]
    fecha_publicacion = request.form["fecha_publicacion"]
    isbn = request.form["isbn"]
    id_editorial = request.form["editorial"]
    precio = request.form["precio"]
    cantidad_disponible = request.form["cantidad_disponible"]
    numero_paginas = request.form["numero_paginas"]
    sinopsis = request.form["sinopsis"]
    idioma = request.form["idioma"]
    peso = request.form["peso"]
    alto = request.form["alto"]
    ancho = request.form["ancho"]
    largo = request.form["largo"]
    id_presentacion = request.form["presentacion"]
    id_genero = request.form["id_genero"]

    query = """INSERT INTO Dimensiones (alto, ancho, largo) VALUES (%s, %s, %s)"""
    values = (alto, ancho, largo)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    id_dimensiones = cursor.lastrowid

    query = """UPDATE Libro SET titulo = %s, fecha_publicacion = %s, isbn = %s, id_editorial = %s, precio = %s, cantidad_disponible = %s, numero_paginas = %s, sinopsis = %s, idioma = %s, peso = %s, id_dimensiones = %s WHERE idLibro = %s"""
    values = (
        titulo,
        fecha_publicacion,
        isbn,
        id_editorial,
        precio,
        cantidad_disponible,
        numero_paginas,
        sinopsis,
        idioma,
        peso,
        id_dimensiones,
        id_libro,
    )
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """INSERT INTO LibroGenero (id_libro, id_genero) VALUES (%s, %s)"""
    values = (id_libro, id_genero)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = (
        """INSERT INTO LibroPresentacion (id_libro, id_presentacion) VALUES (%s, %s)"""
    )
    values = (id_libro, id_presentacion)
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    cursor.close()
    db.close()
    return redirect(url_for("libro.gestion_libro", libro_id=id_libro))


@libro_bp.route("/gestion_libro/<libro_id>")
def gestion_libro(libro_id: int):
    db = get_db_connection()
    id_editoriales.clear()
    editoriales.clear()
    id_presentaciones.clear()
    presentaciones.clear()
    id_todos_generos.clear()
    todos_generos.clear()
    cargar_editoriales()
    cargar_presentaciones()
    cargar_todos_generos()
    editoriales_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(editoriales, id_editoriales)
    )
    presentaciones_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(presentaciones, id_presentaciones)
    )
    generos_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(todos_generos, id_todos_generos)
    )
    cursor = db.cursor(buffered=True)
    query = """SELECT l.idLibro, l.titulo, l.ISBN, l.fecha_publicacion, e.nombre, l.precio, l.cantidad_disponible, l.sinopsis, l.numero_paginas, l.idioma, l.peso, d.alto, d.ancho, d.largo, GROUP_CONCAT(g.nombre) AS generos, a.nombre, a.apellido, p.presentacion
        FROM Libro l JOIN Editorial e ON l.id_editorial = e.idEditorial
        JOIN Dimensiones d ON l.id_dimensiones = d.idDimensiones
        JOIN LibroGenero lg ON l.idLibro = lg.id_libro
        JOIN Genero g ON lg.id_genero = g.idGenero
        JOIN AutorLibro al ON al.id_libro = l.idLibro
        JOIN Autor a ON al.id_autor = a.idAutor
        JOIN LibroPresentacion lp ON lp.id_libro = l.idLibro
        JOIN Presentacion p ON p.idPresentacion = lp.id_presentacion
        WHERE l.idLibro = %s
        GROUP BY l.idLibro, l.titulo, l.ISBN, l.fecha_publicacion, e.nombre, l.precio, l.cantidad_disponible, l.sinopsis, l.numero_paginas, l.idioma, l.peso, d.alto, d.ancho, d.largo, a.nombre, a.apellido, p.presentacion"""
    values = (libro_id,)
    cursor.execute(query, values)
    libro = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template(
        "libro/gestion-libro.html",
        libro=libro,
        editoriales=editoriales_options,
        presentaciones=presentaciones_options,
        generos_select=generos_options,
    )


@libro_bp.route("/eliminar-librp/<id_libro>", methods=["POST"])
def eliminar(id_libro: int):
    query = """DELETE FROM LibroPresentacion WHERE id_libro = %s"""
    values = (id_libro,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    query = """DELETE FROM LibroGenero WHERE id_libro = %s"""
    values = (id_libro,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    query = """DELETE FROM AutorLibro WHERE id_libro = %s"""
    values = (id_libro,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()

    query = """DELETE FROM Libro WHERE idLibro = %s"""
    values = (id_libro,)
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for("libro.gestion"))


@libro_bp.route("/buscar-libro", methods=["GET", "POST"])
def buscar_libro():
    if request.method == "POST":
        busqueda = request.form["busqueda_libro"]
        db = get_db_connection()
        cursor = db.cursor(buffered=True)
        query = """SELECT idLibro, titulo, precio, sinopsis FROM Libro WHERE titulo LIKE %s AND cantidad_disponible > 0"""
        values = ("%" + busqueda + "%",)
        cursor.execute(query, values)
        libros = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template("libro/buscar-libro.html", libros=libros)


@libro_bp.route("/buscar_genero/<genero_id>")
def buscar_genero(genero_id: int):
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    query = """SELECT l.idLibro, l.titulo, l.precio, l.sinopsis
        FROM Libro l JOIN LibroGenero lg ON l.idLibro = lg.id_libro
        JOIN Genero g ON lg.id_genero = g.idGenero
        WHERE l.cantidad_disponible > 0 AND g.idGenero = %s"""
    values = (genero_id,)
    cursor.execute(query, values)
    libros = cursor.fetchall()
    cursor.execute("""SELECT nombre FROM Genero WHERE idGenero = %s""", (genero_id,))
    genero = cursor.fetchone()
    cursor.close()
    db.close()
    genero = genero[0]
    return render_template(
        "libro/libros-categoria.html",
        libros=libros,
        generos=cargar_generos(),
        genero=genero,
    )


@libro_bp.route("/gestion")
def gestion():
    libros = cargar_libros()
    id_autores.clear()
    autores.clear()
    id_editoriales.clear()
    editoriales.clear()
    id_presentaciones.clear()
    presentaciones.clear()
    id_todos_generos.clear()
    todos_generos.clear()
    cargar_autores()
    cargar_editoriales()
    cargar_presentaciones()
    cargar_todos_generos()
    autores_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(autores, id_autores)
    )
    editoriales_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(editoriales, id_editoriales)
    )
    presentaciones_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(presentaciones, id_presentaciones)
    )
    generos_options = "".join(
        f'<option value="{value}">{label}</option>'
        for label, value in zip(todos_generos, id_todos_generos)
    )
    return render_template(
        "libro/gestion.html",
        libros=libros,
        autores=autores_options,
        editoriales=editoriales_options,
        presentaciones=presentaciones_options,
        generos_select=generos_options,
    )


def cargar_libros() -> list[str]:
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(
        """SELECT idLibro, titulo, precio, sinopsis FROM Libro WHERE cantidad_disponible > 0"""
    )
    libros_cursor = cursor.fetchall()
    cursor.close()
    db.close()
    return libros_cursor


def cargar_autores() -> None:
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT idAutor, CONCAT(nombre, ' ', apellido) FROM Autor""")
    autores_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, autor in autores_cursor:
        id_autores.append(valor)
        autores.append(autor)


def cargar_editoriales() -> None:
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT idEditorial, nombre FROM Editorial""")
    editoriales_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, editorial in editoriales_cursor:
        id_editoriales.append(valor)
        editoriales.append(editorial)


def cargar_presentaciones() -> None:
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT idPresentacion, presentacion FROM Presentacion""")
    presentaciones_cursor = cursor.fetchall()
    cursor.close()
    db.close()

    for valor, presentacion in presentaciones_cursor:
        id_presentaciones.append(valor)
        presentaciones.append(presentacion)


def cargar_generos() -> list[str]:
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute(
        """SELECT DISTINCT Genero.idGenero, Genero.nombre
        FROM Genero JOIN LibroGenero ON Genero.idGenero = LibroGenero.id_genero
        JOIN Libro ON LibroGenero.id_libro = Libro.idLibro
        WHERE Libro.cantidad_disponible > 0"""
    )
    generos_cursor = cursor.fetchall()
    cursor.close()
    db.close()
    return generos_cursor


def cargar_todos_generos():
    db = get_db_connection()
    cursor = db.cursor(buffered=True)
    cursor.execute("""SELECT idGenero, nombre FROM Genero""")
    generos_cursor = cursor.fetchall()
    cursor.close()
    db.close()
    for valor, genero in generos_cursor:
        id_todos_generos.append(valor)
        todos_generos.append(genero)

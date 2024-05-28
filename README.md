# Librería

## Requisitos
Tener instalado [Docker](https://www.docker.com/products/docker-desktop/) y [Python](https://www.python.org/downloads/).

## ¿Cómo correr el proyecto?
Abrir Docker Desktop.

Clonar el repositorio
```console
$ git clone 
$ cd ./src/
```

Crear un contenedor que corra la base de datos MySQL
```console
$ docker compose up -d
```

Correr la aplicación web
```console
$ python ./app.py
```


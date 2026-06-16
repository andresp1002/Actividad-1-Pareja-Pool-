# Monitoreo de Rendimiento: Connection Pooling con PostgreSQL y Python

Este proyecto compara el rendimiento de realizar consultas a una base de datos PostgreSQL utilizando una **Conexión Dedicada (Sin Pool)** frente a un **Pool de Conexiones (Con Pool)** usando `psycopg2`.

## Requisitos
* Python 3.x
* PostgreSQL
* Biblioteca `psycopg2` o `psycopg2-binary`

## Configuración
Modifica las credenciales en el script con los datos de tu base de datos local:
```python
DB_CONFIG = {
    "database": "Conexion",
    "user": "emilianava",
    "password": "root",
    "host": "192.168.208.17",
    "port": "5432"
}

Cómo Ejecutarlo
Instala la dependencia:
pip install psycopg2-binary

Ejecuta el script de prueba:
python nombre_de_tu_archivo.py

¿Cómo funciona el Pool de Conexiones?
Sin Pool: Abre y cierra una conexión física por cada consulta, lo que genera una alta latencia debido al acuerdo de red (handshake) y consumo de CPU en el servidor.

Con Pool: Mantiene un grupo de conexiones abiertas y reutilizables. El script solicita una conexión con db_pool.getconn() y la devuelve con db_pool.putconn(conexion) sin cerrarla, optimizando drásticamente el tiempo de ejecución.
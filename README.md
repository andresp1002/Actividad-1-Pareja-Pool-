# Monitoreo de Rendimiento: Connection Pooling con PostgreSQL y Python

## Descripción

Este proyecto tiene como objetivo comparar el rendimiento de las conexiones a una base de datos **PostgreSQL** utilizando dos enfoques diferentes:

* **Conexión dedicada (Sin Pool):** se crea y cierra una conexión para cada consulta.
* **Pool de Conexiones (Con Pool):** se reutilizan conexiones mediante `SimpleConnectionPool` de la biblioteca **psycopg2**.

Además, se realiza una prueba de concurrencia utilizando **10 hilos (threads)** para simular múltiples solicitudes simultáneas hacia la base de datos.


## Objetivo

Implementar y evaluar el uso de un **Pool de Conexiones** en Python para comprender cómo mejora el rendimiento y optimiza el acceso concurrente a una base de datos PostgreSQL.


# Tecnologías utilizadas

* Python 3.x
* PostgreSQL
* psycopg2 / psycopg2-binary
* threading
* time


# Estructura del proyecto

```text
Actividad-1-Pareja-Pool/
│
├── laboratorio_pool.py
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```


# Configuración de la Base de Datos

Antes de ejecutar el proyecto, configure los datos de conexión en el archivo Python (o en el archivo `.env` si decide utilizar variables de entorno).

```python
DB_CONFIG = {
    "database": "Conexion",
    "user": "emilianava",
    "password": "root",
    "host": "192.168.208.17",
    "port": "5432"
}
```


## Instalación

### 1. Clonar el repositorio:

```bash
git clone https://github.com/andresp1002/Actividad-1-Pareja-Pool-.git
```

### 2. Ingresar al proyecto:

```bash
cd Actividad-1-Pareja-Pool-
```

### 3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install psycopg2-binary
```


## Ejecución

Ejecutar el programa con:

```bash
python main.py
```


# Funcionamiento del Pool de Conexiones

## Sin Pool

Cada consulta realiza el siguiente proceso:

* Crear una nueva conexión.
* Ejecutar la consulta.
* Cerrar la conexión.

Este procedimiento incrementa el tiempo de respuesta debido al costo de crear una conexión nueva en cada petición.



## Con Pool

El programa crea un conjunto de conexiones reutilizables utilizando:

```python
pool.SimpleConnectionPool(2, 10, **DB_CONFIG)
```
El pool fue configurado con:
* Mínimo de conexiones disponibles: 2.
* Máximo de conexiones disponibles: 10.

Esto permite mantener conexiones listas para ser utilizadas y controlar la cantidad de conexiones simultáneas hacia PostgreSQL.

Posteriormente:

* Obtiene una conexión mediante `getconn()`.
* Ejecuta la consulta.
* Devuelve la conexión al pool con `putconn()`.

De esta forma se evita crear y destruir conexiones constantemente, mejorando el rendimiento de la aplicación.

## Manejo de conexiones y errores

Cada conexión obtenida desde el pool es administrada mediante bloques de control que permiten liberar correctamente los recursos utilizados.

Cuando una consulta finaliza, la conexión es devuelta al pool para que pueda ser reutilizada por otros procesos.

Esto evita fugas de conexiones y mantiene estable la comunicación con PostgreSQL.

## Cierre del Pool

Al finalizar la ejecución del programa, las conexiones utilizadas son cerradas correctamente mediante:

```python
pool.closeall()
```

Esto permite liberar los recursos asociados al pool de conexiones.


# Prueba de concurrencia

El proyecto implementa una simulación de acceso concurrente utilizando **10 hilos (Threads)**.

Cada hilo:

* Solicita una conexión al pool.
* Ejecuta una consulta.
* Devuelve la conexión al pool.

Esto permite comprobar el correcto funcionamiento del pool bajo múltiples solicitudes simultáneas.



# Prueba de rendimiento

El programa realiza dos pruebas:

### Sin Pool

Se ejecutan múltiples consultas creando una conexión nueva en cada iteración.

### Con Pool

Las consultas reutilizan conexiones previamente abiertas mediante el pool.

Al finalizar, el programa muestra:

* Tiempo total sin Pool.
* Tiempo total con Pool.
* Comparación de rendimiento.
* Tiempo de ejecución con 10 hilos concurrentes.


# Resultados

Al ejecutar el programa se obtiene una salida similar a la siguiente:

```text
Tiempo total SIN POOL: 4.8621 segundos

Tiempo total CON POOL: 1.3764 segundos

El Pool de conexiones fue aproximadamente 3.53 veces más rápido.

========== PRUEBA CON 10 HILOS ==========

Hilo 1: consulta ejecutada correctamente.
Hilo 2: consulta ejecutada correctamente.
...
Hilo 10: consulta ejecutada correctamente.

Tiempo con 10 hilos: 0.0832 segundos
```

> **Nota:** Los tiempos pueden variar dependiendo del hardware y de la configuración de PostgreSQL.


### Integrantes

* María Emilia Navarrete Ávila
* Andrés Peralta


# Conclusiones

La implementación del **Connection Pooling** permite reutilizar conexiones abiertas hacia PostgreSQL, reduciendo significativamente el tiempo de respuesta y el consumo de recursos del servidor.

Las pruebas realizadas muestran que el uso de un **Pool de Conexiones** mejora el rendimiento frente al uso de conexiones dedicadas, especialmente cuando existen múltiples solicitudes concurrentes.

# Pregunta de reflexión
## - ¿Qué pasaría si olvidamos poner la línea db_pool.putconn(conexion) dentro del bloque finally?
Si omitimos el putconn en el bloque finally, las conexiones quedan "prestadas" o "huérfanas". Como la aplicación no devuelve la conexión al pool, esta sigue apareciendo como ocupada indefinidamente. Esto provoca que el pool se vacíe rápidamente hasta alcanzar su capacidad máxima. Una vez lleno, cualquier nueva solicitud de la aplicación se quedará esperando una conexión libre hasta que se agote el tiempo de espera, provocando un error de Timeout.

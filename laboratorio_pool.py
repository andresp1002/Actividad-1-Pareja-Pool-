import time                  
import threading             
import psycopg2              
from psycopg2 import pool    


# Configuración de la base de datos
DB_CONFIG = {
    "database": "Conexion",
    "user": "emilianava",
    "password": "root",
    "host": "192.168.208.17",
    "port": "5432"
}

# PRUEBA 1: CONEXIÓN DEDICADA (SIN POOL)
def consulta_sin_pool():

    # Crear una nueva conexión
    conexion = psycopg2.connect(**DB_CONFIG)

    # Crear cursor
    cursor = conexion.cursor()

    # Ejecutar consulta de prueba
    cursor.execute("SELECT 1;")

    # Obtener el resultado
    cursor.fetchone()

    # Cerrar el cursor
    cursor.close()

    # Cerrar la conexión
    conexion.close()


# PRUEBA 2: POOL DE CONEXIONES

print("--- Inicializando el Pool de Conexiones ---")

# Crear un pool con mínimo 2 y máximo 10 conexiones
db_pool = pool.SimpleConnectionPool(2, 10, **DB_CONFIG)

def consulta_con_pool():

    # Inicializar la variable conexión
    conexion = None

    try:

        # Obtener una conexión del pool
        conexion = db_pool.getconn()

        # Crear cursor
        cursor = conexion.cursor()

        # Ejecutar consulta de prueba
        cursor.execute("SELECT 1;")

        # Obtener el resultado
        cursor.fetchone()

        # Cerrar únicamente el cursor
        cursor.close()

    except Exception as e:

        # Mostrar errores de conexión
        print(f"Error: {e}")

    finally:

        # Devolver la conexión al pool
        if conexion:
            db_pool.putconn(conexion)


# PRUEBA DE RENDIMIENTO

# Número de consultas a ejecutar
ITERACIONES = 1000

print(f"\nEjecutando {ITERACIONES} consultas SIN POOL...")

# Iniciar cronómetro
inicio_sin_pool = time.perf_counter()

# Ejecutar consultas sin pool
for _ in range(ITERACIONES):
    consulta_sin_pool()

# Finalizar cronómetro
fin_sin_pool = time.perf_counter()

# Calcular tiempo total
tiempo_sin_pool = fin_sin_pool - inicio_sin_pool

print(f"Tiempo total SIN POOL: {tiempo_sin_pool:.4f} segundos")

print(f"\nEjecutando {ITERACIONES} consultas CON POOL...")

# Iniciar cronómetro
inicio_con_pool = time.perf_counter()

# Ejecutar consultas con pool
for _ in range(ITERACIONES):
    consulta_con_pool()

# Finalizar cronómetro
fin_con_pool = time.perf_counter()

# Calcular tiempo total
tiempo_con_pool = fin_con_pool - inicio_con_pool

print(f"Tiempo total CON POOL: {tiempo_con_pool:.4f} segundos")

# Calcular la mejora obtenida
mejora = tiempo_sin_pool / tiempo_con_pool

print(f"\n¡El Pool de conexiones fue aproximadamente {mejora:.1f} veces más rápido!")


# PRUEBA DE CONCURRENCIA

def ejecutar_hilo(numero):

    # Inicializar la conexión
    conexion = None

    try:

        # Obtener una conexión del pool
        conexion = db_pool.getconn()

        # Crear cursor
        cursor = conexion.cursor()

        # Ejecutar consulta
        cursor.execute("SELECT 1;")

        # Obtener resultado
        cursor.fetchone()

        # Cerrar cursor
        cursor.close()

        # Mostrar que el hilo terminó correctamente
        print(f"Hilo {numero}: consulta ejecutada correctamente.")

    except Exception as e:

        # Mostrar errores
        print(f"Hilo {numero}: {e}")

    finally:

        # Regresar la conexión al pool
        if conexion:
            db_pool.putconn(conexion)

print("\n========== PRUEBA CON 10 HILOS ==========")

# Iniciar cronómetro
inicio_hilos = time.perf_counter()

# Lista donde se almacenarán los hilos
hilos = []

# Crear e iniciar los 10 hilos
for i in range(10):

    hilo = threading.Thread(target=ejecutar_hilo, args=(i + 1,))

    # Guardar el hilo
    hilos.append(hilo)

    # Iniciar el hilo
    hilo.start()

# Esperar a que todos finalicen
for hilo in hilos:
    hilo.join()

# Finalizar cronómetro
fin_hilos = time.perf_counter()

print(f"\nTiempo con 10 hilos: {fin_hilos - inicio_hilos:.4f} segundos")


# Cerrar todas las conexiones del pool
db_pool.closeall()
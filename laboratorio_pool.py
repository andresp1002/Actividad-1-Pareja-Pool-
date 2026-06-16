import time
import psycopg2
from psycopg2 import pool

# Configuración de credenciales (Ajusta estos datos a tu BD local)
DB_CONFIG = {
    "database": "Conexion",
    "user": "emilianava",
    "password": "root",
    "host": "192.168.208.17",
    "port": "5432"
}

# ==================
# ========================
# PRUEBA 1: SIN POOL (Conexión Dedicada)
# ==========================================
def consulta_sin_pool():
    # Abre conexión física
    conexion = psycopg2.connect(**DB_CONFIG)
    cursor = conexion.cursor()
    
    # Ejecuta una consulta simple
    cursor.execute("SELECT 1;")
    cursor.fetchone()
    
    # Cierra todo
    cursor.close()
    conexion.close()

# ==========================================
# PRUEBA 2: CON POOL de Conexiones
# ==========================================
print("--- Inicializando el Pool de Conexiones ---")
# Inicializamos el Pool (Min: 2, Max: 10 conexiones)
db_pool = pool.SimpleConnectionPool(2, 10, **DB_CONFIG)

def consulta_con_pool():
    conexion = None
    try:
        # En lugar de crear, le pedimos una conexión al pool
        conexion = db_pool.getconn()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT 1;")
        cursor.fetchone()
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        if conexion:
            # SÚPER IMPORTANTE: Devolvemos la conexión al pool, NO la cerramos
            db_pool.putconn(conexion)

# ==========================================
# MEDICIÓN DE RENDIMIENTO (Simulando 100 peticiones)
# ==========================================
ITERACIONES = 1000

print(f"\nEjecutando {ITERACIONES} consultas SIN POOL...")
inicio_sin_pool = time.time()
for _ in range(ITERACIONES):
    consulta_sin_pool()
fin_sin_pool = time.time()
tiempo_sin_pool = fin_sin_pool - inicio_sin_pool
print(f"Tiempo total SIN POOL: {tiempo_sin_pool:.4f} segundos")

print(f"\nEjecutando {ITERACIONES} consultas CON POOL...")
inicio_con_pool = time.time()
for _ in range(ITERACIONES):
    consulta_con_pool()
fin_con_pool = time.time()
tiempo_con_pool = fin_con_pool - inicio_con_pool
print(f"Tiempo total CON POOL: {tiempo_con_pool:.4f} segundos")

# Calcular ganancia
mejora = tiempo_sin_pool / tiempo_con_pool
print(f"\n¡El Pool de conexiones fue aproximadamente {mejora:.1f} veces más rápido!")

# Al apagar la aplicación se cierra el pool por completo
db_pool.closeall()
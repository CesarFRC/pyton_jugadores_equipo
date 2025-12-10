import json
import time
import socket
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://donlike:123@cluster0.khggmzf.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "futbol"

ARCHIVOS = {
    "jugadores.json": "jugadores",
    "equipos.json": "equipos",
    "equipos_completos.json": "equipos_jugadores"
}

internet_disponible = False
ultima_verificacion = 0
tiempo_entre_verificaciones = 60


def verificar_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False


def obtener_datos_json(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
            return datos if datos else None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def guardar_datos_json(nombre_archivo, datos):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar {nombre_archivo}: {e}")
        return False


def conectar_mongodb():
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        cliente.admin.command('ping')
        base_datos = cliente[DATABASE_NAME]
        return cliente, base_datos
    except Exception as e:
        print(f"Error al conectar MongoDB: {e}")
        return None, None


def sincronizar_archivo(archivo, coleccion_nombre, base_datos):
    print(f"  Procesando: {archivo}")
    datos = obtener_datos_json(archivo)
    
    if not datos:
        print(f"Archivo vacío, se omite")
        return False
    
    if isinstance(datos, dict):
        datos = [datos]

    try:
        coleccion = base_datos[coleccion_nombre]
        coleccion.delete_many({})
        
        resultado = coleccion.insert_many(datos)
        cantidad = len(resultado.inserted_ids)
        print(f"{cantidad} documentos guardados en MongoDB")
        
        
        return True
        
    except Exception as e:
        print(f"  Error: {e}\n")
        return False



def sincronizar_todos_archivos():
    print(f"\n[{time.strftime('%H:%M:%S')}] Iniciando sincronización...")
    cliente, base_datos = conectar_mongodb()
    if not cliente:
        print("No se pudo conectar a MongoDB\n")
        return
    
    print("Conexión a MongoDB exitosa\n")
    
    for archivo, coleccion_nombre in ARCHIVOS.items():
        sincronizar_archivo(archivo, coleccion_nombre, base_datos)
    
    cliente.close()
    print("Sincronización completada\n")


def monitorear_internet():
    global internet_disponible, ultima_verificacion 
    print("Sistema iniciado. Esperando conexión a internet...\n")
    while True:
        tiempo_actual = time.time()
        
        if tiempo_actual - ultima_verificacion >= tiempo_entre_verificaciones:
            hay_internet = verificar_internet()
            ultima_verificacion = tiempo_actual
            
            if hay_internet and not internet_disponible:
                internet_disponible = True
                print(f"[{time.strftime('%H:%M:%S')}] CONEXIÓN DETECTADA")
                sincronizar_todos_archivos()
            
            elif not hay_internet and internet_disponible:
                internet_disponible = False
                print(f"[{time.strftime('%H:%M:%S')}] SIN CONEXIÓN - Los datos se guardan localmente")
            
            elif hay_internet and internet_disponible:
                sincronizar_todos_archivos()
        
        time.sleep(5)
        



if __name__ == "__main__":
    monitorear_internet()
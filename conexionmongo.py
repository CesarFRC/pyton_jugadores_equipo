import time
import socket
from pymongo import MongoClient
# Asegúrate de tener gestor_pendientes.py en la misma carpeta
from gestor_pendientes import obtener_pendientes, limpiar_pendientes 

MONGO_URI = "mongodb+srv://donlike:123@cluster0.khggmzf.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "futbol"

internet_disponible = False
ultima_verificacion = 0
tiempo_entre_verificaciones = 30 # Revisar cada 60 segundos

def verificar_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False

def procesar_cola_pendientes(base_datos):
    """
    Lee la lista de pendientes y ejecuta las acciones específicas en Mongo.
    """
    pendientes = obtener_pendientes()
    
    if not pendientes:
        return 

    print(f"\n--- PROCESANDO {len(pendientes)} CAMBIOS PENDIENTES ---")
    
    for cambio in pendientes:
        coleccion = base_datos[cambio["coleccion"]]
        accion = cambio["accion"]
        datos = cambio["datos"]

        try:
            if accion == "insertar":
                # Usamos replace_one con upsert para evitar duplicados y errores
                coleccion.replace_one({"id": datos["id"]}, datos, upsert=True)
                print(f" -> Insertado/Actualizado: {datos.get('nombre', 'ID '+str(datos.get('id')))}")

            elif accion == "actualizar":
                coleccion.update_one({"id": datos["id"]}, {"$set": datos})
                print(f" -> Actualizado ID: {datos.get('id')}")

            elif accion == "eliminar":
                id_eliminar = datos if isinstance(datos, (int, str)) else datos.get("id")
                coleccion.delete_one({"id": id_eliminar})
                print(f" -> Eliminado ID: {id_eliminar}")

        except Exception as e:
            print(f" Error procesando pendiente: {e}")

    # Solo limpiamos la lista si terminamos el loop
    limpiar_pendientes()
    print("--- PENDIENTES SINCRONIZADOS Y LIMPIADOS ---\n")

def intentar_sincronizar():
    """
    Función envoltorio: Verifica si hay pendientes ANTES de conectar a Mongo.
    Ahorra recursos y datos.
    """
    # 1. Chequeo local rápido: ¿Hay algo que subir?
    if not obtener_pendientes():
        # Si no hay pendientes, no hacemos nada.
        return

    # 2. Si hay pendientes, intentamos conectar
    print(f"[{time.strftime('%H:%M:%S')}] Cambios detectados. Conectando a MongoDB...")
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        cliente.admin.command('ping') # Verificar conexión real
        base_datos = cliente[DATABASE_NAME]
        
        procesar_cola_pendientes(base_datos)
        
        cliente.close()
        print(" Conexión cerrada correctamente.")
        
    except Exception as e:
        print(f" No se pudo sincronizar: {e}")

def monitorear_internet():
    global internet_disponible, ultima_verificacion 
    print("Sistema iniciado. Esperando conexión a internet...\n")
    
    while True:
        tiempo_actual = time.time()
        
        if tiempo_actual - ultima_verificacion >= tiempo_entre_verificaciones:
            hay_internet = verificar_internet()
            ultima_verificacion = tiempo_actual
            
            # CASO 1: Regresa el internet
            if hay_internet and not internet_disponible:
                internet_disponible = True
                print(f"[{time.strftime('%H:%M:%S')}] CONEXIÓN DETECTADA - Sincronizando...")
                intentar_sincronizar()
            
            # CASO 2: Se va el internet
            elif not hay_internet and internet_disponible:
                internet_disponible = False
                print(f"[{time.strftime('%H:%M:%S')}] SIN CONEXIÓN - Los cambios se guardarán en cola.")
            
            # CASO 3: Hay internet estable (Mantenimiento)
            elif hay_internet and internet_disponible:
                # Revisamos si se generaron pendientes nuevos mientras había internet
                intentar_sincronizar()
        
        time.sleep(5)

if __name__ == "__main__":
    monitorear_internet()
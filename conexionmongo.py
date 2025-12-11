import time
import socket
from pymongo import MongoClient
from bson import ObjectId # <--- CRUCIAL: Para convertir texto a ID real
from gestor_pendientes import obtener_pendientes, limpiar_pendientes 

MONGO_URI = "mongodb+srv://donlike:123@cluster0.khggmzf.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "futbol"

internet_disponible = False
ultima_verificacion = 0
tiempo_entre_verificaciones = 30 

def verificar_internet():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False

def procesar_cola_pendientes(base_datos):
    pendientes = obtener_pendientes()
    
    if not pendientes:
        return 

    print(f"\n--- PROCESANDO {len(pendientes)} CAMBIOS PENDIENTES ---")
    
    for cambio in pendientes:
        coleccion_nombre = cambio["coleccion"]
        coleccion = base_datos[coleccion_nombre]
        accion = cambio["accion"]
        datos = cambio["datos"]

        try:
            # === CONVERTIR TEXTO A OBJECTID DE MONGO ===
            oid = None
            
            # Caso 1: Viene dentro de los datos (insertar/actualizar)
            if isinstance(datos, dict) and "_id" in datos:
                # Convertimos el string "65a..." a ObjectId real
                datos["_id"] = ObjectId(datos["_id"])
                oid = datos["_id"]
            
            # Caso 2: Compatibilidad vieja (si usabas 'id' normal)
            elif isinstance(datos, dict) and "id" in datos:
                oid = datos["id"]
            # ============================================

            if accion == "insertar":
                # Usamos replace_one con upsert=True.
                # Esto significa: "Busca este _id. Si existe, actualízalo. Si no, créalo."
                # Es a prueba de fallos si se subió dos veces.
                if oid:
                    coleccion.replace_one({"_id": oid}, datos, upsert=True)
                    print(f" -> Sincronizado: {oid}")
                else:
                    coleccion.insert_one(datos)

            elif accion == "actualizar":
                if oid:
                    coleccion.update_one({"_id": oid}, {"$set": datos})
                    print(f" -> Actualizado ID: {oid}")

            elif accion == "eliminar":
                # En eliminar, 'datos' suele ser {"_id": "..."}
                id_eliminar_str = datos.get("_id") or datos.get("id")
                if id_eliminar_str:
                    # Convertimos a ObjectId para poder borrarlo en la nube
                    try:
                        id_mongo = ObjectId(id_eliminar_str)
                    except:
                        id_mongo = id_eliminar_str # Si era un ID viejo (número)

                    coleccion.delete_one({"_id": id_mongo})
                    print(f" -> Eliminado ID: {id_mongo}")

        except Exception as e:
            print(f" Error procesando pendiente en {coleccion_nombre}: {e}")

    limpiar_pendientes()
    print("--- PENDIENTES SINCRONIZADOS Y LIMPIADOS ---\n")

def intentar_sincronizar():
    if not obtener_pendientes():
        return

    print(f"[{time.strftime('%H:%M:%S')}] Cambios detectados. Conectando a MongoDB...")
    try:
        cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        cliente.admin.command('ping') 
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
            
            if hay_internet and not internet_disponible:
                internet_disponible = True
                print(f"[{time.strftime('%H:%M:%S')}] CONEXIÓN DETECTADA - Sincronizando...")
                intentar_sincronizar()
            
            elif not hay_internet and internet_disponible:
                internet_disponible = False
                print(f"[{time.strftime('%H:%M:%S')}] SIN CONEXIÓN - Los cambios se guardarán en cola.")
            
            elif hay_internet and internet_disponible:
                intentar_sincronizar()
        
        time.sleep(5)

if __name__ == "__main__":
    monitorear_internet()
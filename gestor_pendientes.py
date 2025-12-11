import json
import os

ARCHIVO_PENDIENTES = "cambios_pendientes.json"

def registrar_pendiente(coleccion, accion, datos):
    """
    coleccion: "jugadores", "equipos", etc.
    accion: "insertar", "actualizar", "eliminar"
    datos: El diccionario del objeto o el ID (para eliminar)
    """
    entrada = {
        "coleccion": coleccion,
        "accion": accion,
        "datos": datos
    }

    lista_pendientes = []
    
    # 1. Leemos lo que ya hay (si existe el archivo)
    if os.path.exists(ARCHIVO_PENDIENTES):
        try:
            with open(ARCHIVO_PENDIENTES, 'r', encoding='utf-8') as f:
                lista_pendientes = json.load(f)
        except:
            lista_pendientes = []

    # 2. Agregamos el nuevo cambio
    lista_pendientes.append(entrada)

    # 3. Guardamos
    with open(ARCHIVO_PENDIENTES, 'w', encoding='utf-8') as f:
        json.dump(lista_pendientes, f, indent=4, ensure_ascii=False)
    
    print(f" [OFFLINE] Cambio registrado en pendientes: {accion} en {coleccion}")

def obtener_pendientes():
    if not os.path.exists(ARCHIVO_PENDIENTES):
        return []
    try:
        with open(ARCHIVO_PENDIENTES, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def limpiar_pendientes():
    if os.path.exists(ARCHIVO_PENDIENTES):
        os.remove(ARCHIVO_PENDIENTES)
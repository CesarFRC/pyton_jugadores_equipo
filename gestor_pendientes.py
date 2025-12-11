import json
import os

ARCHIVO_PENDIENTES = "cambios_pendientes.json"

def registrar_pendiente(coleccion, accion, datos):
    entrada = {
        "coleccion": coleccion,
        "accion": accion,
        "datos": datos
    }

    lista_pendientes = []
    
    if os.path.exists(ARCHIVO_PENDIENTES):
        try:
            with open(ARCHIVO_PENDIENTES, 'r', encoding='utf-8') as f:
                lista_pendientes = json.load(f)
        except:
            lista_pendientes = []

    lista_pendientes.append(entrada)

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
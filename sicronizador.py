import threading
from conexionmongo import monitorear_internet

def iniciar_sincronizador():
    hilo = threading.Thread(target=monitorear_internet, daemon=True)
    hilo.start()

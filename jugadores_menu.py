from jugadores import jugador
from sicronizador import iniciar_sincronizador
# --- AGREGADO 1: Importamos la función para avisar al sincronizador ---
from gestor_pendientes import registrar_pendiente 

class JugadoresMenu:
    
    def __init__(self, jugadores_iniciales=None):
        if jugadores_iniciales is not None:
            self.jugadores = jugadores_iniciales
            self.debe_guardar = False
            self.archivo = None
        else:
            self.archivo = "jugadores.json"
            self.jugadores = jugador()
            datos = self.jugadores.lectura_json(self.archivo)
            self.debe_guardar = True
            if datos:
                self.jugadores = jugador().convertir_a_objeto(datos)

    def mostrar_menu(self):
        print("\n=== SISTEMA DE GESTIÓN DE JUGADORES ===")
        print("1. Agregar jugador")
        print("2. Ver jugadores")
        print("3. Actualizar jugador")
        print("4. Eliminar jugador")
        print("0. Salir")
        return input("\nSeleccione una opción: ")

    def pedir_datos_jugador(self):
        try:
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            posicion = input("Posición: ")
            nacionalidad = input("Nacionalidad: ")
            numero_de_camiseta = int(input("Número de camiseta: "))
            
            nuevo_jugador = jugador(nombre, edad, posicion, nacionalidad, numero_de_camiseta)
            
            # --- AGREGADO 2: Asegurar un ID para la nube ---
            # Si tu clase jugador no tiene .id, usamos la camiseta como identificador
            if not hasattr(nuevo_jugador, 'id'):
                nuevo_jugador.id = numero_de_camiseta
            # -----------------------------------------------
            
            return nuevo_jugador
        except ValueError:
            print("Error: Ingrese datos válidos")
            return None

    def agregar(self):
        print("\n-- AGREGAR JUGADOR --")
        nuevo = self.pedir_datos_jugador()
        if nuevo:
            self.jugadores.create(nuevo)
            if not self.debe_guardar:
                print("No se guardara lo agregado")
                return
            
            self.jugadores.guardar_json(self.archivo)
            print("Jugador agregado exitosamente y guardado")

            # --- AGREGADO 3: Avisar al sincronizador ---
            # vars(nuevo) convierte el objeto en diccionario para guardarlo
            registrar_pendiente("jugadores", "insertar", vars(nuevo)) 
            # -------------------------------------------

    def ver(self):
        print("\n-- LISTA DE JUGADORES --")
        if getattr(self.jugadores, "es_lista", True) and not self.jugadores.read():
            print("No hay jugadores registrados")
            return
        for i, j in enumerate(self.jugadores.read()):
            print(f"{i}. {j}")

    def actualizar(self):
        if getattr(self.jugadores, "es_lista", True) and not self.jugadores.read():
            print("\nNo hay jugadores para actualizar")
            return
        print("\n-- ACTUALIZAR JUGADOR --")
        for i, j in enumerate(self.jugadores.read()):
            print(f"{i}. {j}")
        try:
            indice = int(input("\nÍndice del jugador a actualizar: "))
            
            # --- AGREGADO 4A: Rescatar ID original antes de cambiar datos ---
            viejo = self.jugadores.read()[indice]
            id_original = getattr(viejo, 'id', getattr(viejo, 'numero_de_camiseta', None))
            # ---------------------------------------------------------------

            nuevo = self.pedir_datos_jugador()
            if nuevo:
                # --- AGREGADO 4B: Mantener el ID para que Mongo sepa a cual cambiar ---
                if id_original: nuevo.id = id_original
                # ----------------------------------------------------------------------

                self.jugadores.update(indice, nuevo)
                if not self.debe_guardar:
                    print("No se guardara lo actualizado")
                    return
                
                self.jugadores.guardar_json(self.archivo)
                print("Jugador actualizado exitosamente")

                # --- AGREGADO 5: Avisar al sincronizador ---
                registrar_pendiente("jugadores", "actualizar", vars(nuevo))
                # -------------------------------------------

        except ValueError:
            print("Error: Índice inválido")

    def eliminar(self):
        if getattr(self.jugadores, "es_lista", True) and not self.jugadores.read():
            print("\nNo hay jugadores para eliminar")
            return
        print("\n-- ELIMINAR JUGADOR --")
        for i, j in enumerate(self.jugadores.read()):
            print(f"{i}. {j}")
        try:
            indice = int(input("\nÍndice del jugador a eliminar: "))
            
            # --- AGREGADO 6A: Capturar ID ANTES de borrar de la lista ---
            obj_borrar = self.jugadores.read()[indice]
            id_borrar = getattr(obj_borrar, 'id', getattr(obj_borrar, 'numero_de_camiseta', None))
            # ------------------------------------------------------------

            self.jugadores.delete(indice)
            if not self.debe_guardar:
                print("No se guardara ")
                return
            
            self.jugadores.guardar_json(self.archivo)
            print("Jugador eliminado exitosamente")

            # --- AGREGADO 6B: Avisar al sincronizador ---
            if id_borrar:
                registrar_pendiente("jugadores", "eliminar", {"id": id_borrar})
            # --------------------------------------------

        except ValueError:
            print("Error: Índice inválido")
        except IndexError:
            print("Error: Índice fuera de rango") # Agregué esto por seguridad

    def run(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == "1":
                self.agregar()
            elif opcion == "2":
                self.ver()
            elif opcion == "3":
                self.actualizar()
            elif opcion == "4":
                self.eliminar()
            elif opcion == "0":
                print("\nSaliendo del programa...")
                break
            else:
                print("\nOpción no válida, intente de nuevo")


if __name__ == "__main__":
    iniciar_sincronizador()
    menu = JugadoresMenu() 
    menu.run()
from equipo_jugadores import equipo_jugadores
from equipo_menu import EquipoMenu
from jugadores_menu import JugadoresMenu
from jugadores import jugador 
from equipo import equipo
from sicronizador import iniciar_sincronizador
# --- AGREGADO 1: Importar gestor ---
from gestor_pendientes import registrar_pendiente

class EquipoJugadoresMenu:

    def __init__(self, equipos_iniciales=None):
        if equipos_iniciales is not None:
            self.lista = equipos_iniciales
            self.debe_guardar = False
            self.archivo = None
        else:
            self.archivo = "equipos_completos.json"
            self.lista = equipo_jugadores() 
            datos = self.lista.lectura_json(self.archivo)
            self.debe_guardar = True
            if datos:
                self.lista = equipo_jugadores().convertir_a_objeto(datos)
        
        # Inicializamos los menús internos como None (parte de tu lógica original)
        self._jugadores_menu = None
        self._equipos_menu = None

    # --- AGREGADO 2: Función auxiliar para limpiar datos anidados ---
    # Esto es necesario porque tienes objetos dentro de objetos.
    def _serializar(self, entidad):
        # Intentamos obtener el ID, si no tiene, usamos el nombre del equipo
        id_obj = getattr(entidad, "id", getattr(entidad.equipo, "nombre", "sin_id"))
        return {
            "id": id_obj,
            "equipo": vars(entidad.equipo), # Convierte el objeto equipo a dict
            "jugadores": [vars(j) for j in entidad.jugadores] # Convierte la lista de jugadores a dicts
        }
    # -------------------------------------------------------------
                
    def jugadores_menu(self):
        if self._jugadores_menu is None:
            self._jugadores_menu = JugadoresMenu()
        return self._jugadores_menu
    
    def equipos_menu(self):
        if self._equipos_menu is None:
            self._equipos_menu = EquipoMenu()
        return self._equipos_menu
        
    def mostrar_menu(self):
        print("\n=== MENÚ EQUIPOS COMPLETOS ===")
        print("1. Agregar equipos jugadores")
        print("2. Ver Equipos jugadores")
        print("3. actualizar equipos jugadores")
        print("4. Eliminar Equipo Completo") 
        print("0. Salir")
        return input("\nSeleccione una opción: ")

    def agregar(self):
        equipo_menu_temp = EquipoMenu(equipo())
        nuevo_equipo = equipo_menu_temp.pedir_datos_equipo()
        # Nota: Si el usuario cancela la creación del equipo, nuevo_equipo podría ser None.
        # Asumo que tu lógica maneja eso, si no, daría error aquí abajo.
        
        jugadores_menu_temp = JugadoresMenu(jugador()) 
        # Truco: Limpiamos la lista del menú temporal para que empiece vacía
        if hasattr(jugadores_menu_temp.jugadores, 'datos'): jugadores_menu_temp.jugadores.datos = []
        
        print("\n--- AGREGAR JUGADORES (Salir del sub-menú para terminar) ---")
        jugadores_menu_temp.run()      
        jugadores_list = jugadores_menu_temp.jugadores
        
        nueva_entidad = equipo_jugadores(nuevo_equipo, jugadores_list)
        
        # --- AGREGADO 3: Asignar ID (Nombre del equipo) ---
        if not hasattr(nueva_entidad, 'id'):
            nueva_entidad.id = nuevo_equipo.nombre
        # --------------------------------------------------

        self.lista.create(nueva_entidad)
        
        if self.debe_guardar and self.archivo:
            self.lista.guardar_json(self.archivo)
            print("Equipo completo agregado y guardado")

            # --- AGREGADO 4: Registrar Pendiente ---
            try:
                datos_limpios = self._serializar(nueva_entidad)
                registrar_pendiente("equipos_jugadores", "insertar", datos_limpios)
            except Exception as e:
                print(f"Error al registrar pendiente: {e}")
            # ---------------------------------------
        else:
            print("Equipo completo agregado (no se guardó en archivo)")

    def ver_equipos_completos(self): 
        print("Lista de equipos completos")
        equipos = self.lista.read()
        
        for i, ej in enumerate(equipos):
            print(f"--- ÍNDICE {i} ---")
            print(ej)
            print("-" * 40)
            
    def actualizar_equipos_completos(self):
        equipos = self.lista.read()
        self.ver_equipos_completos()
        print("\n-- ACTUALIZAR EQUIPO COMPLETO --")
        
        try:
            indice = int(input("Índice del equipo completo a actualizar: "))
            entidad_a_modificar = equipos[indice]
            
            # --- AGREGADO 5: Capturar ID Original ---
            id_original = getattr(entidad_a_modificar, "id", getattr(entidad_a_modificar.equipo, "nombre", None))
            # ----------------------------------------

            equipo_crud = equipo()
            equipo_crud.create(entidad_a_modificar.equipo)
            equipo_menu_temp = EquipoMenu(equipo_crud)
            equipo_menu_temp.run() 
            equipo_modificado = equipo_menu_temp.equipos.read()[0] 
            
            jugadores_menu_temp = JugadoresMenu(entidad_a_modificar.jugadores)
            jugadores_menu_temp.run()
            jugadores_modificados_list = entidad_a_modificar.jugadores
            
            nueva_entidad = equipo_jugadores(equipo_modificado, jugadores_modificados_list)
            
            # --- AGREGADO 6: Restaurar ID ---
            if id_original: nueva_entidad.id = id_original
            else: nueva_entidad.id = equipo_modificado.nombre
            # --------------------------------

            self.lista.update(indice, nueva_entidad)
            
            if self.debe_guardar and self.archivo:
                self.lista.guardar_json(self.archivo)
                print("Equipo Completo actualizado y guardado.")

                # --- AGREGADO 7: Registrar Actualización ---
                datos_limpios = self._serializar(nueva_entidad)
                registrar_pendiente("equipos_jugadores", "actualizar", datos_limpios)
                # -------------------------------------------
            else:
                print("Equipo Completo actualizado. No se guardó en archivo.")

        except (ValueError, IndexError):
            print("Error: Índice inválido")
            
    def eliminar_equipo_completo(self):
        self.ver_equipos_completos()
        print("\n-- ELIMINAR EQUIPO COMPLETO --")
    
        try:
            indice = int(input("Índice del equipo completo a eliminar: "))
            
            # --- AGREGADO 8: Capturar ID antes de borrar ---
            entidad_borrar = self.lista.read()[indice]
            id_borrar = getattr(entidad_borrar, "id", getattr(entidad_borrar.equipo, "nombre", None))
            # -----------------------------------------------

            self.lista.delete(indice)
            
            if self.debe_guardar and self.archivo:
                self.lista.guardar_json(self.archivo)
                print("Equipo Completo eliminado y guardado.")

                # --- AGREGADO 9: Registrar Eliminación ---
                if id_borrar:
                    registrar_pendiente("equipos_jugadores", "eliminar", {"id": id_borrar})
                # -----------------------------------------
            else:
                print("Equipo Completo eliminado. No se guardó en archivo.")
        
        except (ValueError, IndexError):
            print("Error: Índice inválido")
            
    def run(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == "1":
                self.agregar()
            elif opcion == "2":
                self.ver_equipos_completos()
            elif opcion == "3":
                self.actualizar_equipos_completos()
            elif opcion == "4":
                self.eliminar_equipo_completo()
            elif opcion == "0":
                print("\nSaliendo...")
                break
            else:
                print("Opción no válida, intente de nuevo")


if __name__ == "__main__":
    iniciar_sincronizador()
    menu = EquipoJugadoresMenu()
    menu.run()
from equipo_jugadores import equipo_jugadores
from equipo_menu import EquipoMenu
from jugadores_menu import JugadoresMenu


class EquipoJugadoresMenu:
    def __init__(self, equipos_iniciales=None):
        self.archivo = "equipos_completos.json"
        
        self.eq_menu = EquipoMenu()
        self.jug_menu = JugadoresMenu()
        
        self.debe_guardar = True
        
        if equipos_iniciales is not None:
            self.lista = equipos_iniciales
            self.debe_guardar = False
            
        else:
            self.lista = equipo_jugadores()
            datos = self.lista.lectura_json(self.archivo)
            if datos:
                self.lista = equipo_jugadores().convertir_a_objeto(datos)
                
                self.debe_guardar = False

    def _normalizar_jugadores(self, jugadores_data):
        """Asegura que los datos de jugadores sean siempre una lista."""
        if jugadores_data is None:
            return []
        # Asumiendo que si no es lista, es el objeto 'jugador' singular
        if not isinstance(jugadores_data, list):
            return [jugadores_data]
        return jugadores_data[:] # Retorna una copia si ya es una lista

    def mostrar_menu(self):
        print("\n=== SISTEMA DE GESTIÓN DE EQUIPOS CON JUGADORES ===")
        print("1. Agregar equipo con jugadores")
        print("2. Ver equipos")
        print("3. Actualizar equipo con jugadores")
        print("4. Eliminar equipo")
        print("0. Salir")
        return input("\nSeleccione una opción: ")

    def pedir_datos_equipo(self):
        try:
            return self.eq_menu.pedir_datos_equipo()
        except Exception:
            print("Error: datos de equipo inválidos")
            return None

    def pedir_jugadores(self):
        jugadores = []
        try:
            n = int(input("¿Cuántos jugadores agregar? (0 para ninguno): "))
        except ValueError:
            print("Número inválido, se agregarán 0 jugadores")
            n = 0
        for i in range(n):
            print(f"-- Jugador {i+1} --")
            j = self.jug_menu.pedir_datos_jugador()
            if j:
                jugadores.append(j)
        return jugadores

    def agregar(self):
        print("\n-- AGREGAR EQUIPO CON JUGADORES --")
        eq = self.pedir_datos_equipo()
        if not eq:
            return
        jgs = self.pedir_jugadores()
        item = equipo_jugadores(eq, jgs)
        self.lista.create(item)
        if self.debe_guardar:
            self.lista.guardar_json(self.archivo)
            print("Equipo creado y guardado")
        else:
            print("Equipo creado en memoria. NO se guardará automáticamente porque el archivo ya fue cargado o es una lista externa.")

    def ver(self):
        print("\n-- LISTA DE EQUIPOS --")
        if getattr(self.lista, "es_lista", True) and not self.lista.read():
            print("No hay equipos registrados")
            return
        for i, ej in enumerate(self.lista.read()):
            print(f"\n[{i}]")
            nombre_eq = getattr(getattr(ej, "equipo", None), "nombre", None)
            if nombre_eq:
                print(f"Equipo: {nombre_eq}")
            print(ej)

    def actualizar(self):
        if getattr(self.lista, "es_lista", True) and not self.lista.read():
            print("\nNo hay equipos para actualizar")
            return
        print("\n-- Selecione el equipo a actualizar --")
        for i, ej in enumerate(self.lista.read()):
            nombre = getattr(getattr(ej, "equipo", None), "nombre", None) or str(ej)
            print(f"{i}. {nombre}")
        try:
            idx_equipo = int(input("\nÍndice del equipo a actualizar: "))
        except ValueError:
            print("Indice invalido.")
            return
        if not (0 <= idx_equipo < len(self.lista.read())):
            print("Indice fuera de rango")
            return
        
        equipo_item = self.lista.read()[idx_equipo]
        
        print("\n¿Que desea actualizar?")
        print("1. Datos del equipo")
        print("2. Un jugador del equipo")
        print("3. Reemplazar la lista completa de jugadores")
        print("0. Cancelar")
        opcion = input("Selecionar: ").strip()
        
        if opcion == "1":
            nuevo_eq = self.pedir_datos_equipo()
            if not nuevo_eq:
                print("Actualizacion cancelada. ")
                return
            
            # --- CORRECCIÓN CLAVE ---
            jugadores_raw = getattr(equipo_item, "jugadores", None)
            jugadores_actuales = self._normalizar_jugadores(jugadores_raw)
            # ------------------------
            
            nuevo_item = equipo_jugadores(nuevo_eq, jugadores_actuales)
            self.lista.update(idx_equipo, nuevo_item)
            mensaje = "Datos del equipo actualizados"
            
        elif opcion == "2":
            jugadores_raw = getattr(equipo_item, "jugadores", None)
            jugadores_list = self._normalizar_jugadores(jugadores_raw) # Aplicando normalización
            
            if not jugadores_list:
                print("El equipo no tiene jugadores para actualizar. ")
                return
            print("\nJugadores del equipo: ")
            
            # Ahora jugadores_list es una lista y se puede iterar
            for i, j in enumerate(jugadores_list):
                print(f"{i}. {j}")
            try:
                idx_j = int(input("Indice del jugador a actualizar: "))
            except ValueError:
                print("Indice invalido.")
                return
            if not (0 <= idx_j < len(jugadores_list)):
                print("Indice fuera de rango. ")
                return
            
            nuevo_j = self.jug_menu.pedir_datos_jugador()
            if not nuevo_j:
                print("Actualizacion de jugador cancelada. ")
                return
            
            nuevos = jugadores_list[:] # Copia de la lista normalizada
            nuevos[idx_j] = nuevo_j
            nuevo_item = equipo_jugadores(getattr(equipo_item, "equipo", None), nuevos)
            self.lista.update(idx_equipo,nuevo_item)
            mensaje = "Jugador actualizado en el equipo"
            
        elif opcion == "3":
            nuevos = self.pedir_jugadores()
            nuevo_item = equipo_jugadores(getattr(equipo_item, "equipo", None), nuevos)
            self.lista.update(idx_equipo, nuevo_item)
            mensaje = "Lista de jugadores remplazada"
            
        else:
            print("Operacion cancelada")
            return
        
        if self.debe_guardar:
            self.lista.guardar_json(self.archivo)
            print(f"{mensaje} y guardado.")
        else:
            print(f"{mensaje} en memoria (no guardado automaticamente).")

    def eliminar(self):
        if getattr(self.lista, "es_lista", True) and not self.lista.read():
            print("\nNo hay equipos para eliminar")
            return
        print("\n-- ELIMINAR EQUIPO --")
        for i, ej in enumerate(self.lista.read()):
            nombre_eq = getattr(getattr(ej, "equipo", None), "nombre", None)
            titulo = nombre_eq if nombre_eq else str(ej)
            print(f"{i}. {titulo}")
        try:
            idx = int(input("\nÍndice del equipo a eliminar: "))
            self.lista.delete(idx)
            if self.debe_guardar:
                self.lista.guardar_json(self.archivo)
                print("Equipo eliminado y guardado")
            else:
                print("Equipo eliminado en memoria (no se guarda automáticamente).")
        except ValueError:
            print("Índice inválido")

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
    menu = EquipoJugadoresMenu()
    menu.run()
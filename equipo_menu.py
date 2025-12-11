from equipo import equipo
from sicronizador import iniciar_sincronizador
# --- AGREGADO 1: Importamos el gestor ---
from gestor_pendientes import registrar_pendiente

class EquipoMenu:
    def __init__(self, equipos_iniciales=None):
        if equipos_iniciales is not None:
            self.equipos = equipos_iniciales
            self.debe_guardar = False
            self.archivo = None
        else:
            self.archivo = "equipos.json"
            self.equipos = equipo()
            datos = self.equipos.lectura_json(self.archivo)
            self.debe_guardar = True
            if datos:
                self.equipos = equipo().convertir_a_objeto(datos)

    def mostrar_menu(self):
        print("\n=== SISTEMA DE GESTIÓN DE EQUIPOS ===")
        print("1. Agregar equipo")
        print("2. Ver equipos")
        print("3. Actualizar equipo")
        print("4. Eliminar equipo")
        print("0. Salir")
        return input("\nSeleccione una opción: ")

    def pedir_datos_equipo(self):
        try:
            nombre = input("Nombre: ")
            entrenador = input("Entrenador: ")
            estadio = input("Estadio: ")
            pais = input("País: ")
            año_fundacion = int(input("Año de fundación: "))
            
            nuevo_equipo = equipo(nombre, entrenador, estadio, pais, año_fundacion)
            
            # --- AGREGADO 2: Asegurar ID para la nube ---
            # Si el equipo no tiene 'id', usamos el nombre como identificador único
            if not hasattr(nuevo_equipo, 'id'):
                nuevo_equipo.id = nombre
            # --------------------------------------------

            return nuevo_equipo
        except ValueError:
            print("Error: Ingrese datos válidos")
            return None

    def agregar(self):
        print("\n-- AGREGAR EQUIPO --")
        nuevo = self.pedir_datos_equipo()
        if nuevo:
            self.equipos.create(nuevo)
            if not self.debe_guardar:
                print("No se guardara lo agregado  ")
                return
            
            self.equipos.guardar_json(self.archivo)
            print("Equipo agregado y guardado")

            # --- AGREGADO 3: Registrar inserción ---
            registrar_pendiente("equipos", "insertar", vars(nuevo))
            # ---------------------------------------

    def ver(self):
        print("\n-- LISTA DE EQUIPOS --")
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("No hay equipos registrados")
            return
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")

    def actualizar(self):
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para actualizar")
            return
        print("\n-- ACTUALIZAR EQUIPO --")
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")
        try:
            indice = int(input("\nÍndice del equipo a actualizar: "))
            
            # --- AGREGADO 4: Capturar ID original ---
            viejo = self.equipos.read()[indice]
            # Intentamos obtener 'id', si no existe, usamos 'nombre'
            id_original = getattr(viejo, 'id', getattr(viejo, 'nombre', None))
            # ----------------------------------------

            nuevo = self.pedir_datos_equipo()
            if nuevo:
                # Mantenemos el ID para no perder el rastro en la nube
                if id_original: nuevo.id = id_original

                self.equipos.update(indice, nuevo)
                if not self.debe_guardar:
                    print("No guardara los equipos")
                    return
                
                self.equipos.guardar_json(self.archivo)
                print("Equipo actualizado y guardado")

                # --- AGREGADO 5: Registrar actualización ---
                registrar_pendiente("equipos", "actualizar", vars(nuevo))
                # -------------------------------------------

        except ValueError:
            print("Error: Índice inválido")

    def eliminar(self):
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para eliminar")
            return
        print("\n-- ELIMINAR EQUIPO --")
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")
        try:
            indice = int(input("\nÍndice del equipo a eliminar: "))
            
            # --- AGREGADO 6: Capturar ID antes de borrar ---
            obj_borrar = self.equipos.read()[indice]
            id_borrar = getattr(obj_borrar, 'id', getattr(obj_borrar, 'nombre', None))
            # -----------------------------------------------

            self.equipos.delete(indice)
            if not self.debe_guardar:
                print("No Guardara cambios")
                return
            
            self.equipos.guardar_json(self.archivo)
            print("Equipo eliminado y guardado")

            # --- AGREGADO 7: Registrar eliminación ---
            if id_borrar:
                registrar_pendiente("equipos", "eliminar", {"id": id_borrar})
            # -----------------------------------------

        except ValueError:
            print("Error: Índice inválido")

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
                print("\nSaliendo...")
                break
            else:
                print("Opción no válida, intente de nuevo")


if __name__ == "__main__":
    iniciar_sincronizador()
    menu = EquipoMenu()
    menu.run()
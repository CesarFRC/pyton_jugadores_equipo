from equipo import equipo


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
            return equipo(nombre, entrenador, estadio, pais, año_fundacion)
        except ValueError:
            print("Error: Ingrese datos válidos")
            return None

    def agregar(self):
        if not self.debe_guardar:
            print("No debe agregar equipos  ")
            return
        print("\n-- AGREGAR EQUIPO --")
        nuevo = self.pedir_datos_equipo()
        if nuevo:
            self.equipos.create(nuevo)
            self.equipos.guardar_json(self.archivo)
            print("Equipo agregado y guardado")

    def ver(self):
        print("\n-- LISTA DE EQUIPOS --")
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("No hay equipos registrados")
            return
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")

    def actualizar(self):
        if not self.debe_guardar:
            print("No debe actuazlizar equipo")
            return
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para actualizar")
            return
        print("\n-- ACTUALIZAR EQUIPO --")
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")
        try:
            indice = int(input("\nÍndice del equipo a actualizar: "))
            nuevo = self.pedir_datos_equipo()
            if nuevo:
                self.equipos.update(indice, nuevo)
                self.equipos.guardar_json(self.archivo)
                print("Equipo actualizado y guardado")
        except ValueError:
            print("Error: Índice inválido")

    def eliminar(self):
        if not self.debe_guardar:
            print("No debe eliminar equipos")
            return
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para eliminar")
            return
        print("\n-- ELIMINAR EQUIPO --")
        for i, e in enumerate(self.equipos.read()):
            print(f"{i}. {e}")
        try:
            indice = int(input("\nÍndice del equipo a eliminar: "))
            self.equipos.delete(indice)
            self.equipos.guardar_json(self.archivo)
            print("Equipo eliminado y guardado")
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
    menu = EquipoMenu()
    menu.run()
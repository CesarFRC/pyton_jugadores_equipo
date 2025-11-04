from jugadores import jugador


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
            return jugador(nombre, edad, posicion, nacionalidad, numero_de_camiseta)
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
            nuevo = self.pedir_datos_jugador()
            if nuevo:
                self.jugadores.update(indice, nuevo)
                if not self.debe_guardar:
                    print("No se guardara lo actualizado")
                    return
                self.jugadores.guardar_json(self.archivo)
                print("Jugador actualizado exitosamente")
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
            self.jugadores.delete(indice)
            if not self.debe_guardar:
                print("No se guardara ")
                return
            self.jugadores.guardar_json(self.archivo)
            print("Jugador eliminado exitosamente")
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
                print("\nSaliendo del programa...")
                break
            else:
                print("\nOpción no válida, intente de nuevo")


if __name__ == "__main__":
    menu = JugadoresMenu() 
    menu.run()
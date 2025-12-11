from jugadores import jugador
from sicronizador import iniciar_sincronizador
from gestor_pendientes import registrar_pendiente 
from bson import ObjectId 

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

            if not hasattr(nuevo_jugador, '_id'):
                nuevo_jugador._id = str(ObjectId()) 
            
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

            datos_limpios = vars(nuevo).copy()
            if "es_lista" in datos_limpios:
                del datos_limpios["es_lista"]

            registrar_pendiente("jugadores", "insertar", datos_limpios) 

    def ver(self):
        print("\n-- LISTA DE JUGADORES --")
        if getattr(self.jugadores, "es_lista", True) and not self.jugadores.read():
            print("No hay jugadores registrados")
            return
        for i, j in enumerate(self.jugadores.read()):
            id_mongo = getattr(j, '_id', 'Sin ID')
            print(f"{i}. {j} [ID Mongo: {id_mongo}]")

    def actualizar(self):
        if getattr(self.jugadores, "es_lista", True) and not self.jugadores.read():
            print("\nNo hay jugadores para actualizar")
            return
        print("\n-- ACTUALIZAR JUGADOR --")
        for i, j in enumerate(self.jugadores.read()):
            print(f"{i}. {j}")
        try:
            indice = int(input("\nÍndice del jugador a actualizar: "))
            
            viejo = self.jugadores.read()[indice]

            id_original = getattr(viejo, '_id', getattr(viejo, 'id', getattr(viejo, 'numero_de_camiseta', None)))
            
            nuevo = self.pedir_datos_jugador()
            if nuevo:
                if id_original: 
                    nuevo._id = id_original 

                self.jugadores.update(indice, nuevo)
                if not self.debe_guardar:
                    print("No se guardara lo actualizado")
                    return
                
                self.jugadores.guardar_json(self.archivo)
                print("Jugador actualizado exitosamente")

                datos_limpios = vars(nuevo).copy()
                if "es_lista" in datos_limpios:
                    del datos_limpios["es_lista"]

                registrar_pendiente("jugadores", "actualizar", datos_limpios)

        except ValueError:
            print("Error: Índice inválido")

    def eliminar(self):
        self.ver() 
        try:
            indice = int(input("\nÍndice del jugador a eliminar: "))
            
            obj_borrar = self.jugadores.read()[indice]
            id_borrar = getattr(obj_borrar, '_id', getattr(obj_borrar, 'id', None))
            
            self.jugadores.delete(indice)
            if not self.debe_guardar:
                print("No se guardara ")
                return
            
            self.jugadores.guardar_json(self.archivo)
            print("Jugador eliminado exitosamente")

            if id_borrar:
                registrar_pendiente("jugadores", "eliminar", {"_id": id_borrar})

        except (ValueError, IndexError):
            print("Error: Índice inválido")

    def run(self):
        while True:
            opcion = self.mostrar_menu()
            if opcion == "1": self.agregar()
            elif opcion == "2": self.ver()
            elif opcion == "3": self.actualizar()
            elif opcion == "4": self.eliminar()
            elif opcion == "0": break
            else: print("\nOpción no válida")

if __name__ == "__main__":
    iniciar_sincronizador()
    menu = JugadoresMenu() 
    menu.run()
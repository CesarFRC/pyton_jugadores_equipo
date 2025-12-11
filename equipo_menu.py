from equipo import equipo
from sicronizador import iniciar_sincronizador
from gestor_pendientes import registrar_pendiente
# --- AGREGADO: Importamos ObjectId para generar IDs únicos ---
from bson import ObjectId 

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
            
            # --- CAMBIO CLAVE: Generar ID de Mongo localmente ---
            # Si no tiene _id, generamos uno nuevo y lo convertimos a texto
            if not hasattr(nuevo_equipo, '_id'):
                nuevo_equipo._id = str(ObjectId())
            # ----------------------------------------------------

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
                print("No se guardara lo agregado")
                return
            
            self.equipos.guardar_json(self.archivo)
            print("Equipo agregado y guardado")

            # Registramos el pendiente (nuevo ya trae su _id)
            registrar_pendiente("equipos", "insertar", vars(nuevo))

    def ver(self):
        print("\n-- LISTA DE EQUIPOS --")
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("No hay equipos registrados")
            return
        for i, e in enumerate(self.equipos.read()):
            # Mostramos el ID para confirmar
            id_str = getattr(e, '_id', 'Sin ID')
            print(f"{i}. {e} [ID: {id_str}]")

    def actualizar(self):
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para actualizar")
            return
        
        # Reutilizamos ver() para mostrar la lista
        self.ver()
        
        try:
            indice = int(input("\nÍndice del equipo a actualizar: "))
            
            # --- RESCATAR ID ORIGINAL ---
            viejo = self.equipos.read()[indice]
            # Prioridad: _id > id > nombre
            id_original = getattr(viejo, '_id', getattr(viejo, 'id', getattr(viejo, 'nombre', None)))
            # ----------------------------

            nuevo = self.pedir_datos_equipo()
            if nuevo:
                # Pegamos el ID original al nuevo objeto
                if id_original: 
                    nuevo._id = id_original

                self.equipos.update(indice, nuevo)
                if not self.debe_guardar:
                    print("No guardara los equipos")
                    return
                
                self.equipos.guardar_json(self.archivo)
                print("Equipo actualizado y guardado")

                registrar_pendiente("equipos", "actualizar", vars(nuevo))

        except ValueError:
            print("Error: Índice inválido")

    def eliminar(self):
        if getattr(self.equipos, "es_lista", True) and not self.equipos.read():
            print("\nNo hay equipos para eliminar")
            return
        
        self.ver()
        
        try:
            indice = int(input("\nÍndice del equipo a eliminar: "))
            
            # --- CAPTURAR ID PARA BORRAR EN NUBE ---
            obj_borrar = self.equipos.read()[indice]
            id_borrar = getattr(obj_borrar, '_id', getattr(obj_borrar, 'id', getattr(obj_borrar, 'nombre', None)))
            # ---------------------------------------

            self.equipos.delete(indice)
            if not self.debe_guardar:
                print("No Guardara cambios")
                return
            
            self.equipos.guardar_json(self.archivo)
            print("Equipo eliminado y guardado")

            if id_borrar:
                # Enviamos el ID a la cola de pendientes
                registrar_pendiente("equipos", "eliminar", {"_id": id_borrar})

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
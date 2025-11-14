from equipo_jugadores import equipo_jugadores
from equipo_menu import EquipoMenu
from jugadores_menu import JugadoresMenu
from jugadores import jugador 
from equipo import equipo

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
        jugadores_menu_temp = JugadoresMenu(jugador()) 
        jugadores_menu_temp.run()      
        jugadores_list = jugadores_menu_temp.jugadores.read()
        nueva_entidad = equipo_jugadores(nuevo_equipo, jugadores_list)
        self.lista.create(nueva_entidad)
        if self.debe_guardar and self.archivo:
            self.lista.guardar_json(self.archivo)
            print("Equipo completo agregado y guardado")
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
        
        indice = int(input("Índice del equipo completo a actualizar: "))
        entidad_a_modificar = equipos[indice]
        equipo_crud = equipo()
        equipo_crud.create(entidad_a_modificar.equipo)
        equipo_menu_temp = EquipoMenu(equipo_crud)
        equipo_menu_temp.run() 
        equipo_modificado = equipo_menu_temp.equipos.read()[0] 
        jugadores_menu_temp = JugadoresMenu(entidad_a_modificar.jugadores)
        jugadores_menu_temp.run()
        jugadores_modificados_list = entidad_a_modificar.jugadores.read()
        nueva_entidad = equipo_jugadores(equipo_modificado, jugadores_modificados_list)
        self.lista.update(indice, nueva_entidad)
        if self.debe_guardar and self.archivo:
            self.lista.guardar_json(self.archivo)
            print("Equipo Completo actualizado y guardado.")
        else:
            print("Equipo Completo actualizado. No se guardó en archivo.")
            
    def eliminar_equipo_completo(self):
        self.ver_equipos_completos()
        print("\n-- ELIMINAR EQUIPO COMPLETO --")
    
        indice = int(input("Índice del equipo completo a eliminar: "))
        self.lista.delete(indice)
        
        if self.debe_guardar and self.archivo:
            self.lista.guardar_json(self.archivo)
            print("Equipo Completo eliminado y guardado.")
        else:
            print("Equipo Completo eliminado. No se guardó en archivo.")
            
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
    menu = EquipoJugadoresMenu()
    menu.run()
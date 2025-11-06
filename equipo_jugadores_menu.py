from equipo_jugadores import equipo_jugadores
from equipo_menu import EquipoMenu
from jugadores_menu import JugadoresMenu

class EquipoJugadoresMenu:

    def __init__(self, equipos_iniciales=None):

        self.equipos_menu = EquipoMenu()
        self.jugadores_menu = JugadoresMenu()

        if equipos_iniciales is not None:
            self.lista = equipos_iniciales
            self.debe_guardar = False
        else:
            self.archivo = "equipos_completos.json"
            self.lista = equipo_jugadores() 
            datos = self.lista.lectura_json(self.archivo)
            self.debe_guardar = True

            if datos:
                self.lista = equipo_jugadores().convertir_a_objeto(datos)
                
                
                
    def mostrar_menu(self):
        print("\n=== MENÚ EQUIPOS COMPLETOS ===")
        print("1. Asignar jugador a un equipo")
        print("2. Gestión de jugadores") 
        print("3. Gestión de equipos")   
        print("0. Salir")
        return input("\nSeleccione una opción: ")
    
    
    
    def sincronizar_equipos(self):
        equipos_simples = self.equipos_menu.equipos.read()
        
        nombres_en_lista_completa = [ej.equipo.nombre for ej in self.lista.read()]
        
        nuevos_equipos_agregados = []
        
        for equipo_simple in equipos_simples:
            if equipo_simple.nombre not in nombres_en_lista_completa:
                nuevo_ej = equipo_jugadores(equipo_simple, [])
                self.lista.create(nuevo_ej)
                nuevos_equipos_agregados.append(equipo_simple.nombre)

        if nuevos_equipos_agregados:
            print(f"¡Equipos sincronizados! Listos para asignar jugadores: {', '.join(nuevos_equipos_agregados)}")
            if self.debe_guardar:
                self.lista.guardar_json(self.archivo)
                
                
    def asignar_jugador_equipo(self):
        print("\n== ASIGNAR JUGADOR A EQUIPO ==")

        jugadores_disponibles = self.jugadores_menu.jugadores.read()
        equipos_completos = self.lista.read() 

        if not jugadores_disponibles:
            print("No hay jugadores disponibles. Use la Opción 2 para agregarlos.")
            return

        if not equipos_completos:
            print("No hay equipos registrados. Use la Opción 3 para agregarlos y sincronizar.")
            return

        print("\nJugadores (a asignar):")
        for i, j in enumerate(jugadores_disponibles):
            print(f"{i}. {j.nombre}")

        try:
            idx_jugador = int(input("Seleccione el **número** del jugador: "))
            jugador_obj = jugadores_disponibles[idx_jugador]
        except (ValueError, IndexError):
            print("Error: Índice de jugador inválido.")
            return

        print("\nEquipos (a modificar):")
        for i, ej in enumerate(equipos_completos):
            print(f"{i}. {ej.equipo.nombre}") 

        try:
            idx_equipo = int(input("Seleccione el **número** del equipo: "))
            equipo_jugadores_obj = equipos_completos[idx_equipo]
        except (ValueError, IndexError):
            print("Error: Índice de equipo inválido.")
            return
        
        equipo_jugadores_obj.jugadores.create(jugador_obj)
        
        if self.debe_guardar:
            self.lista.guardar_json(self.archivo) 

        print(f"\n{jugador_obj.nombre} ha sido asignado a {equipo_jugadores_obj.equipo.nombre}.")
    
    def recargar_jugadores(self):
        if self.jugadores_menu.archivo:
            datos = self.jugadores_menu.jugadores.lectura_json(self.jugadores_menu.archivo)
            if datos:
                self.jugadores_menu.jugadores = self.jugadores_menu.jugadores.convertir_a_objeto(datos)


    def recargar_equipos(self):
        if self.equipos_menu.archivo:
            datos = self.equipos_menu.equipos.lectura_json(self.equipos_menu.archivo)
            if datos:
                self.equipos_menu.equipos = self.equipos_menu.equipos.convertir_a_objeto(datos)
            
    def run(self):
        while True:
            self.sincronizar_equipos()
            
            opcion = self.mostrar_menu()
            if opcion == "1":
                self.asignar_jugador_equipo()       
            elif opcion == "2":
                self.jugadores_menu.run()
                self.recargar_jugadores()
            elif opcion == "3":
                self.equipos_menu.run()   
                self.recargar_equipos()
            elif opcion == "0":
                print("\nAdiós. Aplicación terminada.")
                break
            else:
                print("Opción no válida")


if __name__ == "__main__":
    menu = EquipoJugadoresMenu()
    menu.run()

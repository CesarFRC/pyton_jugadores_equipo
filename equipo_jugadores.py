from jugadores import jugador
from equipo import equipo

class equipo_jugadores:
    def __init__(self , equipo, jugadores):
        self.equipo = equipo
        self.jugadores = jugadores

if __name__ == "__main__":
    equipo1 = equipo("Atlas", "Diego Cocca", "Estadio Jalisco", "México", 1916)
    jugador1 = jugador("Lionel Messi", 36, "Delantero", "Argentino", 10)
    jugador2 = jugador("Cristiano Ronaldo", 39, "Delantero", "Portugués", 7)
    

    equipo_con_jugadores = equipo_jugadores(equipo1, [jugador1, jugador2])
    
    """
    print(f"Equipo: {equipo_con_jugadores.equipo.nombre}, Estadio: {equipo_con_jugadores.equipo.estadio}, País: {equipo_con_jugadores.equipo.pais}, Año de Fundación: {equipo_con_jugadores.equipo.año_fundacion}")
    for j in equipo_con_jugadores.jugadores:
        print(f"Jugador: {j.nombre}, Edad: {j.edad}, Posición: {j.posicion}, Nacionalidad: {j.nacionalidad}, Número de Camiseta: {j.numero_de_camiseta}")
    """
from jugadores import jugador

class equipo:
    def __init__(self,nombre,entrenador,estadio,pais,año_fundacion):
        self.nombre = nombre
        self.entrenador = entrenador
        self.estadio = estadio
        self.pais = pais
        self.año_fundacion = año_fundacion

if __name__ == "__main__":
    equipo1 = equipo("Atlas", "Diego Cocca", "Estadio Jalisco", "México", 1916)
    
    equipo = [equipo1]
    """""
    for e in equipo:
        print(f"{e.nombre} - {e.entrenador} - {e.estadio} - {e.pais} - {e.año_fundacion}")
    """""
from crud import crud

class equipo(crud):
    def __init__(self,nombre=None,entrenador=None,estadio=None,pais=None,año_fundacion=None):
        self.es_lista = (nombre is None and entrenador is None and estadio is None and pais is None and año_fundacion is None)
        if self.es_lista:
            super().__init__()
        else:
            self.nombre = nombre
            self.entrenador = entrenador
            self.estadio = estadio
            self.pais = pais
            self.año_fundacion = año_fundacion

    def __str__(self):
        if not self.es_lista:
            return f"{self.nombre} - {self.entrenador} - {self.estadio} - {self.pais} - {self.año_fundacion}"
        else:
            return f"Arreglo de {len(self.valor)} equipos"

if __name__ == "__main__":
    equipos = equipo()
    
    equipos.create(equipo("Atlas","Diego Cocca", "Estadio Jalisco", "Mexico", 1916))
    equipos.create(equipo("Real Madrid", "Carlo Ancelotti", "Santiago Bernabéu", "España", 1902))
    equipos.create(equipo("Boca Juniors", "Jorge Almirón", "La Bombonera", "Argentina", 1905))

    print("Mostrar lista de equipos:")
    for e in equipos.read():
        print(e)
        
    print("Actualizando entrenador de Atlas")
    equipos.update(0, equipo("Atlas", "Benjamin Mora", "Estadio Jalisco", "Mexico", 1916))
    for e in equipos.read():
        print(e)
    
    print("Eliminando Real Madrid")
    equipos.delete(1)
    for e in equipos.read():
        print(e)
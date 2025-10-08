from crud import crud
from jugadores import jugador
from equipo import equipo

class equipo_jugadores(crud):
    def __init__(self , equipo=None, jugadores=None):        
        self.es_lista = (equipo is None and jugadores is None)
        if self.es_lista:
            super().__init__()  
        else:
            self.equipo = equipo
            self.jugadores = jugador()
            for j in jugadores:
                self.jugadores.create(j)
                
    def __str__(self):
        if not self.es_lista:  
            texto_equipo = f"Equipo: {self.equipo.nombre}, Estadio: {self.equipo.estadio}, País: {self.equipo.pais}, Año de Fundación: {self.equipo.año_fundacion}"
            texto_jugadores = "\n".join(
                [f"   Jugador: {j.nombre}, Edad: {j.edad}, Posición: {j.posicion}, Nacionalidad: {j.nacionalidad}, Camiseta: {j.numero_de_camiseta}" 
                for j in self.jugadores.read()]
            )
            return texto_equipo + "\n" + texto_jugadores
        else:
            return f"Arreglo de {len(self.valor)} equipos con jugadores"

    def to_dict(self):
        if not self.es_lista:
            return {
            "equipo": self.equipo.to_dict(),
            "jugadores": self.jugadores.to_dict()
        }
        else:
            return super().to_dict()

if __name__ == "__main__":
    jugador1 = jugador("Lionel Messi", 36, "Delantero", "Argentina", 10)
    jugador2 = jugador("Cristiano Ronaldo", 39, "Delantero", "Portugal", 7)
    jugador3 = jugador("Kylian Mbappé", 25, "Delantero", "Francia", 7)

    equipo1 = equipo("Atlas", "Diego Cocca", "Estadio Jalisco", "México", 1916)
     
    #lista = equipo_jugadores()

    #lista.create(equipo_jugadores(equipo1, [jugador1, jugador2]))
    #lista.create(equipo_jugadores(equipo2, [jugador3]))


    eq1 = equipo_jugadores(equipo1,[jugador1, jugador2])
    
    print(eq1.to_dict())
 
    lista_equipos = equipo_jugadores()
    lista_equipos.create(eq1)
    lista_equipos.create(eq1)
    print(lista_equipos.to_dict())
 
# print("Mostrar Lista ")
# for ej in lista.read():
#     print(ej)
#     print("-" * 40)

# print("Actualizando PSG (agregar Neymar)...")
# jugador4 = jugador("Neymar Jr", 32, "Delantero", "Brasil", 10)
# equipo2_modificado = equipo("PSG", "Luis Enrique", "Parc des Princes", "Francia", 1970)
# lista.update(1, equipo_jugadores(equipo2_modificado, [jugador3, jugador4]))

# for ej in lista.read():
#     print(ej)
#     print("-" * 40)

# print("Eliminando al Atlas...")
# lista.delete(0)

# for ej in lista.read():
#     print(ej)
#     print("-" * 40)
#     ''''''''


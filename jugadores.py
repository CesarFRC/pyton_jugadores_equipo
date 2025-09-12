class jugador:
    def __init__(self, nombre: str ,edad: int ,posicion: str, nacionalidad: str, numero_de_camiseta: int):
        self.nombre = nombre
        self.edad = edad
        self.posicion = posicion
        self.nacionalidad = nacionalidad
        self.numero_de_camiseta = numero_de_camiseta  
  
if __name__ == "__main__":
    jugador1 = jugador("Lionel Messi", 36, "Delantero", "Argentino", 10)
    jugador2 = jugador("Cristiano Ronaldo", 39, "Delantero", "Portugués", 7)
    jugador3 = jugador("Lucas", 29, "Defensa", "Brasileño", 4)
    jugador4 = jugador("Fernando", 21, "Mediocampista", "Mexicano", 8)
    jugador5 = jugador("Sergio", 20, "Delantero", "Mexicano", 6)
    
    jugadores = [jugador1,jugador2,jugador3, jugador4, jugador5]
  


    """
    for j in jugadores:
        print(f"{j.nombre}:({j.numero_de_camiseta}) - {j.posicion} - {j.nacionalidad} - {j.edad} años")
    """




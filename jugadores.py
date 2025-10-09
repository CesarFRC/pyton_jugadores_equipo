from crud import crud
import json

class jugador(crud):
    def __init__(self, nombre=None, edad=None, posicion=None, nacionalidad=None, numero_de_camiseta=None):
        self.es_lista = (nombre is None and edad is None and posicion is None and nacionalidad is None and numero_de_camiseta is None)
        if self.es_lista:
            super().__init__()  
        else:
            self.nombre = nombre
            self.edad = edad
            self.posicion = posicion
            self.nacionalidad = nacionalidad
            self.numero_de_camiseta = numero_de_camiseta

    def __str__(self):
        if not self.es_lista: 
            return f"{self.nombre} ({self.numero_de_camiseta}) - {self.posicion} - {self.nacionalidad} - {self.edad} años"
        else:
            return f"Arreglo de {len(self.valor)} jugadores"

    def to_dict(self):
        if not self.es_lista:
            return {
                "nombre": self.nombre,
                "edad": self.edad,
                "posicion": self.posicion,
                "nacionalidad": self.nacionalidad,
                "numero_de_camiseta": self.numero_de_camiseta
            }
        else:
            return [j.to_dict() for j in self.valor]
        
        
    def guardar_json(self, nombre_archivo):
        if not self.es_lista:
            try:
                with open(nombre_archivo,"w", encoding="utf-8") as f:
                    json.dump(self.to_dict(), f, ensure_ascii= False,indent=4)
                print(f"Jugador guardado en '{nombre_archivo}'")
            except Exception as e:
                print(f"Error al guardar jugador: {e}")
        else:
            super().guardar_json(nombre_archivo)
            
   

if __name__ == "__main__":
    jugadores = jugador()

    jugadores.create(jugador("Lionel Messi", 36, "Delantero", "Argentina", 10))
    jugadores.create(jugador("Cristiano Ronaldo", 39, "Delantero", "Portugal", 7))
    jugadores.create(jugador("Lucas", 29, "Defensa", "Brasil", 4))

    #print("Mostrar lista")
    #for j in jugadores.read(): 
        #print(j)  

    #print("Actualizando el primer jugador")
    #jugadores.update(0, jugador("Lionel Messi", 37, "Delantero", "Argentina", 10))
    #for j in jugadores.read():
        #print(j)

    #print("Eliminando el segundo jugador")
    #jugadores.delete(1)
    #for j in jugadores.read():
        #print(j)

    print("Lista de diccionario de objeto jugador:")
    print(jugadores.read()[0].to_dict())

    print("Lista de diccionarios lista jugadores:")
    print(jugadores.to_dict())  
    
    
    jugadores.guardar_json("jugadores.json")
    
    kim = jugador("Kim", 40, "Defensa", "Peru", 12)
    kim.guardar_json("kim.json")

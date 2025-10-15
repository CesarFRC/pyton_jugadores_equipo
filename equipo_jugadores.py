from crud import crud
from jugadores import jugador
from equipo import equipo
import json


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
        
    @classmethod
    def lectura_json(cls, nombre_archivo):
        """Lee un archivo JSON y devuelve un objeto lista de equipos con jugadores"""
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            if isinstance(datos, list):
                lista = cls()
                for d in datos:
                    eq_data = d["equipo"]
                    jug_data = d["jugadores"]

                    eq_obj = equipo(
                        eq_data["nombre"],
                        eq_data["entrenador"],
                        eq_data["estadio"],
                        eq_data["pais"],
                        eq_data["año_fundacion"]
                    )

                    jugadores_obj = [jugador.from_dict(j) for j in jug_data]
                    lista.create(cls(eq_obj, jugadores_obj))

                print("JSON leído correctamente")
                return lista
            else:
                print("El archivo no contiene una lista de equipos")
                return cls()

        except FileNotFoundError:
            print(f"El archivo '{nombre_archivo}' no existe.")
            return cls()
        except Exception as e:
            print(f"Error al leer JSON: {e}")
            return cls() 
            
    

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
    
    
    
    lista_equipos = equipo_jugadores()
    lista_equipos.create(eq1)
    lista_equipos.create(equipo_jugadores(equipo1,[jugador1,jugador2]))
    lista_equipos.guardar_json("equipos_completos.json")
    lista_leida = equipo_jugadores.lectura_json("equipos_completos.json")
    lista_leida.guardar_json("equipos_completos_coopia.json")
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


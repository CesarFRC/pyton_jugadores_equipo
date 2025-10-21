from crud import crud
import json


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
        
    def to_dict(self):
        if not self.es_lista:
            return {
                "nombre": self.nombre,
                "entrenador": self.entrenador,
                "estadio": self.estadio,
                "pais": self.pais,
                "año_fundacion": self.año_fundacion
            }
        else:
            return [equipo.to_dict() for equipo in self.valor]
        
    @classmethod
    def from_dict(cls,data):
        return cls(
            nombre=data.get("nombre"),
            entrenador=data.get("entrenador"),
            estadio=data.get("estadio"),
            pais=data.get("pais"),
            año_fundacion=data.get("año_fundacion")
        )
        
    def convertir_a_objeto(self,data):
        if isinstance(data,list):
            lista = equipo()
            for d in data:
                lista.create(equipo.from_dict(d))
            return lista
        elif isinstance(data,dict):
            return equipo.from_dict(data)
        else:
            return equipo()
            
        
        
        """""""""


    @classmethod
    def from_dict(cls, data):
        return cls(
            nombre=data.get("nombre"),
            entrenador=data.get("entrenador"),
            estadio=data.get("estadio"),
            pais=data.get("pais"),
            año_fundacion=data.get("año_fundacions")
        )
        
    @classmethod
    def lectura_json(cls, nombre_archivo):
        try:
            with open(nombre_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            if isinstance(datos,list):
                lista = cls()
                for d in datos:
                    lista.create(cls.from_dict(d))
                print(f"Json leido y convertido desde el archivo")
                return lista
            else:
                return cls.from_dict(datos)
        except Exception as e:
            print(f"Error al leer JSON: {e}")
            return cls()

            """""""""

    

if __name__ == "__main__":
    equipos = equipo()
    
    equipos.create(equipo("Atlas","Diego Cocca", "Estadio Jalisco", "Mexico", 1916))
    equipos.create(equipo("Real Madrid", "Carlo Ancelotti", "Santiago Bernabéu", "España", 1902))
    equipos.create(equipo("Boca Juniors", "Jorge Almirón", "La Bombonera", "Argentina", 1905))




    
    #print("Mostrar lista de equipos:")
    #for e in equipos.read():
        #print(e)
        
    #print("Actualizando entrenador de Atlas")
    #equipos.update(0, equipo("Atlas", "Benjamin Mora", "Estadio Jalisco", "Mexico", 1916))
    #for e in equipos.read():
        #print(e)
    
    #print("Eliminando Real Madrid")
    #equipos.delete(1)
    #fr e in equipos.read():
        #print(e)
    
    
    print("Lista de diccionario de objeto equipo:")
    print(equipos.read()[0].to_dict())

    print("Lista de diccionarios lista de equipos:")
    print(equipos.to_dict())
    
    equipos.guardar_json("equipos.json")
    
    datos = equipos.lectura_json("equipos.json")
    
    nuevos_equipos = equipo().convertir_a_objeto(datos)
    
    nuevos_equipos.guardar_json("equipos_copia.json")


  
    #nuevos_equipos = equipo.lectura_json("equipos.json")
    #nuevos_equipos.guardar_json("equipos_copia.json")
    
        
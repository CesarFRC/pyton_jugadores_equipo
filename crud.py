import json
import inspect


class crud:
    def __init__(self, *args):
        
        self.valor = []

    def create(self, item):
        self.valor.append(item)

    def read(self):
        return self.valor

    def update(self, index, item):
        if 0 <= index < len(self.valor):
            self.valor[index] = item
        else:
            print("Índice fuera de rango")

    def delete(self, index):
        if 0 <= index < len(self.valor):
            del self.valor[index]
        else:
            print("Índice fuera de rango")
            
    def to_dict(self):
        return [item.to_dict() for item in self.valor]
    

    def guardar_json(self, nombre_archivo):
        """Guarda en json"""
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
            print(f"Lista guardada en '{nombre_archivo}'")
        except Exception as e:
            print(f"Error al guardar JSON: {e}")
            
    
    @classmethod
    def lectura_json(cls, archivo):
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)

            def crear_instancia(dic, clase):
                if not isinstance(dic, dict):
                    return dic

                params = inspect.signature(clase.__init__).parameters
                kwargs = {}

                for key, value in dic.items():
                    if key in params:
                        if isinstance(value, dict) and key.lower() == "equipo":
                            from equipo import equipo
                            kwargs[key] = crear_instancia(value, equipo)

                        elif isinstance(value, list) and key.lower() == "jugadores":
                            from jugadores import jugador
                            kwargs[key] = [crear_instancia(v, jugador) for v in value]

                        else:
                            kwargs[key] = value

                return clase(**kwargs)

            if isinstance(datos, list):
                lista = cls()  
                for item_data in datos:
                    lista.create(crear_instancia(item_data, cls))
                return lista

            elif isinstance(datos, dict):
                return crear_instancia(datos, cls)

            else:
                raise ValueError("JSON inválido: no es lista ni diccionario")

        except Exception as e:
            print(f"Error al leer JSON en {cls.__name__}: {e}")
            return None
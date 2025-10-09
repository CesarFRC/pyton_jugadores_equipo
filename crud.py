import json

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
    
    #Guarda lista como json
    def guardar_json(self, nombre_archivo):
        try:
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)
            print(f"Lista guardada en '{nombre_archivo}'")
        except Exception as e:
            print(f"Error al guardar JSON: {e}")
            
    
  
                
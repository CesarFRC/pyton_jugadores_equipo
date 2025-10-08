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
    
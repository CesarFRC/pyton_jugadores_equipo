class crud:
    def __init__(self, *args):
        if len(args) == 0:   
            self.es_lista = True
            self.valor = []
        elif len(args) == 1: 
            self.es_lista = True
            self.valor = [args[0]]
        else:                
            self.es_lista = False
            self.valor = args

    def create(self, item):
        if self.es_lista:
            self.valor.append(item)
        else:
            print("No se puede agregar a un objeto único")

    def read(self):
        return self.valor

    def update(self, index, item):
        if self.es_lista:
            if 0 <= index < len(self.valor):
                self.valor[index] = item
        else:
            print("No se puede actualizar un objeto único por índice")

    def delete(self, index):
        if self.es_lista:
            if 0 <= index < len(self.valor):
                del self.valor[index]
        else:
            print("No se puede eliminar de un objeto único")

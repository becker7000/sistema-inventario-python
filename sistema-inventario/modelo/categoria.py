
class Categoria:

    def __init__(self,_id,nombre):
        self.__id = _id
        self.__nombre = nombre

    # No imprime, solo entrega una cadena con formato (genera texto)
    def __str__(self):
        return f" [{self.__id}] {self.__nombre}"
